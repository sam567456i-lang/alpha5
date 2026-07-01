"""Tests for the Foundation module."""

from __future__ import annotations

import asyncio
import logging
import sys
import tempfile
import types
import unittest

from Backend.foundation import (
    ConfigurationError,
    DependencyContainer,
    EventBus,
    EventEnvelope,
    HealthChecker,
    HealthStatus,
    LifecycleManager,
    LifecycleState,
    PluginLoader,
    ServiceResolutionError,
    create_application_context,
    load_config,
    redact_mapping,
)


class ConfigurationLoaderTests(unittest.TestCase):
    def test_loads_defaults_and_overrides(self) -> None:
        config = load_config(
            environ={
                "APP_ENV": "testing",
                "LOG_FORMAT": "text",
                "HEALTH_TIMEOUT_SECONDS": "2.5",
            }
        )

        self.assertEqual(config.environment, "testing")
        self.assertEqual(config.log_format, "text")
        self.assertEqual(config.health_timeout_seconds, 2.5)

    def test_invalid_environment_fails(self) -> None:
        with self.assertRaises(ConfigurationError):
            load_config(environ={"APP_ENV": "invalid"})

    def test_env_file_is_loaded(self) -> None:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", delete=False) as handle:
            handle.write("APP_ENV=testing\nLOG_LEVEL=debug\n")
            path = handle.name

        config = load_config(env_file=path, environ={})

        self.assertEqual(config.environment, "testing")
        self.assertEqual(config.log_level, "DEBUG")


class DependencyContainerTests(unittest.TestCase):
    def test_resolves_registered_instance(self) -> None:
        container = DependencyContainer()
        service = object()
        container.register_instance("service", service)

        self.assertIs(container.resolve("service"), service)

    def test_missing_service_fails(self) -> None:
        container = DependencyContainer()

        with self.assertRaises(ServiceResolutionError):
            container.resolve("missing")


class EventBusTests(unittest.IsolatedAsyncioTestCase):
    async def test_emit_uses_contract_envelope_and_notifies_handler(self) -> None:
        bus = EventBus()
        seen: list[EventEnvelope] = []

        bus.subscribe("FoundationStarted", seen.append)
        event = await bus.emit(
            event_type="FoundationStarted",
            producer="foundation.tests",
            payload={"status": "ok"},
        )

        self.assertEqual(seen, [event])
        self.assertEqual(event.event_version, 1)
        self.assertEqual(event.payload["status"], "ok")
        self.assertIn("event_id", event.as_dict())

    async def test_replay_uses_recorded_event(self) -> None:
        bus = EventBus()
        replayed: list[str] = []

        await bus.emit(event_type="Replayable", producer="tests")
        bus.subscribe("Replayable", lambda event: replayed.append(event.event_id))
        await bus.replay("Replayable")

        self.assertEqual(len(replayed), 1)


class HealthCheckerTests(unittest.IsolatedAsyncioTestCase):
    async def test_runs_sync_and_async_checks(self) -> None:
        checker = HealthChecker()

        async def async_check() -> bool:
            await asyncio.sleep(0)
            return True

        checker.register("sync", lambda: True)
        checker.register("async", async_check)

        results = await checker.run_all()
        status_by_name = {result.name: result.status for result in results}

        self.assertEqual(status_by_name["sync"], HealthStatus.HEALTHY)
        self.assertEqual(status_by_name["async"], HealthStatus.HEALTHY)
        self.assertEqual(checker.overall_status(results), HealthStatus.HEALTHY)


class LifecycleManagerTests(unittest.IsolatedAsyncioTestCase):
    async def test_startup_and_shutdown_order(self) -> None:
        events: list[str] = []
        manager = LifecycleManager(logger=logging.getLogger("test.lifecycle"))

        manager.register_startup("first", lambda: events.append("start:first"))
        manager.register_startup("second", lambda: events.append("start:second"))
        manager.register_shutdown("first", lambda: events.append("stop:first"))
        manager.register_shutdown("second", lambda: events.append("stop:second"))

        await manager.startup()
        await manager.shutdown()

        self.assertEqual(manager.state, LifecycleState.STOPPED)
        self.assertEqual(
            events,
            ["start:first", "start:second", "stop:second", "stop:first"],
        )


class ApplicationContextTests(unittest.TestCase):
    def test_context_registers_foundation_services(self) -> None:
        context = create_application_context(
            environ={"APP_ENV": "testing", "LOG_FORMAT": "text"}
        )

        self.assertTrue(context.container.contains("config"))
        self.assertTrue(context.container.contains("event_bus"))
        self.assertIn("foundation.context", context.health_checker.registered_names())


class PluginLoaderTests(unittest.TestCase):
    def test_loads_module_and_calls_register(self) -> None:
        module_name = "alphagrid_test_plugin"
        module = types.ModuleType(module_name)

        def register(container: DependencyContainer) -> None:
            container.register_instance("plugin.loaded", True)

        module.register = register  # type: ignore[attr-defined]
        sys.modules[module_name] = module
        try:
            container = DependencyContainer()
            loader = PluginLoader(container)

            loaded = loader.load(module_name)

            self.assertEqual(loaded.module_path, module_name)
            self.assertTrue(container.resolve("plugin.loaded", bool))
            self.assertEqual(loader.loaded_plugins(), (module_name,))
        finally:
            sys.modules.pop(module_name, None)


class LoggingTests(unittest.TestCase):
    def test_redacts_secret_mapping_values(self) -> None:
        redacted = redact_mapping(
            {
                "api_key": "secret",
                "nested": {"password": "hidden", "safe": "visible"},
            }
        )

        self.assertEqual(redacted["api_key"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["password"], "[REDACTED]")
        self.assertEqual(redacted["nested"]["safe"], "visible")


class EventBusConcurrencyTests(unittest.IsolatedAsyncioTestCase):
    async def test_concurrent_subscribe_and_publish(self) -> None:
        import threading
        for _ in range(50):
            bus = EventBus()
            errors = []
            
            def subscriber_worker(i: int) -> None:
                def handler(event: EventEnvelope) -> None:
                    pass
                try:
                    bus.subscribe(f"Event{i}", handler)
                except Exception as e:
                    errors.append(e)

            threads = [threading.Thread(target=subscriber_worker, args=(i,)) for i in range(10)]
            for t in threads:
                t.start()
                
            for _ in range(10):
                await bus.emit(event_type="Event0", producer="test")
                
            for t in threads:
                t.join()
                
            self.assertEqual(len(errors), 0)

    async def test_bounded_history_does_not_lose_recent(self) -> None:
        bus = EventBus()
        
        for i in range(20000):
            await bus.emit(event_type="BoundedEvent", producer="test", payload={"i": i})
            
        history = await bus.history()
        self.assertEqual(len(history), 10000)
        self.assertEqual(history[-1].payload["i"], 19999)
        self.assertEqual(history[0].payload["i"], 10000)


if __name__ == "__main__":
    unittest.main()

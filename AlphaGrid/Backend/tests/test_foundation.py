import unittest
from Backend.foundation.base_registry import BaseRegistry, RegistryError, CRL
from Backend.foundation.global_registry import get_global_registry
from Backend.core.capability_knowledge_graph import CapabilityKnowledgeGraph, CapabilityNode

class TestFoundationServices(unittest.TestCase):
    def setUp(self):
        self.global_registry = get_global_registry()
        self.graph = CapabilityKnowledgeGraph()

    def test_global_registry_lazy_loading(self):
        # Ensure it doesn't crash on retrieval
        domain_reg = self.global_registry.get_registry("domain")
        self.assertIsNotNone(domain_reg)
        
    def test_base_registry_crl_enforcement(self):
        reg = BaseRegistry("TestReg")
        # Should register with default CRL0
        reg.register("item1", {"val": 1})
        manifest = reg.export_manifest()
        self.assertEqual(manifest["crl_states"]["item1"], "CRL0_CONCEPT")
        
        # Test explicit CRL
        reg.register("item2", {"val": 2}, crl=CRL.CRL7_CERTIFIED)
        manifest2 = reg.export_manifest()
        self.assertEqual(manifest2["crl_states"]["item2"], "CRL7_CERTIFIED")

    def test_registry_fingerprint_integrity(self):
        reg = BaseRegistry("TestRegIntegrity")
        data = {"mutable": "value"}
        reg.register("data1", data)
        self.assertTrue(reg.verify_integrity())
        
        # Mutate the data
        data["mutable"] = "corrupted"
        
        with self.assertRaises(RegistryError):
            reg.verify_integrity()

    def test_knowledge_graph_node_addition(self):
        node = CapabilityNode(
            identity="P10-LIQ-001",
            domain="Liquidity",
            platform="Platform10",
            program="Pipeline",
            family="Pool",
            engine="SweepEngine"
        )
        self.graph.add_node(node)
        self.assertEqual(len(self.graph.get_all_nodes()), 1)
        self.assertEqual(self.graph.get_node("P10-LIQ-001").domain, "Liquidity")

    def test_knowledge_graph_consumer_resolution(self):
        producer = CapabilityNode(
            identity="P10-PROD-001",
            domain="Time",
            platform="P10",
            program="Pipeline",
            family="Session",
            engine="SessionEngine",
            evidence_produced=["SessionData"]
        )
        consumer = CapabilityNode(
            identity="P11-CONS-001",
            domain="ICT",
            platform="P11",
            program="Pipeline",
            family="Killzone",
            engine="KillzoneEngine",
            evidence_consumed=["SessionData"]
        )
        self.graph.add_node(producer)
        self.graph.add_node(consumer)
        
        consumers = self.graph.get_downstream_consumers("P10-PROD-001")
        self.assertEqual(len(consumers), 1)
        self.assertEqual(consumers[0].identity, "P11-CONS-001")

if __name__ == "__main__":
    unittest.main()

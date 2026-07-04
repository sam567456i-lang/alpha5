import json
import os

SCHEMA_DIR = r"C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Governance\schemas"
os.makedirs(SCHEMA_DIR, exist_ok=True)

# Base fields required for every governance file
base_headers = {
    "schema_version": {"type": "string"},
    "format_version": {"type": "string"},
    "generated_by": {"type": "string"},
    "generated_at": {"type": "string", "format": "date-time"},
    "checksum": {"type": "string"}
}

# 1. taxonomy.schema.json
taxonomy_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "markets": {"type": "array", "items": {"type": "string"}},
        "trading_styles": {"type": "array", "items": {"type": "string"}},
        "timeframes": {"type": "array", "items": {"type": "string"}},
        "analysis_domains": {"type": "array", "items": {"type": "string"}},
        "strategy_families": {"type": "array", "items": {"type": "string"}},
        "dashboard_modules": {"type": "array", "items": {"type": "string"}},
        "ai_agents": {"type": "array", "items": {"type": "string"}},
        "data_sources": {"type": "array", "items": {"type": "string"}},
        "governance_status_lifecycle": {"type": "array", "items": {"type": "string"}}
    },
    "required": ["schema_version", "format_version", "checksum", "markets", "timeframes", "governance_status_lifecycle"]
}

# 2. registry.schema.json
registry_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "capabilities": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string", "pattern": "^[A-Z0-9\\-]+$"},
                    "name": {"type": "string"},
                    "version": {"type": "string"},
                    "maturity": {"type": "string"},
                    "relationships": {
                        "type": "object",
                        "properties": {
                            "hard_dependencies": {"type": "array", "items": {"type": "string"}},
                            "soft_dependencies": {"type": "array", "items": {"type": "string"}},
                            "optional_dependencies": {"type": "array", "items": {"type": "string"}},
                            "conflicting_capabilities": {"type": "array", "items": {"type": "string"}},
                            "replaces": {"type": "string"},
                            "deprecated_by": {"type": "string"}
                        }
                    },
                    "market_support": {
                        "type": "object",
                        "properties": {
                            "supported": {"type": "array", "items": {"type": "string"}},
                            "unsupported": {"type": "array", "items": {"type": "string"}},
                            "placeholder": {"type": "array", "items": {"type": "string"}},
                            "required_feeds": {"type": "array", "items": {"type": "string"}}
                        }
                    },
                    "streaming_support": {
                        "type": "object",
                        "properties": {
                            "batch": {"type": "boolean"},
                            "streaming": {"type": "boolean"},
                            "incremental": {"type": "boolean"},
                            "warmup_required": {"type": "integer"},
                            "stateful": {"type": "boolean"}
                        }
                    },
                    "dashboard_contracts": {
                        "type": "object",
                        "properties": {
                            "searchable": {"type": "array"},
                            "filterable": {"type": "array"},
                            "sortable": {"type": "array"},
                            "grouping": {"type": "boolean"},
                            "export": {"type": "boolean"},
                            "comparison": {"type": "boolean"}
                        }
                    },
                    "cross_platform_references": {
                        "type": "object"
                    }
                },
                "required": ["id", "name", "version", "maturity"]
            }
        }
    },
    "required": ["schema_version", "format_version", "checksum", "capabilities"]
}

# 3. validation.schema.json
validation_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "profiles": {
            "type": "object",
            "additionalProperties": {
                "type": "array",
                "items": {"type": "string"}
            }
        }
    }
}

# 4. roadmap.schema.json
roadmap_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "phases": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "status": {"type": "string"},
                    "items": {"type": "array", "items": {"type": "string"}}
                }
            }
        }
    }
}

# 5. platform_manifest.schema.json
platform_manifest_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "platform_id": {"type": "string", "pattern": "^P[0-9]{2}$"},
        "name": {"type": "string"},
        "owner": {"type": "string"},
        "version": {"type": "string"},
        "dependencies": {"type": "array", "items": {"type": "string"}},
        "subsystems": {"type": "array", "items": {"type": "string"}},
        "readiness": {
            "type": "object",
            "properties": {
                "architecture": {"type": "number"},
                "implementation": {"type": "number"},
                "validation": {"type": "number"},
                "performance": {"type": "number"},
                "documentation": {"type": "number"},
                "dashboard": {"type": "number"},
                "ai": {"type": "number"},
                "research": {"type": "number"},
                "testing": {"type": "number"},
                "governance": {"type": "number"}
            }
        }
    },
    "required": ["platform_id", "name", "readiness"]
}

# 6. repository_manifest.schema.json
repository_manifest_schema = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
        **base_headers,
        "repository": {"type": "string"},
        "platforms": {"type": "array", "items": {"type": "string"}},
        "roadmaps": {"type": "array", "items": {"type": "string"}},
        "schemas": {"type": "array", "items": {"type": "string"}},
        "external_repos": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "id": {"type": "string"},
                    "name": {"type": "string"},
                    "license": {"type": "string"},
                    "language": {"type": "string"},
                    "architecture_score": {"type": "number"}
                }
            }
        }
    },
    "required": ["repository", "platforms"]
}

schemas = {
    "taxonomy.schema.json": taxonomy_schema,
    "registry.schema.json": registry_schema,
    "validation.schema.json": validation_schema,
    "roadmap.schema.json": roadmap_schema,
    "platform_manifest.schema.json": platform_manifest_schema,
    "repository_manifest.schema.json": repository_manifest_schema
}

for filename, schema in schemas.items():
    path = os.path.join(SCHEMA_DIR, filename)
    with open(path, "w") as f:
        json.dump(schema, f, indent=2)

print("Generated 6 JSON schemas in Governance/schemas/")

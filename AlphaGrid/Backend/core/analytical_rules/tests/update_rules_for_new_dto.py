import os
import glob
import re

directories = [
    "Backend/core/analytical_rules/implementations/tier0/spatial",
    "Backend/core/analytical_rules/implementations/tier0/temporal",
    "Backend/core/analytical_rules/implementations/tier0/market"
]

for directory in directories:
    for filename in glob.glob(os.path.join(directory, "*.py")):
        if "__init__" in filename: continue
        with open(filename, "r") as f:
            content = f.read()

        # Add imports if missing
        if "from Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification" not in content:
            content = content.replace(
                "from Backend.core.analytical_rules.dto.rule_provenance_dto import RuleProvenanceDTO",
                "from Backend.core.analytical_rules.dto.rule_provenance_dto import RuleProvenanceDTO\nfrom Backend.core.analytical_rules.dto.evidence_classification import EvidenceClassification\nfrom Backend.core.analytical_rules.dto.rule_result_status import RuleResultStatus"
            )

        # Evidence replacement (add status, classification, schema_version, registry_version, compatibility_version)
        content = re.sub(
            r"evidence_type=([^,]+),",
            r"status=RuleResultStatus.SUCCESS,\n            classification=EvidenceClassification.PRIMITIVE,\n            evidence_type=\1,\n            schema_version='1.0.0',\n            registry_version='1.0.0',\n            compatibility_version='>=1.0.0',",
            content
        )

        with open(filename, "w") as f:
            f.write(content)

print("Updated existing rules.")

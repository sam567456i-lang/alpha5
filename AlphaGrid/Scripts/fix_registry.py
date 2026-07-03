import yaml

reg_path = r'C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Docs\Documentation_Registry.yaml'
with open(reg_path, 'r') as f:
    reg = yaml.safe_load(f)

# Find duplicates
seen = {}
for i, doc in enumerate(reg['documents']):
    doc_id = doc.get('Document_ID')
    if doc_id in seen:
        print(f"Duplicate found at index {i}: {doc_id} -> {doc.get('Path')} / {doc.get('Title')}")
        print(f"Original was at index {seen[doc_id]}: {reg['documents'][seen[doc_id]].get('Path')} / {reg['documents'][seen[doc_id]].get('Title')}")
    else:
        seen[doc_id] = i

# I will just write code to fix the IDs
def generate_new_id(prefix):
    for i in range(1, 1000):
        new_id = f"{prefix}-{i:03d}"
        if new_id not in seen:
            return new_id
    return None

new_docs = []
for doc in reg['documents']:
    doc_id = doc.get('Document_ID')
    # If it's one of the ones I added recently:
    if doc.get('Path') in [
        'Constitutions/architecture_bible.md',
        'Governance/master_dependency_graph.md',
        'Governance/master_phase_checklist.md',
        'Specifications/master_interface_specification.md'
    ]:
        prefix = doc_id.split('-')[0]
        new_id = generate_new_id(prefix)
        doc['Document_ID'] = new_id
        seen[new_id] = True
        print(f"Changed {doc.get('Path')} to {new_id}")
    new_docs.append(doc)

reg['documents'] = new_docs
with open(reg_path, 'w') as f:
    yaml.dump(reg, f, sort_keys=False)

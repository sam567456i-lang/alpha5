import os

paths = [
    r'C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\platforms\platform9_features',
    r'C:\Users\praka\Documents\Codex\2026-06-30\alphagrid-infinity-x-5-0-master\AlphaGrid\Backend\tests'
]

for p in paths:
    for root, dirs, files in os.walk(p):
        for f_name in files:
            if f_name.endswith('.py'):
                file_path = os.path.join(root, f_name)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                if 'AlphaGrid.Backend.' in content:
                    content = content.replace('AlphaGrid.Backend.', 'Backend.')
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)

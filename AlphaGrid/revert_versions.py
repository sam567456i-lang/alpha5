import os

math_dir = 'Backend/math/public'

for root, _, files in os.walk(math_dir):
    for f in files:
        if f.endswith('.py'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r') as file:
                content = file.read()
            
            content = content.replace('version="1.1.0"', 'version="1.0.0"')
            
            with open(filepath, 'w') as file:
                file.write(content)

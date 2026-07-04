import os

files = [
    'Backend/math/public/sma.py',
    'Backend/math/public/wma.py',
    'Backend/math/public/rolling_sum.py',
    'Backend/math/public/variance.py',
    'Backend/math/public/stddev.py'
]

for f in files:
    with open(f, 'r') as file:
        content = file.read()
    
    content = content.replace('complexity=complexity="O(n)"', 'complexity="O(n)"')
    
    with open(f, 'w') as file:
        file.write(content)
    print(f"Fixed {f}")

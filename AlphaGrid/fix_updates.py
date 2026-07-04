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
    
    func_name = f.split('/')[-1].split('.')[0]
    
    if f"def update_{func_name}" not in content:
        content += f"\n\ndef update_{func_name}(bar: Any, state: Dict[str, Any]) -> Any:\n    raise NotImplementedError(\"Streaming API reserved for future implementation.\")\n"
        
        with open(f, 'w') as file:
            file.write(content)
        print(f"Added update_{func_name} to {f}")

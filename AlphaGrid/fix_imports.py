import os

target_dirs = [
    'Backend/validation/validators',
    'Backend/math/public',
    'Tests/benchmarks',
    'Scripts'
]

replacements = {
    'Backend.math.moving_averages.ema': 'Backend.math.public.ema',
    'Backend.math.moving_averages.sma': 'Backend.math.public.sma',
    'Backend.math.moving_averages.wma': 'Backend.math.public.wma',
    'Backend.math.rolling.rolling_sum': 'Backend.math.public.rolling_sum',
    'Backend.math.statistics.variance': 'Backend.math.public.variance',
    'Backend.math.statistics.stddev': 'Backend.math.public.stddev',
    'Backend.math.indicator_result': 'Backend.math.public.indicator_result',
    'Backend.math.utilities.alignment': 'Backend.math.public.alignment',
    'Backend.math.utilities.nan': 'Backend.math.public.nan',
    'Backend.math.utilities.validation': 'Backend.math.public.validation'
}

for d in target_dirs:
    for root, dirs, files in os.walk(d):
        for f in files:
            if f.endswith('.py'):
                filepath = os.path.join(root, f)
                with open(filepath, 'r') as file:
                    content = file.read()
                
                new_content = content
                for old, new in replacements.items():
                    new_content = new_content.replace(old, new)
                    
                if new_content != content:
                    with open(filepath, 'w') as file:
                        file.write(new_content)
                    print(f'Updated {filepath}')

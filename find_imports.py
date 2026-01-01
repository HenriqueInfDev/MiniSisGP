import os

def find_relative_imports(root_dir):
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(subdir, file)
                with open(filepath, 'r') as f:
                    for line in f:
                        if line.strip().startswith('from ..'):
                            print(filepath)
                            break

find_relative_imports('app')

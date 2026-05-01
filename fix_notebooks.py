import json
import glob
import os

fix_code = [
    '# ── Fix PySpark path issue with spaces ──\n',
    'import os\n',
    'import sys\n',
    'venv_scripts = os.path.dirname(sys.executable)\n',
    'os.environ["PATH"] = f"{venv_scripts};{os.environ.get(\'PATH\', \'\')}"\n',
    'os.environ["PYSPARK_PYTHON"] = "python"\n',
    'os.environ["PYSPARK_DRIVER_PYTHON"] = "python"\n',
    '\n'
]

notebooks = glob.glob(r'e:\CUFE\Spring 25\Big Data\Project\notebooks\*.ipynb')
for nb_path in notebooks:
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)
            if 'SparkSession.builder' in source_text:
                # Remove old fix lines
                new_source = []
                for line in source:
                    if 'PYSPARK_PYTHON' not in line and 'PYSPARK_DRIVER_PYTHON' not in line and 'sys.executable' not in line:
                        new_source.append(line)
                
                # Prepend fix
                if 'venv_scripts' not in source_text:
                    cell['source'] = fix_code + new_source
                    modified = True
    
    if modified:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f'Fixed {os.path.basename(nb_path)}')

print('Done fixing notebooks.')

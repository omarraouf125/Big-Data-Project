"""Add HADOOP_HOME setup to all notebooks."""
import json
import glob
import os

HADOOP_LINES = [
    "# Fix Windows PySpark: set HADOOP_HOME\n",
    "os.environ['HADOOP_HOME'] = r'C:\\hadoop'\n",
    "os.environ['PATH'] = r'C:\\hadoop\\bin;' + os.environ.get('PATH', '')\n",
    "os.environ['PYSPARK_PYTHON'] = sys.executable\n",
    "os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable\n",
    "\n"
]

notebooks = sorted(glob.glob(r'e:\CUFE\Spring_25\Big Data\Project\notebooks\0*.ipynb'))
for nb_path in notebooks:
    if '01_' in nb_path:
        continue  # already fixed
    
    with open(nb_path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    
    modified = False
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source = cell.get('source', [])
            source_text = ''.join(source)
            if 'SparkSession.builder' in source_text and 'HADOOP_HOME' not in source_text:
                # Find the line with SparkSession and inject before it
                new_source = []
                for line in source:
                    if 'SparkSession.builder' in line or 'spark = (' in line:
                        new_source.extend(HADOOP_LINES)
                    new_source.append(line)
                cell['source'] = new_source
                modified = True
                break
        if modified:
            break
    
    # Also make sure import sys is present in the imports cell
    for cell in nb.get('cells', []):
        if cell.get('cell_type') == 'code':
            source_text = ''.join(cell.get('source', []))
            if 'import os' in source_text and 'import sys' not in source_text:
                cell['source'].insert(1, "import sys\n")
                modified = True
            break
    
    if modified:
        with open(nb_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1)
        print(f'Fixed {os.path.basename(nb_path)}')
    else:
        print(f'Skipped {os.path.basename(nb_path)} (already OK or no Spark init)')

print('Done.')

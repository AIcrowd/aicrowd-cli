import json
import os
import sys


def parse(ipynb_path, code_file=None, bash_file=None):

    if not ipynb_path.endswith('.ipynb'):
        sys.exit('%s is not Jupyter Notebook file.' % ipynb_path)
    if not os.path.isfile(ipynb_path):
        sys.exit('%s is not a valid file.' % ipynb_path)

    # Check outputfile
    filename = os.path.basename(ipynb_path)
    if code_file is None:
        path = os.path.dirname(ipynb_path)
        py_filename = filename.replace('.ipynb', '.py')
        outputfile = os.path.join(path, py_filename)
    elif not code_file.endswith('.py'):
        code_file += '.py'
        print('Added .py to outputfile')

    # Load Jupyter Notebook
    with open(ipynb_path) as f:
        ipynb = json.load(f)

    # Extract source from code-cells
    py_cells = [item['source'] for item in ipynb['cells']
                if item['cell_type'] == 'code']

    # Filter cells to omit and restructure sourcecode in list
    code = []
    for cell in py_cells:
        if cell[0].startswith('# omit cell'):
            continue
        for x in cell:
            code.append(x)

    # Create Ssring from code list
    code_string = ''
    bash_string = ''
    for line in code:
        if line.lstrip().startswith('%') or \
                line.lstrip().startswith('!'):
            bash_string += line.lstrip()[1:]
        else:
            code_string += line

        # Print code string to outputfile
    with open(code_file, 'w') as f:
        f.write(code_string)

    with open(bash_file, 'w') as f:
        f.write(bash_file)
        
    print('successfully extracted code of %s' % filename)
    return outputfile

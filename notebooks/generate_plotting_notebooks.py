import papermill as pm
import nbformat as nbf
from config import analysis_config

def modify_markdown_header(notebook_name, variable):
    notebook = nbf.read(notebook_name, nbf.NO_CONVERT)
    cells_to_keep = []
    for cell in notebook.cells:
        if cell.cell_type == 'markdown':
            cell['source'] = cell['source'].replace('Variable', variable)
        
        cells_to_keep.append(cell)
    new_notebook = notebook
    new_notebook.cells = cells_to_keep
    nbf.write(new_notebook, notebook_name, version=nbf.NO_CONVERT)
    return print(f'Modified {notebook_name} with {variable} header')

for variable_type in analysis_config['variables']:
    for variable in analysis_config['variables'][variable_type]:
        out_notebook_name = f"{variable_type}_{variable}.ipynb"
        pm.execute_notebook(
            "interactive_plot_template.ipynb",
            out_notebook_name,
            parameters=dict(variable=variable),
            kernel_name='python3'
        )
        modify_markdown_header(out_notebook_name, variable)
        
        

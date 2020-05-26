# Jupyter notebooks module loader
Allows to import Jupyter notebooks as if there were regular python modules.

The code is based on the following example from Jupyter's documentation:  
https://jupyter-notebook.readthedocs.io/en/stable/examples/Notebook/Importing%20Notebooks.html

## Installation
```bash
pip install jupyter-module-loader
```

## Usage
Suppose a project has the following files structure:
```text
src/
├── main.py
└── my_notebook.ipynb
```
Let `my_notebook.ipynb` have a cell containing following code:
```python
    def fn():
        ...
```
Within `main.py` it is possible to import `my_notebook.ipynb` like so:
```python
    import jupyter_module_loader
    jupyter_module_loader.register()

    import my_notebook
    my_notebook.fn() # Calls fn() defined within the notebook above
```

You may limit the cells that are imported by assigning tags to those cells you want to load and call ```jupyter_module_loader.register(tags=[<a list of tags that work as markers for cells that are to be imported>])```
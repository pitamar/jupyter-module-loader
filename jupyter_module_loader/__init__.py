import io, os, sys, types
from IPython import get_ipython
from nbformat import read
from IPython.core.interactiveshell import InteractiveShell

__all__ = ['find_notebook', 'NotebookLoader', 'NotebookFinder', 'register_hook']


def find_notebook(fullname, path=None):
    """find a notebook, given its fully qualified name and an optional path

    This turns "foo.bar" into "foo/bar.ipynb"
    and tries turning "Foo_Bar" into "Foo Bar" and "Foo-Bar" if Foo_Bar
    does not exist.
    """
    name = fullname.rsplit('.', 1)[-1]
    if not path:
        path = ['']

    transformers = [
        # let import Notebook_Name find "Notebook_Name.ipynb"
        lambda p: p,

        # let import Notebook_Name find "Notebook Name.ipynb"
        lambda p: p.replace('_', ' '),

        # let import Notebook_Name find "Notebook-Name.ipynb"
        lambda p: p.replace('_', '-'),
    ]
    for d in path:
        for transformer in transformers:
            nb_path = os.path.join(d, name + ".ipynb")
            transformed_path = transformer(nb_path)
            if os.path.isfile(transformed_path):
                return transformed_path


class NotebookModule(types.ModuleType):
    def __init__(self, fullname, path, loader):
        super().__init__(fullname)
        self.__file__ = path
        self.__loader__ = loader
        self.__dict__['get_ipython'] = get_ipython

    def __dir__(self):
        if '__dir__' in self.__dict__:
            fields = self.__dict__['__dir__']()
        elif '__all__' in self.__dict__:
            fields = self.__dict__['__all__']
        else:
            fields = [f for f in self.__dict__.keys() if f != 'get_ipython']

        return fields


class NotebookLoader(object):
    """Module Loader for Jupyter Notebooks"""

    def __init__(self, path=None):
        self.shell = InteractiveShell.instance()
        self.path = path

    def load_module(self, fullname):
        """import a notebook as a module"""
        path = find_notebook(fullname, self.path)

        print("importing Jupyter notebook from %s" % path)

        # load the notebook object
        with io.open(path, 'r', encoding='utf-8') as f:
            nb = read(f, 4)

        # create the module and add it to sys.modules
        # if name in sys.modules:
        #    return sys.modules[name]
        mod = NotebookModule(fullname=fullname, path=path, loader=self)
        sys.modules[fullname] = mod

        # extra work to ensure that magics that would affect the user_ns
        # actually affect the notebook module's ns
        save_user_ns = self.shell.user_ns
        self.shell.user_ns = mod.__dict__

        try:
            for cell in nb.cells:
                if cell.cell_type == 'code':
                    # transform the input to executable Python
                    code = self.shell.input_transformer_manager.transform_cell(cell.source)
                    # run the code in themodule
                    exec(code, mod.__dict__)
        finally:
            self.shell.user_ns = save_user_ns

        return mod


class NotebookFinder(object):
    """Module finder that locates Jupyter Notebooks"""

    def __init__(self):
        self.loaders = {}

    def __eq__(self, other):
        is_equal = type(other) == type(self)
        return is_equal

    def find_module(self, fullname, path=None):
        nb_path = find_notebook(fullname, path)
        if not nb_path:
            return

        key = path
        if path:
            # lists aren't hashable
            key = os.path.sep.join(path)

        # if key not in self.loaders:
        #     self.loaders[key] = NotebookLoader(path)

        self.loaders[key] = NotebookLoader(path)

        return self.loaders[key]


def register(*args, **kwargs):
    notebook_finder = NotebookFinder(*args, **kwargs)

    if notebook_finder in sys.meta_path:
        sys.meta_path.remove(notebook_finder)

    sys.meta_path.append(notebook_finder)

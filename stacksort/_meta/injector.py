import importlib.abc
import importlib.machinery
import sys
import types

from pathlib import Path

from stacksort._meta import stackoverflow

class StackSortFinder(importlib.abc.MetaPathFinder):
    _COMMON_PREFIX = "stacksort."

    def __init__(self, loader):
        self._loader = loader

    def find_spec(self, fullname, path, target=None):
        """Attempt to locate the requested module
        fullname is the fully-qualified name of the module,
        path is set to __path__ for sub-modules/packages, or None otherwise.
        target can be a module object, but is unused in this example.
        """
        print("Call from find_spec!", self, fullname, path, target)

        if fullname.startswith(self._COMMON_PREFIX):
            name = fullname[len(self._COMMON_PREFIX):]
            return self._gen_spec(name)

    def _gen_spec(self, fullname):
        return importlib.machinery.ModuleSpec(fullname, self._loader)


class StackSortLoader(importlib.abc.Loader):
    def create_module(self, spec):
        def stack_runner(unsorted_list):
            compiled_func = stackoverflow.find(spec.name) # Probably shouldn't return compiled code, wrong abstraction - just a stand-in
            return compiled_func(unsorted_list)

        return stack_runner
    def exec_module(self, module):
        pass

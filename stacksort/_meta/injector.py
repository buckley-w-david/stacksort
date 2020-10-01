import datetime
import importlib.abc
import importlib.machinery
import sys
import types

import logging

from pathlib import Path

from stacksort._meta import stackoverflow
from stacksort._meta import compile # FIXME propbably shouldn't shadow the name compile

class StackSortFinder(importlib.abc.MetaPathFinder):
    _COMMON_PREFIX = "stacksort."

    def __init__(self, loader):
        self._loader = loader

    def find_spec(self, fullname, path, target=None):
        if fullname.startswith(self._COMMON_PREFIX):
            name = fullname[len(self._COMMON_PREFIX):]
            return self._gen_spec(name)

    def _gen_spec(self, fullname):
        return importlib.machinery.ModuleSpec(fullname, self._loader)

safety_date = datetime.datetime(2020, 9, 30) # Block new answers from targetting this specifically I guess
class StackSortLoader(importlib.abc.Loader):
    def __init__(self, *args, **kwargs):
        self.selection_strategy = stackoverflow.SelectionStrategy.SEQUENTIAL
        self.safety_date = safety_date # Safe by default I guess, but that's less fun
        self.logger = logging.getLogger(__name__)

        super().__init__(*args, **kwargs)

    def be_safe(self):
        self.safety_date = safety_date

    def be_unsafe(self):
        self.safety_date = None # Woo! Lets go dude!

    def create_module(self, spec):
        def stack_runner(unsorted_list):
            for code_block in stackoverflow.find(spec.name.replace('_', ' '), self.selection_strategy, self.safety_date):
                self.logger.debug('CODE BLOCK\n\n%s\n\n', code_block)
                try:
                    runner = compile.compile_sorter(code_block)
                    return runner(unsorted_list)
                except Exception as e:
                    self.logger.debug(e)
            raise compile.NoValidCodeError("Whoops")
        return stack_runner

    def exec_module(self, module):
        pass

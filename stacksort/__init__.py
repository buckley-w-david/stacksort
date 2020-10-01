from stacksort._meta import injector
import sys

#
# I'm being pretty sneaky here by naming the loader 'config'
#
# This allows me to keep the python library flow for typical usage (lol, as if this would be used)
# >>> from stacksort import quicksort
#
# However it also allows me expose configuration options to a user that would want it
# >>> from stacksort import config # Does not go through the custom finder/loader since python can locate the object
# >>> config.selection_strategy = ...
# >>> from stacksort import quicksort # since the "config" object is the loader itself, it has access to configured selection_strategy
#
config = injector.StackSortLoader()
finder = injector.StackSortFinder(config)
sys.meta_path.append(finder)

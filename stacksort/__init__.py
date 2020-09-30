from stacksort._meta import injector
import sys

loader = injector.StackSortLoader()
finder = injector.StackSortFinder(loader)
sys.meta_path.append(finder)

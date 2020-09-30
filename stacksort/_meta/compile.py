import ast, _ast

# Never thought I'd import this... What a world we live in
from lib2to3 import refactor
fixers = refactor.get_fixers_from_package('lib2to3.fixes') # Why is this package like this?
refactoring_tool = refactor.RefactoringTool(fixers)

class NoValidCodeError(Exception):
    pass

class MultipleError(Exception):
    def __init__(self, context=None):
        self.context = [] if context is None else context

    def add_context(self, context: Exception):
        self.context.append(context)

    @property
    def message(self):
        return '\n'.join(str(exc) for exc in self.context)

def valid_signature(func_def: _ast.FunctionDef):
    # Only 1 function argument, or only 1 that isn't given a default value
    return len(func_def.args.args) == 1 or len(func_def.args.args) - len(func_def.args.defaults) == 1

def entrypoints(tree: _ast.Module):
    return [
        f.name
        for f in tree.body
        if isinstance(f, _ast.FunctionDef) and valid_signature(f)
    ]


class RemovePrints(ast.NodeTransformer):
    def visit_Expr(self, node):
        if isinstance(node, _ast.Expr) \
                and isinstance(node.value, _ast.Call) \
                and isinstance(node.value.func, _ast.Name) \
                and node.value.func.id == 'print':
            return None
        return node

remove_prints = RemovePrints()

class StackRunner:
    def __init__(self, tree, compiled_module):
        self.tree = tree
        self.code = compiled_module
        self.working_entrypoint = None
        self.err = MultipleError()
        # I wish I could keep this self-contained
        # but I can't get recursive functions to work correctly
        # when I do it the way I want to
        #
        # self.locals = {}
        # self.globals = {}
        # exec(compiled_module, self.globals, self.locals)
        #
        # This executes just fine, but when actually calling the function, it fails
        # trying to recurse since it does not exist in the actual global namespace
        #
        # If I were crazy, I could re-write the ast when compiling to change all refernces to functions
        # defined within the ast to be looked up in a passed-in dict instead of letting python
        # do normal name resolution

        exec(compiled_module, globals())

    def __call__(self, unsorted_list):
        ul = unsorted_list.copy()

        if self.working_entrypoint:
            return self.working_entrypoint(unsorted_list)

        for entrypoint in entrypoints(self.tree):
            try:
                func = globals()[entrypoint]
                val = func(ul)
                # If function returned a value
                if val: # This has weird behavior if the function executed fine, but was passed an empty list
                    self.working_entrypoint = func
                    return val
                # If it didn't return a value, check if it modified the list in-place
                elif ul != unsorted_list:
                    # Wrap the in-place function to make it return the sorted list
                    def func2(unsorted_list):
                        ul = unsorted_list.copy()
                        func(ul)
                        return ul
                    self.working_entrypoint = func2
                    return ul

            except Exception as e:
                self.err.add_context(e)

        raise NoValidCodeError("¯\_(ツ)_/¯") from self.err


# Heuristics Time!
# It has functions:
#   - Should we remove non-function elements? Probably not for now
#   - Try to call the functions
#       - If it has more than 1 function, try each?
#       - Only call functions that take a single argument, this is likely to catch any main funciton + recursive worker setup and call the right one
#           - What about functions that have 1 required argument and some more arguments but they have a default value?
# There are no functions:
#  - We make one ;)
#  - We'll need to scan the code for references to variables that do not have an assignment, those will be our function arguments
#       - If there is more than one such reference, we probably just bail since we only have 1 value to pass in (the unsorted list)
#       - If there are none, that probably means that the answer seeded an example list to sort. We could try to scan for list variable creation in this case and yeet it
#           - only check in the top level
#  - How do we handle knowing what to return...
#       - look for initialization of empty lists?  Probably a good candidate for what to return
#       - some of these will sort the list in-place, return the list param?

def compile_sorter(code: str):
    try:
        new_code = str(refactoring_tool.refactor_string(code, 'StackOverflow'))
        tree = ast.fix_missing_locations(ast.parse(new_code))
        new_tree = remove_prints.visit(tree)
        compiled_code = compile(new_tree, '<StackOverflow>', 'exec')
    except Exception as exc:
        raise

    return StackRunner(tree, compiled_code)


if __name__ == '__main__':
    __name__ = 'stacksort' # Don't want my test environment being '__main__' to screw with my results

    import random
    l = list(range(100))
    random.shuffle(l)

    example_code = {}

    # https://stackoverflow.com/a/41432461
    example_code['bubble'] = '''
def BubbleSort(logindata):
    NoSwaps = 1
    N = len(logindata)
    logindata = list(logindata)
    while NoSwaps == 1:
        Count = 1
        NoSwaps = 0
        for Count in range(N-1):
            if logindata[Count] > logindata[Count+1]:
                temp = logindata[Count]
                logindata[Count] = logindata[Count+1]
                logindata[Count+1]=temp
                NoSwaps=1
    return tuple(logindata)

if __name__ == "__main__":
    logindata=["tom@gmail.com","Password1"],["Harry","Password2"],["Jake","Password3"]
    logindata = BubbleSort(logindata)
    print(logindata)
    #(['Harry', 'Password2'], ['Jake', 'Password3'], ['tom@gmail.com', 'Password1'])
    '''

    # https://stackoverflow.com/a/18783542
    example_code['merge'] = '''
def msort2(x):
    if len(x) < 2:
        return x
    result = []          # moved!
    mid = int(len(x) / 2)
    y = msort2(x[:mid])
    z = msort2(x[mid:])
    while (len(y) > 0) and (len(z) > 0):
        if y[0] > z[0]:
            result.append(z[0])
            z.pop(0)
        else:
            result.append(y[0])
            y.pop(0)
    result += y
    result += z
    return result
    '''

    # https://stackoverflow.com/a/18762455
    example_code['merge_bad'] = '''
result = [0]*len(x)   # replace 0 with a suitable default element if necessary.
                      # or just copy x (result = x[:])
    '''

    # https://stackoverflow.com/a/18262384
    example_code['quicksort'] = '''
def sort(array=[12,4,5,6,7,3,1,15]):
    """Sort the array by using quicksort."""

    less = []
    equal = []
    greater = []

    if len(array) > 1:
        pivot = array[0]
        for x in array:
            if x < pivot:
                less.append(x)
            elif x == pivot:
                equal.append(x)
            elif x > pivot:
                greater.append(x)
        # Don't forget to return something!
        return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
    # Note that you want equal ^^^^^ not pivot
    else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
        return array
    '''

    # https://stackoverflow.com/a/27461889
    example_code['quicksort_2'] = '''
def partition(array, begin, end):
    pivot = begin
    for i in xrange(begin+1, end+1):
        if array[i] <= array[begin]:
            pivot += 1
            array[i], array[pivot] = array[pivot], array[i]
    array[pivot], array[begin] = array[begin], array[pivot]
    return pivot



def quicksort(array, begin=0, end=None):
    if end is None:
        end = len(array) - 1
    def _quicksort(array, begin, end):
        if begin >= end:
            return
        pivot = partition(array, begin, end)
        _quicksort(array, begin, pivot-1)
        _quicksort(array, pivot+1, end)
    return _quicksort(array, begin, end)
    '''

    # https://stackoverflow.com/a/42112362
    example_code['insertion'] = '''
alist = [4,7,9,1,3,0,5,2,6,8]
sortlist = []
print(alist)
print(sortlist)
sortlist.append(alist[0])
alist.pop(0)

while len(alist) != 0:
    swap = False
    for pos in range(0, len(sortlist)-1):
        if sortlist[pos] > alist[0] and swap != True:
            sortlist.insert(pos,alist[0])
            swap = True
            print(alist)
            print(sortlist)
    if swap == False:
        sortlist.insert(len(sortlist),alist[0])
    alist.pop(0)

alist = sortlist

print(alist)
    '''

    # https://stackoverflow.com/a/15235396
    example_code['selection'] = '''
source = [4,2,1,10,5,3,100]
for i in range(len(source)):
    mini = min(source[i:]) #find minimum element
    min_index = source[i:].index(mini) #find index of minimum element
    source[i + min_index] = source[i] #replace element at min_index with first element
    source[i] = mini                  #replace first element with min element
print source
    '''

    # https://stackoverflow.com/a/48384624
    example_code['selection_2'] = '''
aList = [1,5,6,3]

def selection_sort(List):
    for i in range(len(List)):
        min = i
        for k in range(i,len(List)):
            if List[k] < List[min]:
                min = k
        swap(List, min, i)
    print(List)

def swap(List, x, y):
    temp = List[x]
    List[x] = List[y]
    List[y] = temp

selection_sort(aList)
    '''

    for key, code in example_code.items():
        print('keyword: ', key)
        print('CODE:\n', code)
        print('Input List: ', l)
        print()
        try:
            runner = compile_sorter(code)
            print('Output List: ', runner(l))
        except Exception as e:
            print('Blew Up: ', e)
        print("\n------------\n")

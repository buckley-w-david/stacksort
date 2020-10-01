from stackapi import StackAPI
import datetime
import random
import enum
from bs4 import BeautifulSoup

StackOverflowApi = StackAPI('stackoverflow')
StackOverflowApi.page_size = 50
StackOverflowApi.max_pages = 1

class SelectionStrategy(enum.Enum):
    SEQUENTIAL = enum.auto()
    RANDOM = enum.auto()

    @staticmethod
    def from_str(name: str) -> 'SelectionStrategy':
        return getattr(SelectionStrategy, name.strip().upper())

'''

On import the module that is created will have to store the name it was imported as, and use that in the creation of an instance of the module/function that it returns
On call the function will do the following

1. Use /2.2/search?page=1&pagesize=5&order=desc&sort=relevance&tagged=python;sorting&nottagged=python-2.x&intitle={mergesort}&site=stackoverflow to get questions
2. Use /2.2/questions/{ids}/answers?order=desc&sort=activity&site=stackoverflow to get all answers
3. Loop through the answers, pull out the body, extract the code
    4. Given the code:
        - wrap response in a function that will ultimatly be called
            - If the code is already in a function, identify the function name so you can call it
                - If it's many functions, loop through them?
            - If it's just bare code, wrap it in a function
                - Need to identify variables in the block that don't have an assignment, those will have to be params
                    - What to do if there's more than 1?
    5. call that compiled code
    6. If it didn't explode and did return a value, we done. If not then go to the next loop

'''

def find(keyword, selection_strategy=SelectionStrategy.SEQUENTIAL, safety_date=None):
    question_options = {
        'order': 'desc',
        'sort': 'relevance',
        'q': keyword,
        'nottagged': 'python-2.x',
        'tagged': ['python', 'sorting'],
        'filter': '!b93xdWqUwqOO7m'
    }
    answer_options = {
        'order': 'desc',
        'sort': 'votes',
        'filter': '-XG6tqDiasfBQHS1'
    }
    if safety_date:
        question_options['todate'] = safety_date
        answer_options['todate'] = safety_date
    question_search = StackOverflowApi.fetch('search/advanced', **question_options)
    ids = [ item['question_id'] for item in question_search['items'] if item['is_answered'] ]
    answer_search = StackOverflowApi.fetch('questions/{ids}/answers', ids=ids, **answer_options)

    # TODO fetch more answers if we run out
    for answer in answer_search['items']:
        if safety_date:
            edit_date = datetime.datetime.fromtimestamp(answer.get('last_edit_date', 0))
            if edit_date > safety_date:
                continue
        soup = BeautifulSoup(answer['body'], features="lxml")
        for pre in soup.find_all('pre'):
            for code in pre.findChildren('code'):
                yield code.text

# example_code = dict()
# def _find(keyword, selection_strategy=SelectionStrategy.SEQUENTIAL, safety_date=None):
#     print(keyword, selection_strategy, safety_date)
#     match = example_code.get(keyword)
#     if not match:
#         return [random.choice(list(example_code.values()))]
#     return [match]
#
#     # https://stackoverflow.com/a/41432461
# example_code['bubble'] = '''
# def BubbleSort(logindata):
#     NoSwaps = 1
#     N = len(logindata)
#     logindata = list(logindata)
#     while NoSwaps == 1:
#         Count = 1
#         NoSwaps = 0
#         for Count in range(N-1):
#             if logindata[Count] > logindata[Count+1]:
#                 temp = logindata[Count]
#                 logindata[Count] = logindata[Count+1]
#                 logindata[Count+1]=temp
#                 NoSwaps=1
#     return tuple(logindata)
#
# if __name__ == "__main__":
#     logindata=["tom@gmail.com","Password1"],["Harry","Password2"],["Jake","Password3"]
#     logindata = BubbleSort(logindata)
#     print(logindata)
#     #(['Harry', 'Password2'], ['Jake', 'Password3'], ['tom@gmail.com', 'Password1'])
#     '''
#
#     # https://stackoverflow.com/a/18783542
# example_code['merge'] = '''
# def msort2(x):
#     if len(x) < 2:
#         return x
#     result = []          # moved!
#     mid = int(len(x) / 2)
#     y = msort2(x[:mid])
#     z = msort2(x[mid:])
#     while (len(y) > 0) and (len(z) > 0):
#         if y[0] > z[0]:
#             result.append(z[0])
#             z.pop(0)
#         else:
#             result.append(y[0])
#             y.pop(0)
#     result += y
#     result += z
#     return result
#     '''
#
#     # https://stackoverflow.com/a/18762455
# example_code['merge_bad'] = '''
# result = [0]*len(x)   # replace 0 with a suitable default element if necessary.
#                       # or just copy x (result = x[:])
#     '''
#
#     # https://stackoverflow.com/a/18262384
# example_code['quicksort'] = '''
# def sort(array=[12,4,5,6,7,3,1,15]):
#     """Sort the array by using quicksort."""
#
#     less = []
#     equal = []
#     greater = []
#
#     if len(array) > 1:
#         pivot = array[0]
#         for x in array:
#             if x < pivot:
#                 less.append(x)
#             elif x == pivot:
#                 equal.append(x)
#             elif x > pivot:
#                 greater.append(x)
#         # Don't forget to return something!
#         return sort(less)+equal+sort(greater)  # Just use the + operator to join lists
#     # Note that you want equal ^^^^^ not pivot
#     else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
#         return array
#     '''
#
#     # https://stackoverflow.com/a/27461889
# example_code['quicksort_2'] = '''
# def partition(array, begin, end):
#     pivot = begin
#     for i in xrange(begin+1, end+1):
#         if array[i] <= array[begin]:
#             pivot += 1
#             array[i], array[pivot] = array[pivot], array[i]
#     array[pivot], array[begin] = array[begin], array[pivot]
#     return pivot
#
#
#
# def quicksort(array, begin=0, end=None):
#     if end is None:
#         end = len(array) - 1
#     def _quicksort(array, begin, end):
#         if begin >= end:
#             return
#         pivot = partition(array, begin, end)
#         _quicksort(array, begin, pivot-1)
#         _quicksort(array, pivot+1, end)
#     return _quicksort(array, begin, end)
#     '''
#
#     # https://stackoverflow.com/a/42112362
# example_code['insertion'] = '''
# alist = [4,7,9,1,3,0,5,2,6,8]
# sortlist = []
# print(alist)
# print(sortlist)
# sortlist.append(alist[0])
# alist.pop(0)
#
# while len(alist) != 0:
#     swap = False
#     for pos in range(0, len(sortlist)-1):
#         if sortlist[pos] > alist[0] and swap != True:
#             sortlist.insert(pos,alist[0])
#             swap = True
#             print(alist)
#             print(sortlist)
#     if swap == False:
#         sortlist.insert(len(sortlist),alist[0])
#     alist.pop(0)
#
# alist = sortlist
#
# print(alist)
#     '''
#
#     # https://stackoverflow.com/a/15235396
# example_code['selection'] = '''
# source = [4,2,1,10,5,3,100]
# for i in range(len(source)):
#     mini = min(source[i:]) #find minimum element
#     min_index = source[i:].index(mini) #find index of minimum element
#     source[i + min_index] = source[i] #replace element at min_index with first element
#     source[i] = mini                  #replace first element with min element
# print source
#     '''
#
#     # https://stackoverflow.com/a/48384624
# example_code['selection_2'] = '''
# aList = [1,5,6,3]
#
# def selection_sort(List):
#     for i in range(len(List)):
#         min = i
#         for k in range(i,len(List)):
#             if List[k] < List[min]:
#                 min = k
#         swap(List, min, i)
#     print(List)
#
# def swap(List, x, y):
#     temp = List[x]
#     List[x] = List[y]
#     List[y] = temp
#
# selection_sort(aList)
#     '''



# stacksort

Inspired by the famous XKCD comic [Ineffective Sorts](https://xkcd.com/1185/).

```
StackSort connects to StackOverflow, searches for 'sort a list', and downloads and runs code snippets until the list is sorted.
```

## Disclaimer

Please do not actually run this. It has even less safety features than the [JavaScript version](https://gkoberger.github.io/stacksort/).

## Usage

Taking this idea an running with it, `stacksort` lets you fetch unsafe, unvetted, arbitrary code from StackOverflow and blindly execute it like you would any other python package!

```
>>> from stacksort import bubblesort
>>> l = [6, 9, 3, 1, 5, 4, 7, 8, 2]
>>> bubblesort(l)
# Who knows what happens here! It'll try to find a bubblesort implementation and run it
```

`stacksort` will search StackOverflow for python snippets, and use whatever you tried to import as part of the search criteria!

I have provided a Dockerfile for a bit of additional safety if you want to try to run it (I am aware containers aren't perfectly safe, but I didn't feel like setting up a real VM)

```bash
 $ docker build .
 $ docker run -it -v $PWD:/src $THE_BUILD_ID /bin/bash
 $ pip install -r requirements.txt
 $ pip install .
 $ python
```

```python
 >>> import random
 >>> l = list(range(100))
 >>> random.shuffle(l)

 >>> import logging
 >>> logging.basicConfig()

 >>> from stacksort import config
 >>> config.logger.setLevel(logging.DEBUG)

 >>> from stacksort import bubblesort
 >>> sorted_list = bubblesort(l)
DEBUG:stacksort._meta.injector:CODE BLOCK

list1, list2 = [1, 2, 3], [1, 4, 3]
print [index for index, (e1, e2) in enumerate(zip(list1, list2)) if e1 == e2]



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

[0, 2]



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

list1, list2 = ["a", "b", "c", "d", "e"], ["e", "d", "c", "b", "a"]
print [index for index, (e1, e2) in enumerate(zip(list1, list2)) if e1 == e2]



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

[2]



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

a, b = b, a



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

def gen_move(seq):
    from bisect import bisect_left
    out = seq[0:1]
    for elem in seq[1:]:
        index = bisect_left(out, elem)
        if seq[index] != elem:
            if index == 0:
                print "Move {} before {}".format(elem, out[index])
            else:
                print "Move {} after {}".format(elem, out[index - 1])
        out.insert(index, elem)
    print out



DEBUG:stacksort._meta.injector:empty body on If
DEBUG:stacksort._meta.injector:CODE BLOCK

gen_move([1,3,2,7,6,0,4])
Move 2 after 1
Move 6 after 3
Move 0 before 1
Move 4 after 3
[0, 1, 2, 3, 4, 6, 7]

gen_move(range(10)[::-1])
Move 8 before 9
Move 7 before 8
Move 6 before 7
Move 5 before 6
Move 4 before 5
Move 3 before 4
Move 2 before 3
Move 1 before 2
Move 0 before 1
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

gen_move(range(10))
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]



DEBUG:stacksort._meta.injector:invalid syntax (<unknown>, line 2)
DEBUG:stacksort._meta.injector:CODE BLOCK

In [5]: %timeit gen_move(range(10000, 0, -1))
10000 loops, best of 3: 84 us per loop



DEBUG:stacksort._meta.injector:invalid syntax (<unknown>, line 1)
DEBUG:stacksort._meta.injector:CODE BLOCK

sum(1 ln 1 + 2 ln 2 + 3 ln 3 + ..... n ln n) < O(n ln n)



DEBUG:stacksort._meta.injector:invalid syntax (<unknown>, line 1)
DEBUG:stacksort._meta.injector:CODE BLOCK

O(n)



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

%%cython
import numpy as np
cimport numpy as np
cimport cython
@cython.boundscheck(False) 
@cython.wraparound(False)
cpdef cython_bubblesort_numpy(long[:] np_ary):
    """ 
    The Cython implementation of bubble sort with NumPy memoryview.

    """
    cdef int count, i, j # static type declarations
    count = np_ary.shape[0]

    for i in range(count):
        for j in range(1, count):
            if np_ary[j] < np_ary[j-1]:
                np_ary[j-1], np_ary[j] = np_ary[j], np_ary[j-1]

    return np.asarray(np_ary)



DEBUG:stacksort._meta.injector:invalid syntax (<unknown>, line 1)
DEBUG:stacksort._meta.injector:CODE BLOCK

with open(file, 'r') as f:
    data = [int(line.strip()) for line in f]



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

int(' 13')    # 13
int('13\t')   # 13
int('13 \n')  # 13



DEBUG:stacksort._meta.injector:¯\_(ツ)_/¯
DEBUG:stacksort._meta.injector:CODE BLOCK

    swapped = True
    while swapped:
            swapped = False
            for i in range(0,len(lis)-1):
                    if lis[i] > lis[i + 1] or lis[i] == lis[i+1]:
                        swapped = True
                        switch = lis[i]
                        lis[i] = lis[i+1]
                        lis[i+1] = switch
    return lis



DEBUG:stacksort._meta.injector:unexpected indent (<unknown>, line 1)
DEBUG:stacksort._meta.injector:CODE BLOCK

import random

def createRandom():
    return [random.randrange(1,100) for i in range(100)]

def bubblesort(test):
    is_sorted = False
    while not is_sorted:
        is_sorted= True
        for y in range(len(test) - 1):
            if test[y] > test[y+1]:
                test[y], test[y+1] = test[y+1], test[y]
                is_sorted= False

lst = createRandom()
bubblesort(lst)
print(lst)
>>> print(sorted_list)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]
>>> from stacksort import quicksort
>>> other_sorted_list = quicksort(l)
DEBUG:stacksort._meta.injector:CODE BLOCK

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
>>> print(other_sorted_list)
[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99]

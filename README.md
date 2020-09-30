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

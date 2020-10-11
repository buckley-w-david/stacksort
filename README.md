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

## Try it Out!

You can try it out yourself in your browser using Binder and opening the `playground.ipynb` file. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/buckley-w-david/stacksort/master)

```
>>> from stacksort import config
>>> import logging
>>> logging.basicConfig(level=logging.DEBUG)
>>> config.logger.setLevel(logging.DEBUG)
>>> from random import shuffle
>>> l = list(range(100))
>>> shuffle(l)
>>> from stacksort import quicksort
>>> quicksort(l)
...
```

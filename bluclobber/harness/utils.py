def merge(dicta, dictb):
    dicta.update(dictb)
    return dicta

from functools import reduce
from collections import defaultdict
from collections import deque
from itertools import islice

import re

lowalpha=re.compile('[^a-z]')

def normalize(word):
    return re.sub(lowalpha,'',word.lower())

def add(x,y):
    return x+y

def triple_sum(a,b):
    return [a[0]+b[0],a[1]+b[1],a[2]+b[2]]

def double_sum(a,b):
    return [a[0]+b[0],a[1]+b[1]]

def merge_under(operand):
    def _reducer(a,b):
        for key in b:
            if key in a:
                a[key]=operand(a[key],b[key])
            else:
                a[key]=b[key]
        return a
    return _reducer

def groups_of(count, iterable):
    # in_groups_of(3,range(7)) gives:
    # [[0,1,2],[1,2,3],[2,3,4],[3,4,5],[4,5,6]]
    iterable=iter(iterable)# in case a sequence is given
    current=deque(islice(iterable,0,count))
    yield list(current)
    for element in iterable:
        current.popleft()
        current.append(element)
        yield list(current)

def groups_of_with_page(count, iterable):
    for group in groups_of(count, iterable):
        return group[0][0], map(lambda x: x[1], group)

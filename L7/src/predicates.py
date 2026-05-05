from typing import Callable, Iterable, Any
from itertools import islice

def forall(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return all(map(pred, iterable))

def exists(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return any(map(pred, iterable))

'''
    filter - zwraca zbiór dla których warunek jest spełniony
    islice - przechodzenie po maksymalnie n pierwszych elemetach zbioru
'''
def atleast(n: int, pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    if n <= 0: raise ValueError("Invalid n value")
    satisfied = filter(pred, iterable)
    return sum(1 for _ in islice(satisfied, n)) == n

def atmost(n: int, pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    if n <= 0: raise ValueError("Invalid n value")
    satisfied = filter(pred, iterable)
    return sum(1 for _ in islice(satisfied, n + 1)) <= n
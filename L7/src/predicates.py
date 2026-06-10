from typing import Callable, Iterable, Any, TypeVar
from itertools import islice

T = TypeVar('T')

def forall(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return all(map(pred, iterable))

def exists(pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    return any(map(pred, iterable))

'''
    filter - zwraca zbiór dla których warunek jest spełniony
    islice - przechodzenie po maksymalnie n pierwszych elemetach zbioru
'''
def atleast(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    if n < 0: raise ValueError("Invalid n value")
    if n == 0: return True
    satisfied = filter(pred, iterable)
    return sum(1 for _ in islice(satisfied, n)) == n

def atmost(n: int, pred: Callable[[T], bool], iterable: Iterable[T]) -> bool:
    if n < 0: raise ValueError("Invalid n value")
    satisfied = filter(pred, iterable)
    return sum(1 for _ in islice(satisfied, n + 1)) <= n

if __name__ == "__main__":
    abc = lambda x: x % 2 == 0
    print(atmost(3, abc, [2,3,4,5,7,1,2]))
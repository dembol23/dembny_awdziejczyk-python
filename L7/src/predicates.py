from typing import Callable, Iterable, Any

''' 
2a. forall (pred, iterable) funkcja zwraca True, jeśli każdy element
iterable spełnia predykat pred, w przeciwnym przypadku False.
'''
def forall(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return all(map(pred, iterable))

''' 
2b. exists (pred, iterable) funkcja zwraca True, jeśli co najmniej jeden
element iterable spełnia predykat pred, w przeciwnym przypadku False.
'''
def exists(pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return any(map(pred, iterable))

'''
2c. atleast (n, pred, iterable) funkcja zwraca True, jeśli co najmniej n
elementów iterable spełnia predykat pred, w przeciwnym przypadku False.
'''
def atleast(n: int, pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return sum(map(pred, iterable)) >= n


'''
2d. atmost (n, pred, iterable) funkcja zwraca True, jeśli co najwyżej n
elementów iterable spełnia predykat pred, w przeciwnym przypadku False.
'''
def atmost(n: int, pred: Callable[[Any], bool], iterable: Iterable[Any]) -> bool:
    return sum(map(pred, iterable)) <= n
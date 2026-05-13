import sys
from typing import Callable, Generator, Any
from functools import cache


def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator()

def mem_make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    if not hasattr(f, '_cache'):
        f._cache = cache(f)

    return make_generator(f._cache)

def mem_make_generator_rec(f):
    cached_f = cache(f)
    module = sys.modules[f.__module__]
    if hasattr(module, f.__name__):
        setattr(module, f.__name__, cached_f)
    return make_generator(cached_f)

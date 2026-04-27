from typing import Callable, Generator, Any
from functools import cache, cached_property


def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def generator():
        n = 1
        while True:
            yield f(n)
            n += 1

    return generator()

def mem_make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    return make_generator(cache(f))

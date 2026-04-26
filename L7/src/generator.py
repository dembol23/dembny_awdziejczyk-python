from typing import Callable, Generator, Any

def make_generator(f: Callable[[int], Any]) -> Generator[Any, None, None]:
    def generator():
        n = 1
        while True:
            yield(f(n))
            n +=1

    return generator()
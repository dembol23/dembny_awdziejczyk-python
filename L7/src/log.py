import logging
import time
from datetime import datetime
from typing import Callable
from functools import wraps


def log(level_name: str) -> Callable:
    level = getattr(logging, level_name.upper(), None)
    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {level_name!r}")
    
    def decorator(target):
        if isinstance(target, type):
            original_init = target.__init__

            @wraps(original_init)
            def new_init(self, *args, **kwargs):
                logger = logging.getLogger(target.__name__)
                logger.log(level, "Instantiated %s | args=%s kwargs=%s",
                           target.__name__, args, kwargs)
                original_init(self, *args, **kwargs)

            target.__init__ = new_init
            return target

        @wraps(target)
        def wrapper(*args, **kwargs):
            call_time = datetime.now()
            start = time.perf_counter()
            result = target(*args, **kwargs)
            duration = time.perf_counter() - start

            logger = logging.getLogger(target.__name__)
            logger.log(level,"\nFunction:  %s\nCall time: %s\nDuration:  %.6fs\nArguments: %s, %s\nResult:    %s\n",
                       target.__name__, call_time, duration, args, kwargs, result)

            return result

        return wrapper

    return decorator


@log("INFO")
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


@log("DEBUG")
class Car:
    def __init__(self, brand: str, year: int):
        self.brand = brand
        self.year = year


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    print(fib(5))

    car = Car("Toyota", 2020)
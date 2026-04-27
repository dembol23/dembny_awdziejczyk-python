import datetime
import logging
from typing import Callable
from functools import wraps


def log(level: str) -> Callable:
    def decorator(f: Callable) -> Callable:
        @wraps(f)
        def wrapper(*args, **kwargs):
            result = f(*args, **kwargs)

            logger = logging.getLogger(f.__name__)
            logger.setLevel(level)

            if not logger.handlers:
                handler = logging.StreamHandler()
                logger.addHandler(handler)

            logger.log(logging.getLevelName(level), f"""
                Function:  {f.__name__}
                Call time: {datetime.datetime.now()}
                Arguments: {args}, {kwargs}
                Result:    {result}""")

            return result

        return wrapper

    return decorator

@log("INFO")
def fib(n: int) -> int:
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

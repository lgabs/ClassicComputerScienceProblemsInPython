from typing import Dict
import timeit
from functools import lru_cache


@lru_cache(maxsize=None)
def fibonacci(n: int) -> int:
    if n < 2:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci2(n: int) -> int:
    start = timeit.default_timer()
    fib = fibonacci(n)
    stop = timeit.default_timer()
    print(f"Fibonacci({n}): {fib} ({stop - start}s)")


if __name__ == "__main__":
    fibonacci2(50)

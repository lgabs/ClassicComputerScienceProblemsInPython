from typing import List, Iterable, TypeVar, Callable
import timeit
import time
from generic_search import linear_contains, binary_contains

import random
import matplotlib.pyplot as plt

T = TypeVar("T")

LIST_SIZE: int = 1000000
MAX_NUMBER: int = LIST_SIZE


def timing(f):
    def wrap(*args, **kwargs):
        time1 = time.time()
        ret = f(*args, **kwargs)
        time2 = time.time()
        # print('{:s} function took {:.3f} ms'.format(f.__name__, (time2-time1)*1000.0))
        taken = (time2 - time1) * 1000.0  # in ms
        return ret, taken

    return wrap


@timing
def timed_linear_contains(iterable: Iterable[T], key: T) -> bool:
    return linear_contains(iterable, key)


@timing
def timed_binary_contains(iterable: Iterable[T], key: T) -> bool:
    return binary_contains(iterable, key)


def evaluate_search_times(
    n_searches: int, search_function: Callable[[Iterable[T], T], bool], sort: bool = False
):
    numbers: List[int] = [random.randint(0, MAX_NUMBER) for _ in range(LIST_SIZE)]
    if sort:
        numbers = sorted(numbers)
    times_taken = []
    for _ in range(n_searches):
        random_number = random.choice(numbers)
        contains, taken_time_ms = search_function(numbers, random_number)
        times_taken.append(taken_time_ms)

    return times_taken


if __name__ == "__main__":
    n_searches = 1000
    times_from_linear = evaluate_search_times(n_searches, timed_linear_contains)
    times_from_binary = evaluate_search_times(n_searches, timed_binary_contains, sort=True)

    # Times are very different, so we'll plot separately
    f, ax = plt.subplots(1, 2, figsize=(10, 6))
    ax[0].hist(times_from_linear, color="blue", alpha=0.7)
    mean = sum(times_from_linear) / len(times_from_linear)
    ax[0].axvline(mean, label=f"mean: {round(mean,2)}")
    ax[0].set_title("Linear Search")
    ax[0].set_xlabel("Time (ms)")
    ax[0].legend()

    ax[1].hist(times_from_binary, color="red", alpha=0.7)
    mean = sum(times_from_binary) / len(times_from_binary)
    ax[1].axvline(mean, label=f"mean: {round(mean,4)}")
    ax[1].set_title("Binary Search")
    ax[1].set_xlabel("Time (ms)")
    ax[1].legend()

    plt.suptitle(f"Different times to search numbers\nin a {LIST_SIZE} size list")
    plt.show()

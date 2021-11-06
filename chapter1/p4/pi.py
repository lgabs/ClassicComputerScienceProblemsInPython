import timeit
import matplotlib.pyplot as plt

def calculate_pi(n_terms: int) -> float:
    denominator: float = 1.0
    pi: float = 0.0
    for i in range(n_terms):
        pi += (-1)** i * (4 / denominator)
        denominator += 2.0
    return pi

def check_complexity():
    pis = []
    ns = []
    time = []
    for n in range(0, 1000, 1):
        ns.append(n)
        start = timeit.default_timer()
        pis.append(calculate_pi(n))
        stop = timeit.default_timer()
        time.append(stop - start)
    plt.plot(ns, time)
    plt.xlabel("number of terms"), plt.ylabel("Time taken (s)")
    plt.show()

if __name__ == "__main__":
    print(calculate_pi(1000000))
    check_complexity()
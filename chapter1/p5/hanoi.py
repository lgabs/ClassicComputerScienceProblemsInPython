from typing import TypeVar, Generic, List
T = TypeVar('T')

class Stack(Generic[T]):

    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)

def hanoi(begin: Stack[int], end: Stack[int], temp: Stack[int], disks: int) -> None:
    if disks == 1:
        end.push(begin.pop())
    else:
        hanoi(begin, temp, end, disks - 1) # solve H(n-1) to put stack on temp
        hanoi(begin, end, temp, 1) # move bottom disk to the end from begin
        hanoi(temp, end, begin, disks - 1) # solve H(n-1) again to move temp tower to the end

def hanoi_minimum_steps(n: int) -> int:
    if n == 1:
        return 1
    else:
        return 2 * hanoi_minimum_steps(n-1) + 1

if __name__ == "__main__":
    num_discs: int = 15
    tower_a: Stack[int] = Stack()
    tower_b: Stack[int] = Stack()
    tower_c: Stack[int] = Stack()
    for i in range(1, num_discs + 1):
        tower_a.push(i)
    print("towers before: ", tower_a, tower_b, tower_c)
    hanoi(tower_a, tower_c, tower_b, num_discs)
    print("towers later: ", tower_a, tower_b, tower_c)

    # arbitrary limit since 64 explodes calculations
    # exact solution is: 2^(n-1)*H(1) + (1 + 2^1 + 2^2 + ... + 2^(n-2))
    # which is:  2^(n-1)*H(1) + 2^(n-1) - 1 = 2^(n-1) * (H(1) + 1) - 1 = 2^n - 1
    if num_discs <= 20: 
        print("minimum moves: ", hanoi_minimum_steps(num_discs))

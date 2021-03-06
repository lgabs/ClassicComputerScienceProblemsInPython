from __future__ import annotations
from typing import (
    TypeVar,
    Iterable,
    Sequence,
    Generic,
    List,
    Callable,
    Set,
    Deque,
    Dict,
    Any,
    Optional,
    Union,
    Tuple,
)
from typing_extensions import Protocol
from heapq import heappush, heappop
import time

T = TypeVar("T")


def linear_contains(iterable: Iterable[T], key: T) -> bool:
    for item in iterable:
        if item == key:
            return True
    return False


C = TypeVar("C", bound="Comparable")


class Comparable(Protocol):
    def __eq__(self, other: Any) -> bool:
        ...

    def __lt__(self: C, other: C) -> bool:
        ...

    def __gt__(self: C, other: C) -> bool:
        return (not self < other) and self != other

    def __le__(self: C, other: C) -> bool:
        return self < other or self == other

    def __ge__(self: C, other: C) -> bool:
        return not self < other


def binary_contains(sequence: Sequence[C], key: C) -> bool:
    low: int = 0
    high: int = len(sequence) - 1
    while low <= high:  # while there is still a search space
        mid: int = (low + high) // 2
        if sequence[mid] < key:
            low = mid + 1
        elif sequence[mid] > key:
            high = mid - 1
        else:
            return True
    return False


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.pop()  # LIFO

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Generic[T]):
    def __init__(self) -> None:
        self._container: Deque[T] = Deque()

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def __len__(self) -> bool:
        return len(self._container)

    def push(self, item: T) -> None:
        self._container.append(item)

    def pop(self) -> T:
        return self._container.popleft()  # FIFO

    def __repr__(self) -> str:
        return repr(self._container)


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    @property
    def empty(self) -> bool:
        return not self._container  # not is true for empty container

    def push(self, item: T) -> None:
        heappush(self._container, item)  # in by priority

    def pop(self) -> T:
        return heappop(self._container)  # out by priority

    def __repr__(self) -> str:
        return repr(self._container)


class Node(Generic[T]):
    def __init__(
        self,
        state: T,
        parent: Optional[Node],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


def dfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    return_visited_states: bool = False,
) -> Optional[Node[T]]:
    """
    Generalized Deep-First Search Algorithm.
    """
    # frontier is where we've yet to go
    frontier: Stack[Node[T]] = Stack()
    frontier.push(Node(initial, None))  # Set inicial state on frontier
    # explored is where we've been
    explored: Set[T] = {initial}  # We start already at initial state
    visited_states: int = 0

    # keep going while there is more to explore
    while not frontier.empty:
        # remove the node from stack to analyze
        current_node: Node[T] = frontier.pop()
        visited_states += 1  # add one more visited state
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return (current_node, visited_states)
        # check where we can go next and haven't explored
        # remember that each successor is already a valid one
        # (ex: in maze problem, a blocked cell is not a valid successor)
        for child in successors(current_state):
            if child in explored:  # skip children we already explored
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))  # add node to frontier
    return (None, None)  # went through everything and never found goal


def bfs(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    verbose: bool = False,
) -> Optional[Node[T]]:
    """
    Generalized Breadth-First Search Algorithm.
    """
    # frontier is where we've yet to go
    frontier: Queue[Node[T]] = Queue()
    frontier.push(Node(initial, None))
    # explored is where we've been
    explored: Set[T] = {initial}
    visited_states: int = 0
    times: List[float] = []
    skipped: int = 0

    # keep going while there is more to explore
    while not frontier.empty:
        t1 = time.time()
        current_node: Node[T] = frontier.pop()  # takes from the left!
        if verbose:  # and visited_states % 100000 == 0 and visited_states > 0:
            print("Current Node:\n", current_node.state)
            print("Visited states: ", visited_states)
            print("States explored: ", len(explored))
            print("Skipped states: ", skipped)
            print(
                "Average time per loop: ",
                sum(times) / len(times) if len(times) > 0 else None,
            )
            print()
            # input("Press enter to continue...")
        visited_states += 1  # add one more visited state
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return (current_node, visited_states)
        # check where we can go next and haven't explored
        successors_nodes = successors(current_state)
        if verbose:
            print("Number of successors: ", len(successors_nodes))
            print("-" * 20)
        for child in successors_nodes:
            if child in explored:  # skip children we already explored
                skipped += 1
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))
        times.append((time.time() - t1) * 1000)  # in ms
    return (None, None)  # went through everything and never found goal


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], float],
    return_visited_states: bool = False,
) -> Optional[Node[T]]:
    # frontier is where we've yet to go
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0.0, heuristic(initial)))
    # explored is where we've been
    explored: Dict[T, float] = {initial: 0.0}
    visited_states: int = 0

    # keep going while there is more to explore
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        visited_states += 1  # add one more visited state
        current_state: T = current_node.state
        # if we found the goal, we're done
        if goal_test(current_state):
            return (current_node, visited_states)
        # check where we can go next and haven't explored
        for child in successors(current_state):
            new_cost: float = (
                current_node.cost + 1
            )  # 1 assumes a grid, need a cost function for more sophisticated apps

            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return (None, None)  # went through everything and never found goal


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    # work backwards from end to front
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


if __name__ == "__main__":
    print(linear_contains([1, 5, 15, 15, 15, 15, 20], 5))  # True
    print(binary_contains(["a", "d", "e", "f", "z"], "f"))  # True
    print(binary_contains(["john", "mark", "ronald", "sarah"], "sheila"))  # False

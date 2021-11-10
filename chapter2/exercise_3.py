from __future__ import annotations
from typing import List, Optional
from generic_search import bfs, Node, node_to_path

MISSIONARIES: int = 11
CANNIBALS: int = 10


class MCState:
    def __init__(self, missionaries: int, cannibals: int, boat: bool) -> None:
        self.wm: int = missionaries  # west bank missionaries
        self.wc: int = cannibals  # west bank cannibals
        self.em: int = MISSIONARIES - self.wm  # east bank missionaries
        self.ec: int = CANNIBALS - self.wc  # east bank cannibals
        self.boat: bool = boat

    def __str__(self) -> str:
        return (
            "On the west bank there are {} missionaries and {} cannibals.\n"
            "On the east bank there are {} missionaries and {} cannibals.\n"
            "The boat is on the {} bank."
        ).format(self.wm, self.wc, self.em, self.ec, ("west" if self.boat else "east"))

    @property
    def is_legal(self) -> bool:
        if self.wm < self.wc and self.wm > 0:
            return False
        if self.em < self.ec and self.em > 0:
            return False
        return True

    def __key(self):
        return (self.wm, self.wc, self.em, self.ec, self.boat)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        if isinstance(other, MCState):
            return self.__key() == other.__key()
        return NotImplemented

    def goal_test(self) -> bool:
        return self.is_legal and self.em == MISSIONARIES and self.ec == CANNIBALS

    def successors(self) -> List[MCState]:
        successors: List[MCState] = []
        if self.boat:  # boat on west bank
            if self.wm > 1:
                # try moving 2 missionaries
                successors.append(MCState(self.wm - 2, self.wc, not self.boat))
            if self.wm > 0:
                # try moving one missionary
                successors.append(MCState(self.wm - 1, self.wc, not self.boat))
            if self.wc > 1:
                # try moving 2 cannibals
                successors.append(MCState(self.wm, self.wc - 2, not self.boat))
            if self.wc > 0:
                # try moving one cannibal
                successors.append(MCState(self.wm, self.wc - 1, not self.boat))
            if (self.wc > 0) and (self.wm > 0):
                # try moving one of each category
                successors.append(MCState(self.wm - 1, self.wc - 1, not self.boat))
        else:  # boat on east bank
            if self.em > 1:
                successors.append(MCState(self.wm + 2, self.wc, not self.boat))
            if self.em > 0:
                successors.append(MCState(self.wm + 1, self.wc, not self.boat))
            if self.ec > 1:
                successors.append(MCState(self.wm, self.wc + 2, not self.boat))
            if self.ec > 0:
                successors.append(MCState(self.wm, self.wc + 1, not self.boat))
            if (self.ec > 0) and (self.em > 0):
                successors.append(MCState(self.wm + 1, self.wc + 1, not self.boat))
        return [x for x in successors if x.is_legal]


def display_solution(path: List[MCState]):
    if len(path) == 0:  # sanity check
        return
    old_state: MCState = path[0]
    print(old_state)
    for current_state in path[1:]:
        if current_state.boat:
            print(
                "{} missionaries and {} cannibals moved from the east bank to the west bank.\n".format(
                    old_state.em - current_state.em, old_state.ec - current_state.ec
                )
            )
        else:
            print(
                "{} missionaries and {} cannibals moved from the west bank to the east bank.\n".format(
                    old_state.wm - current_state.wm, old_state.wc - current_state.wc
                )
            )
        print(current_state)
        old_state = current_state


if __name__ == "__main__":
    start: MCState = MCState(MISSIONARIES, CANNIBALS, True)
    solution: Optional[Node[MCState]]
    visited_states: int
    solution, visited_states = bfs(start, MCState.goal_test, MCState.successors, True)
    if solution is None:
        print("No solution found!")
    else:
        path: List[MCState] = node_to_path(solution)
        display_solution(path)

    print("visited_states: ", visited_states)

from enum import Enum
from typing import List, NamedTuple, Callable, Optional
import random
from math import sqrt

from p2_generic_search import Node, dfs, node_to_path, bfs  # , astar


class Cell(str, Enum):
    EMPTY = " "
    BLOCKED = "X"
    START = "S"
    GOAL = "G"
    PATH = "*"


class MazeLocation(NamedTuple):
    row: int
    column: int


class Maze:
    def __init__(
        self,
        rows: int = 10,
        columns: int = 10,
        sparseness: float = 0.2,
        start: MazeLocation = MazeLocation(0, 0),
        goal: MazeLocation = MazeLocation(9, 9),
    ) -> None:
        # initialize basic instance variables
        self._rows: int = rows
        self._columns: int = columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        # fill the grid with empty cells
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for c in range(columns)] for r in range(rows)
        ]
        # populate the grid with blocked cells
        self._randomly_fill(rows, columns, sparseness)
        # fill the start and goal locations in
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def _randomly_fill(self, rows: int, columns: int, sparseness: float):
        for row in range(rows):
            for column in range(columns):
                if random.uniform(0, 1.0) < sparseness:
                    self._grid[row][column] = Cell.BLOCKED

    # return a nicely formatted version of the maze for printing
    def __str__(self) -> str:
        output: str = "-" * (self._columns + 2) + "\n"  # making outside limits
        for row in self._grid:
            output += "|" + "".join([c.value for c in row]) + "|\n"
        output += "-" * (self._columns + 2)  # making outside limits
        return output

    def goal_test(self, ml: MazeLocation) -> bool:
        """
        Test if a MazeLocation is our goal.
        """
        return ml == self.goal

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        """
        Get successors list of MazeLocations for a MazeLocation, i.e, every next
        MazeLocation which is a valid one.
        """
        locations: List[MazeLocation] = []
        if (
            ml.row + 1 < self._rows
            and self._grid[ml.row + 1][ml.column] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row + 1, ml.column))
        if ml.row - 1 >= 0 and self._grid[ml.row - 1][ml.column] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row - 1, ml.column))
        if (
            ml.column + 1 < self._columns
            and self._grid[ml.row][ml.column + 1] != Cell.BLOCKED
        ):
            locations.append(MazeLocation(ml.row, ml.column + 1))
        if ml.column - 1 >= 0 and self._grid[ml.row][ml.column - 1] != Cell.BLOCKED:
            locations.append(MazeLocation(ml.row, ml.column - 1))
        return locations

    def mark(self, path: List[MazeLocation]):
        """
        Mark a path of MazeLocations on the Maze Grid.
        """
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.PATH
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL

    def clear(self, path: List[MazeLocation]):
        """
        Clear a path from the Maze Grid and leave only start and goal marks.
        """
        for maze_location in path:
            self._grid[maze_location.row][maze_location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


if __name__ == "__main__":
    while True:
        # Test DFS
        m: Maze = Maze()  # initialize a ramdomly filled maze.
        print("--" * 30 + "\nLet's solve this nice maze:")
        print(m)
        input("Press enter to continue to our solution...")
        solution1: Optional[Node[MazeLocation]] = dfs(
            m.start, m.goal_test, m.successors
        )
        if solution1 is None:
            print("No solution found using depth-first search!")
        else:
            path1: List[MazeLocation] = node_to_path(solution1)
            m.mark(path1)
            print("depth-first search:")
            print(m)
            m.clear(path1)

        # Test BFS
        solution2: Optional[Node[MazeLocation]] = bfs(
            m.start, m.goal_test, m.successors
        )
        if solution2 is None:
            print("No solution found using breadth-first search!")
        else:
            path2: List[MazeLocation] = node_to_path(solution2)
            m.mark(path2)
            print("breadth-first search:")
            print(m)
            m.clear(path2)

        should_continue = input(
            "--" * 30 + "\nPress 'Y' to run another test of 'Q' to quit:\n\n\n"
        )
        if should_continue == "Q":
            break

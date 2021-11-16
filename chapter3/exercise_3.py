from __future__ import annotations
from enum import Enum
from typing import Coroutine, NamedTuple, List, Dict, Optional, Set, Tuple
from random import choice, randint, random
from math import sqrt, floor
from csp import CSP, Constraint


class SudokuCell(NamedTuple):
    """
    Variables for the problem, is a position (i,j) in the sudoku game,
    with i,j from 0 to 8.
    """

    row: int
    column: int

    def __eq__(self, other: SudokuCell):
        return hash((self.row, self.column)) == hash((other.row, other.column))


class SudokuGrid:
    def __init__(self, dimension: int = 9):
        self.dimension: int = dimension
        self.variables = []

    def __str__(self) -> str:
        """return a nicely formatted version of the maze for printing"""
        steps = int(sqrt(self.dimension))
        output = ""
        output += "-" * (self.dimension + 2 + (steps - 1)) + "\n"

        for i, row in enumerate(self.grid):
            output += "|"
            for k in range(0, self.dimension, steps):
                output += "".join(row[k : k + steps]) + "|"
            output += "\n"
            if (i + 1) % int(sqrt(self.dimension)) == 0:
                output += "-" * (self.dimension + 2 + (steps - 1)) + "\n"

        return output

    @property
    def cells(self) -> List[SudokuCell]:
        return [
            SudokuCell(i, j)
            for j in range(self.dimension)
            for i in range(self.dimension)
        ]

    def preset_sudoku(self, grid: List[List[str]]):
        self.grid = grid

    def generate_sudoku(self, sparseness: float = 0.80) -> None:
        # initialize empty grid and fill random positions

        def generate_digit():
            if random() <= sparseness:
                return " "
            else:
                return str(randint(1, 9))

        self.grid: List[List[str]] = [
            [generate_digit() for j in range(self.dimension)]
            for i in range(self.dimension)
        ]


class InnerGame(NamedTuple):
    i: int
    j: int

    def __eq__(self, other: InnerGame):
        return hash((self.i, self.j)) == hash((other.i, other.j))


class SudokuConstraint(Constraint[SudokuCell, str]):
    def __init__(self, cells: List[SudokuCell], dimension: int) -> None:
        super().__init__(cells)
        self.cells: List[str] = cells
        self.dimension = dimension
        self.steps = sqrt(dimension)

    def satisfied(self, assignment: Dict[SudokuCell, str]) -> bool:

        # inner games
        cell_games: Dict[InnerGame, List[str]] = {}
        # for each cell, O(N)
        for cell, value in assignment.items():
            cell_game: InnerGame = InnerGame(
                int(floor(cell.row / self.steps)), int(floor(cell.column / self.steps))
            )
            if cell_game not in cell_games:
                cell_games[cell_game] = [value]
            else:
                cell_games[cell_game].append(value)

        # for each game
        for game, values in cell_games.items():
            if len(set(values)) != len(values):
                return False

        # for each row
        for row in range(self.dimension):
            values = [values for cell, values in assignment.items() if cell.row == row]
            if len(set(values)) != len(values):
                return False

        # for each column
        for column in range(self.dimension):
            values = [
                values for cell, values in assignment.items() if cell.column == column
            ]
            if len(set(values)) != len(values):
                return False

        return True  # no conflit


def generate_domain() -> List[str]:
    return [str(k) for k in range(1, 10)]


if __name__ == "__main__":
    sudoku: SudokuGrid = SudokuGrid(9)
    # sudoku.generate_sudoku(sparseness=0.8)  # sudoku game with some filled
    preset_grid = [
        ["8", "3", " ", "2", " ", "6", " ", " ", " "],
        ["1", " ", " ", " ", "4", "5", " ", "9", " "],
        ["9", " ", "6", "8", " ", "7", "5", " ", "2"],
        [" ", " ", "4", " ", " ", " ", " ", "1", "8"],
        ["2", " ", " ", "7", "5", " ", " ", " ", " "],
        ["3", " ", "8", " ", "6", "1", "2", "5", "7"],
        ["5", " ", " ", "1", " ", " ", " ", " ", "3"],
        ["4", " ", " ", "6", " ", "9", " ", "8", " "],
        ["6", " ", "9", " ", " ", "3", " ", "2", "4"],
    ]
    sudoku.preset_sudoku(preset_grid)
    print("before:\n")
    print(sudoku)
    domains: Dict[SudokuCell, List[str]] = {}
    pre_assignment: Dict[SudokuCell, str] = {}
    for i, row in enumerate(sudoku.grid):
        for j, value in enumerate(row):
            cell = SudokuCell(i, j)
            if value != " ":
                pre_assignment[cell] = value
                domains[cell] = [value]  # the domain for a given sudoku number is fixed
            else:
                domains[cell] = generate_domain()

    csp: CSP[SudokuCell, str] = CSP(sudoku.cells, domains)
    csp.add_constraint(SudokuConstraint(sudoku.cells, sudoku.dimension))
    solution: Optional[Dict[SudokuCell, str]] = csp.backtracking_search(
        assignment=pre_assignment
    )

    if solution is None:
        print("No solution found!")
    else:
        print("found solution!\n")
        for cell, cell_solution in solution.items():
            sudoku.grid[cell.row][cell.column] = cell_solution

        print(sudoku)

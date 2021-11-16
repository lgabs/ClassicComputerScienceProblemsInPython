from __future__ import annotations
from typing import Coroutine, NamedTuple, List, Dict, Optional
from random import choice, randint, random
from math import sqrt
from string import ascii_uppercase
from csp import CSP, Constraint

Grid = List[List[str]]  # inner grid in sudoku
OuterGrid = List[List[Grid]]  # outer sudoku grid


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows: int, columns: int, sparseness: float = 0.80) -> OuterGrid:
    # initialize empty grid and fill random positions
    inner_sizes: int = int(sqrt(rows))  # equals 3 in classical sudoku

    def generate_number():
        if random() <= sparseness:
            return " "
        else:
            return str(randint(1, 9))

    def generate_inner_grid() -> Grid:
        return [
            [generate_number() for _ in range(inner_sizes)] for r in range(inner_sizes)
        ]

    outer_grid: OuterGrid = [
        [generate_inner_grid() for _ in range(inner_sizes)] for _ in range(inner_sizes)
    ]

    return outer_grid


def display_grid(outer_grid: OuterGrid) -> None:
    # return a nicely formatted version of the maze for printing
    n_rows: int = len(outer_grid)
    n_columns: int = len(outer_grid[0])
    n_inner_rows: int = len(outer_grid)
    n_inner_columns: int = len(outer_grid[0])

    output: str = ""
    for outer_row in outer_grid:
        output += (
            "-" * ((n_inner_columns + 1) * n_columns + 2 - 1) + "\n"
        )  # markers before row
        for r in range(n_rows):  # iterate through first line of 3 horizontal grids
            for c in range(n_columns):
                output += "|" + "".join(
                    [value for line in outer_row[c][r] for value in line]
                )
            # at the end of a line, we break
            output += "|\n"

    output += (
        "-" * ((n_inner_columns + 1) * n_columns + 2 - 1) + "\n"
    )  # markers at the end
    print(output)
    print()


if __name__ == "__main__":
    outer_grid: Grid = generate_grid(9, 9)
    print("grid before:\n")
    display_grid(outer_grid)

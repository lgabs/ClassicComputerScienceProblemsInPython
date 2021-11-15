from __future__ import annotations
from typing import Coroutine, NamedTuple, List, Dict, Optional
from random import choice, randint, random
from string import ascii_uppercase
from csp import CSP, Constraint

Grid = List[List[str]]  # type alias for grids


class Colors:
    CBLACK = "\33[30m"
    CRED = "\33[31m"
    CGREEN = "\33[32m"
    CYELLOW = "\33[33m"
    CBLUE = "\33[34m"
    CVIOLET = "\33[35m"
    CBEIGE = "\33[36m"
    CWHITE = "\33[37m"
    ENDC = "\033[0m"

    @classmethod
    def random_color(self) -> str:
        return choice(
            [
                self.CBLACK,
                self.CBLUE,
                self.CGREEN,
                self.CRED,
                self.CVIOLET,
                self.CYELLOW,
                self.CBEIGE,
            ]
        )


def colored_position(marker: str, color: str) -> str:
    return color + marker + Colors.ENDC


class GridLocation(NamedTuple):
    row: int
    column: int


class Circuit(NamedTuple):
    height: int
    width: int

    def __eq__(self, other: Circuit):
        return hash((self.height, self.width)) == hash((other.height, other.width))


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize empty grid
    return [[" " for _ in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    # return a nicely formatted version of the maze for printing
    rows = len(grid)
    columns = len(grid[0])

    output: str = "-" * (columns + 2) + "\n"  # making outside limits
    for row in grid:
        output += "|" + "".join([c for c in row]) + "|\n"
    output += "-" * (columns + 2)  # making outside limits

    print(output)
    print()


def generate_domain(circuit: Circuit, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    grid_height: int = len(grid)
    grid_width: int = len(grid[0])

    # iterate thought circuit board
    # try to position looking from left upper position's of circuit
    # do not rotate circuits
    for row in range(grid_height):
        for col in range(grid_width):
            columns: range = range(col, col + circuit.width + 1)
            rows: range = range(row, row + circuit.height + 1)

            if (
                col + circuit.width <= grid_width
                and row + circuit.height <= grid_height
            ):
                for c in columns:
                    for r in rows:
                        # ideally we could avoid using inner spaces for performance
                        domain.append([GridLocation(r, c)])

        return domain


class CircuitLayoutConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, circuits: List[Circuit]) -> None:
        super().__init__(circuits)
        self.circuits: List[str] = circuits

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # if there are any duplicates grid locations, then there is an overlap
        all_locations = [locs for values in assignment.values() for locs in values]
        return len(set(all_locations)) == len(all_locations)


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    print("grid before: ")
    display_grid(grid)
    circuits: List[Circuit] = [
        Circuit(1, 6),
        Circuit(4, 4),
        Circuit(2, 2),
        Circuit(3, 3),
        Circuit(2, 5),
    ]
    circuit_colors: List[str] = [
        Colors.CBEIGE,
        Colors.CBLUE,
        Colors.CGREEN,
        Colors.CVIOLET,
        Colors.CYELLOW,
        Colors.CRED,
    ]
    print("circuits:\n", circuits)
    locations: Dict[str, List[List[GridLocation]]] = {}
    for circuit in circuits:
        locations[circuit] = generate_domain(circuit, grid)
    csp: CSP[str, List[GridLocation]] = CSP(circuits, locations)
    csp.add_constraint(CircuitLayoutConstraint(circuits))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for circuit, grid_locations in solution.items():
            for loc in grid_locations:
                grid[loc.row][loc.column] = colored_position(
                    marker="X", color=circuit_colors[circuits.index(circuit)]
                )
        print("\nlater:\n")
        display_grid(grid)

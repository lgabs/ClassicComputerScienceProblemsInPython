from typing import Coroutine, NamedTuple, List, Dict, Optional, Set
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


def colored_letter(letter: str, color: str) -> str:
    return color + letter + Colors.ENDC


class GridLocation(NamedTuple):
    row: int
    column: int


def generate_grid(rows: int, columns: int) -> Grid:
    # initialize grid with random letters
    return [[choice(ascii_uppercase) for c in range(columns)] for r in range(rows)]


def display_grid(grid: Grid) -> None:
    for row in grid:
        print("".join(row))
    print()


def generate_domain(word: str, grid: Grid) -> List[List[GridLocation]]:
    domain: List[List[GridLocation]] = []
    height: int = len(grid)
    width: int = len(grid[0])
    length: int = len(word)
    for row in range(height):
        for col in range(width):
            columns: range = range(col, col + length + 1)
            rows: range = range(row, row + length + 1)
            if col + length <= width:
                # left to right
                domain.append([GridLocation(row, c) for c in columns])
                # diagonal towards bottom right
                if row + length <= height:
                    domain.append([GridLocation(r, col + (r - row)) for r in rows])
            if row + length <= height:
                # top to bottom
                domain.append([GridLocation(r, col) for r in rows])
                # diagonal towards bottom left
                if col - length >= 0:
                    domain.append([GridLocation(r, col - (r - row)) for r in rows])

        return domain


class WordSearchConstraint(Constraint[str, List[GridLocation]]):
    def __init__(self, words: List[str]) -> None:
        super().__init__(words)
        self.words: List[str] = words

    def satisfied(self, assignment: Dict[str, List[GridLocation]]) -> bool:
        # previously, we were only checking if the set of locations do not overlap
        # Now, if the sums of separate sets' length per letter differ from
        # their joint length, that's because we have duplicate locations
        # for different letters, which is conflit
        letters_map: Dict[str, Set[GridLocation]] = {}
        for word, locations in assignment.items():
            for letter, location in zip(word, locations):
                if letter not in letters_map:
                    letters_map[letter] = {location}
                else:
                    letters_map[letter].add(location)
        separate_sums_len: int = sum(
            [len(v) for v in letters_map.values()]
        )  # sum of sets' lenght
        jointed_sum_len: int = len(
            list(set().union(*letters_map.values()))
        )  # join all sets before taking length

        return (
            separate_sums_len == jointed_sum_len
        )  # if sums match, we do not have conflits


if __name__ == "__main__":
    grid: Grid = generate_grid(9, 9)
    print("grid before: ")
    display_grid(grid)
    words: List[str] = ["MATTHEW", "JOE", "MARY", "SARAH", "SALLY"]
    word_colors: List[str] = [
        Colors.CBEIGE,
        Colors.CBLUE,
        Colors.CGREEN,
        Colors.CVIOLET,
        Colors.CYELLOW,
        Colors.CRED,
    ]
    print("words:\n", words)
    locations: Dict[str, List[List[GridLocation]]] = {}
    for word in words:
        locations[word] = generate_domain(word, grid)
    csp: CSP[str, List[GridLocation]] = CSP(words, locations)
    csp.add_constraint(WordSearchConstraint(words))
    solution: Optional[Dict[str, List[GridLocation]]] = csp.backtracking_search()
    if solution is None:
        print("No solution found!")
    else:
        for word, grid_locations in solution.items():
            # random reverse half the time
            if choice([True, False]):
                grid_locations.reverse()
            for index, letter in enumerate(word):
                (row, col) = (grid_locations[index].row, grid_locations[index].column)
                grid[row][col] = colored_letter(
                    letter=letter, color=word_colors[words.index(word)]
                )
        print("\nlater:\n")
        display_grid(grid)

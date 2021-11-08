from p2_maze import *

MAZE_SIZE = 10

if __name__ == "__main__":
    while True:
        # Test DFS
        m: Maze = Maze(
            rows=MAZE_SIZE,
            columns=MAZE_SIZE,
            start=MazeLocation(0, 0),
            goal=MazeLocation(MAZE_SIZE - 1, MAZE_SIZE - 1),
        )  # initialize a ramdomly filled maze.
        print("--" * 30 + "\nLet's solve this nice maze:")
        print(m)
        input("Press enter to continue to our solution...")
        solution1: Optional[Node[MazeLocation]]
        visited_states: int
        solution1, visited_states = dfs(
            m.start, m.goal_test, m.successors, return_visited_states=True
        )
        if solution1 is None:
            print("No solution found using depth-first search!")
        else:
            path1: List[MazeLocation] = node_to_path(solution1)
            m.mark(path1)
            print("depth-first search:")
            print(m)
            m.clear(path1)
            print(f"{visited_states} states were visited.")

        # # Test BFS
        # solution2: Optional[Node[MazeLocation]] = bfs(
        #     m.start, m.goal_test, m.successors
        # )
        # if solution2 is None:
        #     print("No solution found using breadth-first search!")
        # else:
        #     path2: List[MazeLocation] = node_to_path(solution2)
        #     m.mark(path2)append
        # distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
        # solution3: Optional[Node[MazeLocation]] = astar(
        #     m.start, m.goal_test, m.successors, distance
        # )
        # if solution3 is None:
        #     print("No solution found using A*!")
        # else:
        #     path3: List[MazeLocation] = node_to_path(solution3)
        #     m.mark(path3)
        #     print("A* search:")
        #     print(m)

        should_continue = input(
            "--" * 30 + "\nPress 'Y' to run another test of 'Q' to quit:\n\n\n"
        )

        if should_continue == "Q":
            break

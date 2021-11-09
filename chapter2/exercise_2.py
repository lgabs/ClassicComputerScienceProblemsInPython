from p2_maze import *
import matplotlib.pyplot as plt

SIMULATIONS = 100
MAZE_SIZE = 10

if __name__ == "__main__":

    dfs_states = []
    dfs_pathsizes = []
    bfs_states = []
    bfs_pathsizes = []
    astar_states = []
    astar_pathsizes = []
    for s in range(SIMULATIONS):
        # initialize a ramdomly filled maze.
        m: Maze = Maze(
            rows=MAZE_SIZE,
            columns=MAZE_SIZE,
            start=MazeLocation(0, 0),
            goal=MazeLocation(MAZE_SIZE - 1, MAZE_SIZE - 1),
        )
        # Test DFS
        solution, n_states = dfs(m.start, m.goal_test, m.successors)
        if n_states:
            dfs_pathsizes.append(len(node_to_path(solution)))
            dfs_states.append(n_states)

        # Test BFS
        solution, n_states = bfs(m.start, m.goal_test, m.successors)
        if n_states:
            bfs_pathsizes.append(len(node_to_path(solution)))
            bfs_states.append(n_states)

        # Test DFS
        distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
        solution, n_states = astar(m.start, m.goal_test, m.successors, distance)
        if n_states:
            path = node_to_path(solution)
            astar_pathsizes.append(len(node_to_path(solution)))
            astar_states.append(n_states)

    f, ax = plt.subplots(1, 2, figsize=(12, 6))

    def plot_results(
        l: List[int], color: str, alpha: float, search_method: str, ax: plt.Axes
    ):
        ax.hist(l, color=color, alpha=0.7)
        mean = sum(l) / len(l)
        ax.axvline(mean, label=search_method + f" {round(mean,2)}", color=color)

    plot_results(dfs_states, "blue", 0.7, "DFS mean:", ax[0])
    plot_results(bfs_states, "red", 0.7, "BFS mean:", ax[0])
    plot_results(astar_states, "orange", 0.7, "A* mean:", ax[0])
    ax[0].set_title(
        f"Number of states visited in each maze solutions\n(simulations={SIMULATIONS}, maze size = {MAZE_SIZE})"
    )
    ax[0].legend(loc="upper left")

    plot_results(dfs_pathsizes, "blue", 0.7, "DFS mean:", ax[1])
    plot_results(bfs_pathsizes, "red", 0.7, "BFS mean:", ax[1])
    plot_results(astar_pathsizes, "orange", 0.7, "A* mean:", ax[1])
    ax[1].set_title(
        f"Path size in each maze solutions\n(simulations={SIMULATIONS}, maze size = {MAZE_SIZE})"
    )
    ax[1].legend(loc="upper left")

    plt.show()

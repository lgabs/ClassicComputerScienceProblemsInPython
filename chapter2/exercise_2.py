from p2_maze import *
from scipy import stats
import matplotlib.pyplot as plt

SIMULATIONS = 100
MAZE_SIZE = 10

if __name__ == "__main__":

    dfs_states = []
    bfs_states = []
    astar_states = []
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
            dfs_states.append(n_states)

        # Test BFS
        solution, n_states = bfs(m.start, m.goal_test, m.successors)
        if n_states:
            bfs_states.append(n_states)

        # Test DFS
        distance: Callable[[MazeLocation], float] = manhattan_distance(m.goal)
        solution, n_states = astar(m.start, m.goal_test, m.successors, distance)
        if n_states:
            astar_states.append(n_states)

    plt.hist(dfs_states, color="blue", alpha=0.7)
    mean = sum(dfs_states) / len(dfs_states)
    plt.axvline(mean, label=f"mean dfs: {round(mean,2)}", color='blue')

    plt.hist(bfs_states, color="red", alpha=0.7)
    mean = sum(bfs_states) / len(bfs_states)
    plt.axvline(mean, label=f"mean bfs: {round(mean,2)}", color='red')

    plt.hist(astar_states, color="orange", alpha=0.7)
    mean = sum(astar_states) / len(astar_states)
    plt.axvline(mean, label=f"mean astar: {round(mean,2)}", color='orange')

    plt.suptitle(f"Maze Solutions")
    plt.legend()
    plt.show()

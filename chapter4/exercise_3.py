# Use this chapter’s graph framework to prove or disprove the classic Bridges of Königsberg problem,
# as described on Wikipedia: https://en.wikipedia.org/wiki/Seven_Bridges_of_Königsberg.

from typing import TypeVar, List, Optional
from weighted_edge import WeightedEdge
from weighted_graph import WeightedGraph
import sys

sys.path.insert(
    0, ".."
)  # so we can access the Chapter2 package in the parent directory
from chapter2.generic_search import bfs, Node

from itertools import combinations


V = TypeVar("V")  # type of the vertices in the graph


def BridgeSolution(graph: WeightedGraph) -> bool:
    """
    Euler's solution for bridge problem.
    """

    # Check that graph is connected
    # A graph is connected if there is a path from any vertex
    # to any other vertex
    for u, v in list(combinations(graph._vertices, 2)):
        bfs_result: Optional[Node[V]]
        bfs_result, _ = bfs(u, lambda x: x == v, graph.neighbors_for_vertex)
        if bfs_result is None:
            print("The graph is not connected.")
            return False

    # check degree of nodes
    degrees_parity: List[int] = []
    for vertex in graph._vertices:
        edges: List[WeightedEdge] = graph.edges_for_vertex(vertex)
        degrees_parity.append(len(edges) % 2)
    # degrees list must have exactly zero or two cases of
    # odd degree
    if sum(degrees_parity) not in (0, 2):
        return False
    else:
        return True


if __name__ == "__main__":
    graph: WeightedGraph[str] = WeightedGraph(
        [
            "land1",
            "land2",
            "land3",
            "land4",
        ]
    )
    graph.add_edge_by_vertices("land1", "land2", "bridge 1")
    graph.add_edge_by_vertices("land1", "land2", "bridge 2")
    graph.add_edge_by_vertices("land1", "land3", "bridge 3")
    graph.add_edge_by_vertices("land1", "land3", "bridge 4")
    graph.add_edge_by_vertices("land1", "land4", "bridge 5")
    graph.add_edge_by_vertices("land4", "land2", "bridge 6")
    graph.add_edge_by_vertices("land4", "land3", "bridge 7")

    print("Graph from original problem:")
    print(graph)

    print("Does the graph has solution for bridge problem?")
    solution: bool = BridgeSolution(graph)
    print("Answer: ", solution)
    print("-" * 60)

    print("Example of graph with zero odd degrees:")
    graph2: WeightedGraph[str] = WeightedGraph(
        [
            "land1",
            "land2",
            "land3",
            "land4",
        ]
    )
    graph2.add_edge_by_vertices("land1", "land2", "bridge 1")
    graph2.add_edge_by_vertices("land1", "land3", "bridge 2")
    graph2.add_edge_by_vertices("land4", "land2", "bridge 3")
    graph2.add_edge_by_vertices("land4", "land3", "bridge 4")
    print(graph2)

    print("Does the graph has solution for bridge problem?")
    solution: bool = BridgeSolution(graph2)
    print("Answer: ", solution)
    print("-" * 60)

    print("Example of graph with exactly two nodes with odd degrees:")
    graph3: WeightedGraph[str] = WeightedGraph(
        [
            "land1",
            "land2",
            "land3",
            "land4",
        ]
    )
    graph3.add_edge_by_vertices("land1", "land2", "bridge 1")
    graph3.add_edge_by_vertices("land1", "land3", "bridge 2")
    graph3.add_edge_by_vertices("land4", "land2", "bridge 3")
    graph3.add_edge_by_vertices("land4", "land3", "bridge 4")
    graph3.add_edge_by_vertices("land1", "land4", "bridge 5")
    print(graph3)

    print("Does the graph has solution for bridge problem?")
    solution: bool = BridgeSolution(graph3)
    print("Answer: ", solution)
    print("-" * 60)

    print("Example of graph not connected:")
    graph4: WeightedGraph[str] = WeightedGraph(
        [
            "land1",
            "land2",
            "land3",
            "land4",
        ]
    )
    graph4.add_edge_by_vertices("land1", "land2", "bridge 1")
    graph4.add_edge_by_vertices("land1", "land3", "bridge 2")
    graph4.add_edge_by_vertices("land2", "land3", "bridge 3")
    print(graph4)

    print("Does the graph has solution for bridge problem?")
    solution: bool = BridgeSolution(graph4)
    print("Answer: ", solution)

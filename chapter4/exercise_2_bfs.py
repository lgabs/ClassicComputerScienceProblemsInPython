from typing import TypeVar, Generic, List, Optional, Tuple
from edge import Edge
from graph import Graph

from typing import TypeVar, List, Optional

V = TypeVar("V")  # type of the vertices in the graph


class DiGraph(Generic[V], Graph[V]):

    # This is an DIRECTED graph,
    # so we always DO NOT ADD edges in both directions
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)


def build_graph(vertices: List[V] = [], edges: List[Tuple[str, str]] = []) -> DiGraph:
    graph: DiGraph[str] = DiGraph(vertices=vertices)
    for edge in edges:
        graph.add_edge_by_vertices(*edge)

    return graph


if __name__ == "__main__":
    # test basic Graph construction
    vertices: List[str] = [
        "Seattle",
        "San Francisco",
        "Los Angeles",
        "Riverside",
        "Phoenix",
        "Chicago",
        "Boston",
        "New York",
        "Atlanta",
        "Miami",
        "Dallas",
        "Houston",
        "Detroit",
        "Philadelphia",
        "Washington",
    ]
    edges: List[Tuple[str, str]] = [
        ("Seattle", "Chicago"),
        ("Seattle", "San Francisco"),
        ("San Francisco", "Riverside"),
        ("San Francisco", "Los Angeles"),
        ("Los Angeles", "Riverside"),
        ("Los Angeles", "Phoenix"),
        ("Riverside", "Phoenix"),
        ("Riverside", "Chicago"),
        ("Phoenix", "Dallas"),
        ("Phoenix", "Houston"),
        ("Dallas", "Chicago"),
        ("Dallas", "Atlanta"),
        ("Dallas", "Houston"),
        ("Houston", "Atlanta"),
        ("Houston", "Miami"),
        ("Atlanta", "Chicago"),
        ("Atlanta", "Washington"),
        ("Atlanta", "Miami"),
        ("Miami", "Washington"),
        ("Chicago", "Detroit"),
        ("Detroit", "Boston"),
        ("Detroit", "Washington"),
        ("Detroit", "New York"),
        ("Boston", "New York"),
        ("New York", "Philadelphia"),
        ("Philadelphia", "Washington"),
    ]

    # test graph build
    print("-" * 100 + "\nTest graph build")
    city_graph1 = build_graph(vertices[:], edges)
    print(city_graph1)
    print("Check the edges of two vertexs with edges linking them:")
    print("Philadelphia: ", city_graph1.edges_for_vertex("Philadelphia"))
    print("Washington: ", city_graph1.edges_for_vertex("Washington"))

    # 2. Test bfs
    start = "Atlanta"
    end = "New York"
    print("-" * 100 + f"\nTest BFS: {start}->{end}")
    city_DiGraph = build_graph(vertices[:], edges)
    # Reuse BFS from chapter 2 on city_graph
    import sys

    sys.path.insert(
        0, ".."
    )  # so we can access the Chapter2 package in the parent directory
    from chapter2.generic_search import bfs, Node, node_to_path

    bfs_result: Optional[Node[V]]
    visited_states: int
    bfs_result, visited_states = bfs(
        start, lambda x: x == end, city_DiGraph.neighbors_for_vertex
    )
    if bfs_result is None:
        print("No solution found using breadth-first search!")
    else:
        path: List[V] = node_to_path(bfs_result)
        print("Path from Boston to Miami:")
        print(path)
        print("visited states: ", visited_states)

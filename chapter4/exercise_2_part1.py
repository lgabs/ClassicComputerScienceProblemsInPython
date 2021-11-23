from typing import TypeVar, Generic, List, Optional, Tuple
from edge import Edge

V = TypeVar("V")  # type of the vertices in the graph


class Graph(Generic[V]):
    def __init__(self, vertices: List[V] = []) -> None:
        self._vertices: List[V] = vertices[:]  # makes a new instance of vertices list
        self._edges: List[List[Edge]] = [[] for _ in vertices]  #  adjacency lists

    @property
    def vertex_count(self) -> int:
        return len(self._vertices)  # Number of vertices

    @property
    def edge_count(self) -> int:
        return sum(map(len, self._edges))  # Number of edges.

    # Add a vertex to the graph and return its index
    def add_vertex(self, vertex: V) -> int:
        self._vertices.append(vertex)
        self._edges.append([])  # Add empty list for containing edges
        return self.vertex_count - 1  # Return index of added vertex

    def remove_vertex(self, vertex: V) -> V:
        """
        remove a vertex from the graph and return it. It will remove
        all related edges and update the indexes.
        """
        removed_index: int = self.index_of(vertex)
        removed_vertex: V = self._vertices.pop(removed_index)
        removed_edges: List[Edge] = self._edges.pop(removed_index)
        # remove other related edges using connected edges (for bidirectional graphs)
        # remember that every vertex shifted left one unit
        def update_edge(edge: Edge, removed_index: int):
            u: int = edge.u if edge.u < removed_index else edge.u - 1
            v: int = edge.v if edge.v < removed_index else edge.v - 1
            return Edge(u, v)

        for i in range(self.vertex_count):
            self._edges[i] = [
                update_edge(edge, removed_index)
                for edge in self._edges[i]
                if edge.v != removed_index
            ]

        return removed_vertex

    # This is an DIRECTED graph,
    # so we always DO NOT ADD edges in both directions
    def add_edge(self, edge: Edge) -> None:
        self._edges[edge.u].append(edge)

    # Add an edge using vertex indices (convenience method)
    def add_edge_by_indices(self, u: int, v: int) -> None:
        edge: Edge = Edge(u, v)
        self.add_edge(edge)

    # Add an edge by looking up vertex indices (convenience method)
    def add_edge_by_vertices(self, first: V, second: V) -> None:
        u: int = self._vertices.index(first)
        v: int = self._vertices.index(second)
        self.add_edge_by_indices(u, v)

    # Find the vertex at a specific index
    def vertex_at(self, index: int) -> V:
        return self._vertices[index]

    # Find the index of a vertex in the graph
    def index_of(self, vertex: V) -> int:
        return self._vertices.index(vertex)

    # Find the vertices that a vertex at some index is connected to
    def neighbors_for_index(self, index: int) -> List[V]:
        return list(map(self.vertex_at, [e.v for e in self._edges[index]]))

    # Look up a vertice's index and find its neighbors (convenience method)
    def neighbors_for_vertex(self, vertex: V) -> List[V]:
        return self.neighbors_for_index(self.index_of(vertex))

    # Return all of the edges associated with a vertex at some index
    def edges_for_index(self, index: int) -> List[Edge]:
        return self._edges[index]

    # Look up the index of a vertex and return its edges (convenience method)
    def edges_for_vertex(self, vertex: V) -> List[Edge]:
        return self.edges_for_index(self.index_of(vertex))

    # Make it easy to pretty-print a Graph
    def __str__(self) -> str:
        desc: str = ""
        for i in range(self.vertex_count):
            desc += f"#{i}: {self.vertex_at(i)} -> {self.neighbors_for_index(i)}\n"
        return desc


def build_graph(
    vertices: List[V] = [], edges: List[Tuple[str, str]] = []
) -> Graph[str]:
    graph: Graph[str] = Graph(vertices=vertices)
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
    city_graph1 = build_graph(vertices, edges)
    print(city_graph1)

    # test graph's vertex removal
    print("-" * 100 + "\nTest removing vertex 'Miami'")
    _ = city_graph1.remove_vertex("Miami")
    print("after removal:")
    print(city_graph1)

    # 2. Test bfs
    print("-" * 100 + "\nTest BFS")
    city_graph2 = build_graph(vertices, edges)
    # Reuse BFS from chapter 2 on city_graph
    import sys

    sys.path.insert(
        0, ".."
    )  # so we can access the Chapter2 package in the parent directory
    from chapter2.generic_search import bfs, Node, node_to_path

    bfs_result: Optional[Node[V]]
    visited_states: int
    bfs_result, visited_states = bfs(
        "Phoenix", lambda x: x == "Washington", city_graph2.neighbors_for_vertex
    )
    if bfs_result is None:
        print("No solution found using breadth-first search!")
    else:
        path: List[V] = node_to_path(bfs_result)
        print("Path from Boston to Miami:")
        print(path)
        print("visited states: ", visited_states)

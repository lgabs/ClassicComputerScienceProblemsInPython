from typing import TypeVar, Generic, List, Optional
from edge import Edge
from graph import Graph

V = TypeVar("V")  # type of the vertices in the graph


class Graph2(Graph):
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


if __name__ == "__main__":
    # test basic Graph construction
    city_graph: Graph2 = Graph2(
        [
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
    )
    city_graph.add_edge_by_vertices("Seattle", "Chicago")
    city_graph.add_edge_by_vertices("Seattle", "San Francisco")
    city_graph.add_edge_by_vertices("San Francisco", "Riverside")
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles")
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside")
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Phoenix")
    city_graph.add_edge_by_vertices("Riverside", "Chicago")
    city_graph.add_edge_by_vertices("Phoenix", "Dallas")
    city_graph.add_edge_by_vertices("Phoenix", "Houston")
    city_graph.add_edge_by_vertices("Dallas", "Chicago")
    city_graph.add_edge_by_vertices("Dallas", "Atlanta")
    city_graph.add_edge_by_vertices("Dallas", "Houston")
    city_graph.add_edge_by_vertices("Houston", "Atlanta")
    city_graph.add_edge_by_vertices("Houston", "Miami")
    city_graph.add_edge_by_vertices("Atlanta", "Chicago")
    city_graph.add_edge_by_vertices("Atlanta", "Washington")
    city_graph.add_edge_by_vertices("Atlanta", "Miami")
    city_graph.add_edge_by_vertices("Miami", "Washington")
    city_graph.add_edge_by_vertices("Chicago", "Detroit")
    city_graph.add_edge_by_vertices("Detroit", "Boston")
    city_graph.add_edge_by_vertices("Detroit", "Washington")
    city_graph.add_edge_by_vertices("Detroit", "New York")
    city_graph.add_edge_by_vertices("Boston", "New York")
    city_graph.add_edge_by_vertices("New York", "Philadelphia")
    city_graph.add_edge_by_vertices("Philadelphia", "Washington")
    print(city_graph)

    print("removing vertex 'Miami':")
    _ = city_graph.remove_vertex("Miami")
    print("after removal:")
    print(city_graph)

from __future__ import annotations
from typing import TypeVar, List, Optional, Tuple, Dict
from dataclasses import dataclass

from exercise_2_mst import *

# from mst import WeightedPath, print_weighted_path
from weighted_edge import WeightedEdge
from priority_queue import PriorityQueue

from dijkstra import *

V = TypeVar("V")  # type of the vertices in the graph

if __name__ == "__main__":
    city_graph: WeightedDiGraph[str] = WeightedDiGraph(
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

    city_graph.add_edge_by_vertices("Seattle", "Chicago", 1737)
    city_graph.add_edge_by_vertices("Seattle", "San Francisco", 678)
    city_graph.add_edge_by_vertices("San Francisco", "Riverside", 386)
    city_graph.add_edge_by_vertices("San Francisco", "Los Angeles", 348)
    city_graph.add_edge_by_vertices("Los Angeles", "Riverside", 50)
    city_graph.add_edge_by_vertices("Los Angeles", "Phoenix", 357)
    city_graph.add_edge_by_vertices("Riverside", "Phoenix", 307)
    city_graph.add_edge_by_vertices("Riverside", "Chicago", 1704)
    city_graph.add_edge_by_vertices("Phoenix", "Dallas", 887)
    city_graph.add_edge_by_vertices("Phoenix", "Houston", 1015)
    city_graph.add_edge_by_vertices("Dallas", "Chicago", 805)
    city_graph.add_edge_by_vertices("Dallas", "Atlanta", 721)
    city_graph.add_edge_by_vertices("Dallas", "Houston", 225)
    city_graph.add_edge_by_vertices("Houston", "Atlanta", 702)
    city_graph.add_edge_by_vertices("Houston", "Miami", 968)
    city_graph.add_edge_by_vertices("Atlanta", "Chicago", 588)
    city_graph.add_edge_by_vertices("Atlanta", "Washington", 543)
    city_graph.add_edge_by_vertices("Atlanta", "Miami", 604)
    city_graph.add_edge_by_vertices("Miami", "Washington", 923)
    city_graph.add_edge_by_vertices("Chicago", "Detroit", 238)
    city_graph.add_edge_by_vertices("Detroit", "Boston", 613)
    city_graph.add_edge_by_vertices("Detroit", "Washington", 396)
    city_graph.add_edge_by_vertices("Detroit", "New York", 482)
    city_graph.add_edge_by_vertices("Boston", "New York", 190)
    city_graph.add_edge_by_vertices("New York", "Philadelphia", 81)
    city_graph.add_edge_by_vertices("Philadelphia", "Washington", 123)

    distances, path_dict = dijkstra(city_graph, "Los Angeles")
    name_distance: Dict[str, Optional[int]] = distance_array_to_vertex_dict(
        city_graph, distances
    )
    print("Distances from Los Angeles:")
    for key, value in name_distance.items():
        print(f"{key} : {value}")
    print("")  # blank line

    print("Shortest path from Los Angeles to Boston:")
    path: WeightedPath = path_dict_to_path(
        city_graph.index_of("Los Angeles"), city_graph.index_of("Boston"), path_dict
    )
    print_weighted_path(city_graph, path)

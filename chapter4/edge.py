from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Edge:
    """
    Edges do not store any vertex info other than their index.
    """

    u: int  # the "from" vertex
    v: int  # the "to" vertex

    def reversed(self) -> Edge:
        return Edge(self.v, self.u)

    def __str__(self) -> str:
        return f"{self.u} -> {self.v}"

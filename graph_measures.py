from heapq import nlargest
from operator import itemgetter
from statistics import mean
from typing import Union, Optional, Tuple, Any

import matplotlib.pyplot as plt
from networkx import Graph, DiGraph
from networkx import is_weighted, is_directed
from networkx import degree_assortativity_coefficient
from networkx import clustering, average_clustering
from networkx import number_connected_components, connected_components
from networkx import average_shortest_path_length, diameter, eccentricity
from networkx import global_efficiency
from networkx import closeness_centrality, betweenness_centrality

from networkx import draw
from networkx.algorithms import betweenness_centrality


class GraphMeasures:
    def __init__(self, graph: Graph):
        self.graph = graph

    @property
    def graph(self) -> Union[Graph, DiGraph]:
        return self._graph

    @graph.setter
    def graph(self, graph: Union[Graph, DiGraph]):
        self._graph = graph
        self._directed = is_directed(self._graph)
        self._weighted = is_weighted(self._graph)

    @property
    def directed(self) -> bool:
        return self._directed

    @property
    def weighted(self) -> bool:
        return self._weighted

    @property
    def node_count(self) -> int:
        return self.graph.number_of_nodes()

    @property
    def edge_count(self) -> Union[int, Tuple[int, int]]:
        if self.directed:
            return len(self.graph.in_edges)
        else:
            return self.graph.number_of_edges()

    @property
    def avg_edge_count(self) -> Union[float, Tuple[float, float]]:
        if self.directed:
            return (
                mean([degree[1] for degree in self.graph.in_degree()]),
                mean([degree[1] for degree in self.graph.out_degree()])
            )
        else:
            return mean([degree[1] for degree in self.graph.degree()])

    @property
    def avg_strength(self) -> Union[float, Tuple[float, float]]:
        if self.weighted:
            if self.directed:
                return \
                    (mean(degree for degree in dict(self.graph.in_degree(weight='weight')).values()),
                     mean(degree for degree in dict(self.graph.out_degree(weight='weight')).values()))
            else:
                return mean(degree for degree in dict(self.graph.degree(weight='weight')).values())
        else:
            raise ValueError('Unweighted graphs cannot have strength.')

    @property
    def component_count(self) -> int:
        return number_connected_components(self.graph)

    @property
    def largest_component_properties(self) -> Tuple[int, int]:
        largest_component: Graph = max(connected_components(self.graph), key=len, reverse=True)
        return largest_component.number_of_nodes(), largest_component.number_of_edges()

    @property
    def shortest_path_length(self):
        return average_shortest_path_length(self.graph)

    @property
    def diameter(self) -> int:
        return diameter(self.graph)

    @property
    def eccentricity(self) -> dict:
        return eccentricity(self.graph)

    @property
    def global_efficiency(self) -> Optional[float]:
        if not self.directed:
            return global_efficiency(self.graph)
        else:
            return None

    @property
    def global_clustering_coefficient(self) -> float:
        return clustering(self.graph)

    @property
    def avg_clustering_coefficient(self) -> float:
        return average_clustering(self.graph)

    @property
    def degree_assortativity(self) -> float:
        return degree_assortativity_coefficient(self.graph)

    def draw_degree_distribution_diagram(self):
        args = []
        kwargs = {}
        if self.directed:
            if self.weighted:
                pass
        draw(self.graph, *args, **kwargs)
        plt.savefig(f"{self.graph.name}.png", format='PNG')


    @property
    def top10_central_degree(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        return nlargest(10, self.graph.degree, key=itemgetter(1))

    @property
    def top10_central_betweenness(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        bc = betweenness_centrality(self.graph)
        return nlargest(10, bc.keys(), key=itemgetter)

    @property
    def top10_central_closeness(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        pass

    @property
    def top10_central_table(self) -> str:
        pass

    @property
    def avg_closeness_centrality(self):
        pass

    @property
    def avg_betweenness_centrality(self):
        pass




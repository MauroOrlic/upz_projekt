from collections import Counter
from heapq import nlargest
from operator import itemgetter
from statistics import mean
from typing import Union, Tuple, Any, Dict

from networkx import Graph, DiGraph
from networkx import average_shortest_path_length, diameter, eccentricity
from networkx import closeness_centrality, betweenness_centrality, degree_centrality
from networkx import degree_assortativity_coefficient
from networkx import global_efficiency
from networkx import is_weighted, is_directed, is_connected, is_weakly_connected
from networkx import \
    number_connected_components, connected_components, \
    number_strongly_connected_components, strongly_connected_components, weakly_connected_components
from networkx import transitivity, average_clustering

from networkx import all_pairs_shortest_path_length


def global_efficiency_directional(graph: Union[DiGraph, Graph]):
    # Identical to original, however without raising NetworkxNotImplementedError
    # when passed directional graphs. No idea why original author blocked it
    # even though it appears to work.
    n = len(graph)
    denom = n * (n - 1)
    if denom != 0:
        lengths = all_pairs_shortest_path_length(graph)
        g_eff = 0
        for source, targets in lengths:
            for target, distance in targets.items():
                if distance > 0:
                    g_eff += 1 / distance
        g_eff /= denom
    else:
        g_eff = 0
    return g_eff


class MeasureError(AttributeError):
    pass


class GraphMeasures:
    def __init__(self, graph: Graph):
        self._graph = graph
        self._directed = None
        self._weighted = None
        self._connected = None
        self._weakly_connected = None
        self._strongly_connected = None

        self._node_count = None
        self._edge_count = None
        self._avg_edge_count = None
        self._avg_strength = None
        self._component_count = None
        self._largest_component_measures = None
        self._shortest_path_length = None
        self._diameter = None
        self._eccentricity = None
        self._global_efficiency = None
        self._global_clustering_coefficient = None
        self._avg_clustering_coefficient = None
        self._degree_assortativity = None
        self._degree_distribution = None
        self._top10_central_degree = None
        self._top10_central_betweenness = None
        self._top10_central_closeness = None
        self._avg_closeness_centrality = None
        self._avg_betweenness_centrality = None

    @property
    def graph(self) -> Union[Graph, DiGraph]:
        return self._graph

    @property
    def directed(self) -> bool:
        if self._directed is None:
            self._directed = is_directed(self.graph)

        return self._directed

    @property
    def weighted(self) -> bool:
        if self._weighted is None:
            self._weighted = is_weighted(self.graph)

        return self._weighted

    @property
    def connected(self) -> bool:
        if self._connected is None:
            if not self.directed:
                self._connected = is_connected(self.graph)
            else:
                raise MeasureError('Directed graphs cannot be plainly connected, '
                                   'use \'weakly_connected\' or \'strongly_connected\' instead.')
        return self._connected

    @property
    def weakly_connected(self) -> bool:
        if self._weakly_connected is None:
            if self.directed:
                self._weakly_connected = is_weakly_connected(self.graph)
            else:
                raise MeasureError('Undirected graphs cannot be weakly connected, '
                                   'use \'connected\' instead.')

        return self._weakly_connected

    @property
    def strongly_connected(self) -> bool:
        if self._strongly_connected is None:
            if self.directed:
                self._strongly_connected = is_weakly_connected(self.graph)
            else:
                raise MeasureError('Undirected graphs cannot be strongly connected, '
                                   'use \'connected\' instead.')

        return self._strongly_connected

    @property
    def node_count(self) -> int:
        if self._node_count is None:
            self._node_count = self.graph.number_of_nodes()
        return self._node_count

    @property
    def edge_count(self) -> Union[int, Tuple[int, int]]:
        if self._edge_count is None:
            if self.directed:
                self._edge_count = len(self.graph.in_edges)
            else:
                self._edge_count = self.graph.number_of_edges()

        return self._edge_count

    @property
    def avg_edge_count(self) -> Union[float, Tuple[float, float]]:
        if self._avg_edge_count is None:
            if self.directed:
                self._avg_edge_count = (
                    mean([degree[1] for degree in self.graph.in_degree()]),
                    mean([degree[1] for degree in self.graph.out_degree()])
                )
            else:
                self._avg_edge_count = mean([degree[1] for degree in self.graph.degree()])

        return self._avg_edge_count

    @property
    def avg_strength(self) -> Union[float, Tuple[float, float]]:
        if self._avg_strength is None:
            if self.weighted:
                if self.directed:
                    self._avg_strength = \
                        (mean(degree for degree in dict(self.graph.in_degree(weight='weight')).values()),
                         mean(degree for degree in dict(self.graph.out_degree(weight='weight')).values()))
                else:
                    self._avg_strength = mean(degree for degree in dict(self.graph.degree(weight='weight')).values())
            else:
                raise MeasureError('Unweighted graphs cannot have strength.')
        return self._avg_strength

    @property
    def component_count(self) -> int:
        if self._component_count is None:
            if self.directed:
                self._component_count = number_strongly_connected_components(self.graph)
            else:
                self._component_count = number_connected_components(self.graph)

        return self._component_count

    @property
    def largest_component_measures(self) -> 'GraphMeasures':
        if self._largest_component_measures is None:
            if self.directed:
                if self.strongly_connected:
                    return self

                largest_component: DiGraph = self.graph.subgraph(
                    max(strongly_connected_components(self.graph), key=len)
                ).copy()
            else:
                if self.connected:
                    return self
                largest_component: Graph = self.graph.subgraph(
                    max(connected_components(self.graph), key=len)
                ).copy()

            self._largest_component_measures = GraphMeasures(largest_component)

        return self._largest_component_measures

    @property
    def shortest_path_length(self):
        if self._shortest_path_length is None:
            if self.directed:
                largest_component: DiGraph = self.graph.subgraph(
                    max(weakly_connected_components(self.graph), key=len)
                ).copy()
            else:
                largest_component: Graph = self.graph.subgraph(
                    max(connected_components(self.graph), key=len)
                ).copy()
            self._shortest_path_length = average_shortest_path_length(largest_component)

        return self._shortest_path_length

    @property
    def diameter(self) -> int:
        if self._diameter is None:
            if self.directed:
                largest_component: DiGraph = self.graph.subgraph(
                    max(strongly_connected_components(self.graph), key=len)
                ).copy()
            else:
                largest_component: Graph = self.graph.subgraph(
                    max(connected_components(self.graph), key=len)
                ).copy()
            self._diameter = diameter(largest_component)

        return self._diameter

    @property
    def eccentricity(self) -> Union[int, float]:
        if self._eccentricity is None:
            if self.directed:
                largest_component: DiGraph = self.graph.subgraph(
                    max(strongly_connected_components(self.graph), key=len)
                ).copy()
            else:
                largest_component: Graph = self.graph.subgraph(
                    max(connected_components(self.graph), key=len)
                ).copy()

            self._eccentricity = max(eccentricity(largest_component).values())

        return self._eccentricity

    @property
    def global_efficiency(self) -> float:
        if self._global_efficiency is None:
            if self.directed:
                self._global_efficiency = global_efficiency_directional(self.graph)
            else:
                self._global_efficiency = global_efficiency(self.graph)

        return self._global_efficiency

    @property
    def global_clustering_coefficient(self) -> float:
        if self._global_clustering_coefficient is None:
            self._global_clustering_coefficient = transitivity(self.graph)

        return self._global_clustering_coefficient

    @property
    def avg_clustering_coefficient(self) -> float:
        if self._avg_clustering_coefficient is None:
            self._avg_clustering_coefficient = average_clustering(self.graph)

        return self._avg_clustering_coefficient

    @property
    def degree_assortativity(self) -> float:
        if self._degree_assortativity is None:
            self._degree_assortativity = degree_assortativity_coefficient(self.graph)

        return self._degree_assortativity

    @property
    def degree_distribution(self) -> Union[Dict[int, int], Tuple[Dict[int, int], Dict[int, int]]]:
        if self._degree_distribution is None:
            if self.directed:
                distribution = (
                    dict(Counter(sorted([degree for node, degree in self.graph.in_degree()]))),
                    dict(Counter(sorted([degree for node, degree in self.graph.out_degree()])))
                )
            else:
                distribution = \
                    dict(Counter(sorted([degree for node, degree in self.graph.degree()])))

            self._degree_distribution = distribution

        return self._degree_distribution

    @property
    def top10_central_degree(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        if self._top10_central_degree is None:
            dc = degree_centrality(self.graph)
            self._top10_central_degree = nlargest(10, dc.items(), key=itemgetter(1))

        return self._top10_central_degree

    @property
    def top10_central_betweenness(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        if self._top10_central_betweenness is None:
            bc = betweenness_centrality(self.graph)
            self._top10_central_betweenness = nlargest(10, bc.items(), key=itemgetter(1))

        return self._top10_central_betweenness

    @property
    def top10_central_closeness(self) -> Tuple[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]:
        if self._top10_central_closeness is None:
            cc = closeness_centrality(self.graph)
            self._top10_central_closeness = nlargest(10, cc.items(), key=itemgetter(1))

        return self._top10_central_closeness

    @property
    def avg_closeness_centrality(self) -> float:
        if self._avg_closeness_centrality is None:
            self._avg_closeness_centrality = mean([centrality for centrality in closeness_centrality(self.graph).values()])

        return self._avg_closeness_centrality

    @property
    def avg_betweenness_centrality(self):
        if self._avg_betweenness_centrality is None:
            self._avg_betweenness_centrality = mean([centrality for centrality in betweenness_centrality(self.graph).values()])

        return self._avg_betweenness_centrality




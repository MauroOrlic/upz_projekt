from pathlib import Path
from mtx import read_mtx, read_edges
from networkx import Graph, DiGraph, \
    write_graphml, read_graphml, \
    is_weighted, \
    average_shortest_path_length, density, diameter, eccentricity, clustering, degree_assortativity_coefficient, number_connected_components, connected_components
from typing import Union, Optional, Tuple
from statistics import mean


def load_raw(path: Path) -> Union[Graph, DiGraph]:
    '''
    graph = Graph(name=path.stem)
    with path.open('r') as file:
        for line in file:
            if line[0] != '%':
                line = line.rstrip()
                items = line.split(' ')
                if len(items) == 3:
                    graph.add_edge(int(items[0]), int(items[1]), weight=float(items[2]))
                else:
                    graph.add_edge(int(items[0]), int(items[1]))
    return graph
    '''
    if path.suffix == '.mtx':
        graph = read_mtx(path.as_posix())
    elif path.suffix == '.edges':
        graph = read_edges(path.as_posix(), comments='%')
    else:
        raise ValueError("Usupported format.")
    graph.name = path.stem
    return graph


def dump_graphml(graph: Graph, path: Path):
    path = Path(path.parent / path.stem).with_suffix('.graphml')
    with path.open('wb') as file:
        write_graphml(graph, file)


def load_graphml(path: Path) -> Graph:
    with path.open('r') as file:
        return read_graphml(file)


class GraphMeasures:
    def __init__(self, graph: Graph):
        self.graph = graph

    @property
    def graph(self) -> Union[Graph, DiGraph]:
        return self._graph

    @graph.setter
    def graph(self, graph: Union[Graph, DiGraph]):
        self._graph = graph
        self._directed = self._graph.is_directed()
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
    def connection_count(self) -> Union[int, Tuple[int, int]]:
        if self.directed:
            return len(self.graph.in_edges)
        else:
            return self.graph.number_of_edges()

    @property
    def avg_connection_count(self) -> Union[float, Tuple[float, float]]:
        if self.directed:
            return \
                (mean(degree for degree in self.graph.in_degree.values()),
                 mean(degree for degree in self.graph.out_degree.values()))
        else:
            return mean(self.graph.degree.values())

    @property
    def avg_strength(self) -> Optional[Union[float, Tuple[float, float]]]:
        if self.weighted:
            if self.directed:
                return \
                    (mean(degree for degree in self.graph.in_degree(weight='weight').values()),
                     mean(degree for degree in self.graph.out_degree(weight='weight').values()))
            else:
                return mean(self.graph.degree(weight='weight').values())

    @property
    def component_count(self) -> int:
        return number_connected_components(self.graph)

    @property
    def largest_component(self) -> Tuple[int, int]:
        largest_component: Graph = max(connected_components(self.graph), key=len, reverse=True)
        return largest_component.number_of_nodes(), largest_component.number_of_edges()

    @property
    def shortest_path_lenght(self):
        return average_shortest_path_length(self.graph)

    @property
    def diameter(self) -> int:
        return diameter(self.graph)

    @property
    def eccentricity(self) -> dict:
        return eccentricity(self.graph)

    @property
    def global_efficiency(self):
        pass

    @property
    def global_grouping_coefficient(self):
        pass

    @property
    def avg_grouping_coefficient(self):
        pass

    @property
    def assortativity(self):
        pass

    @property
    def degree_distribution_diagram(self):
        if self.directed:
            if self.weighted:
                pass

    @property
    def top_10_degree_central(self):
        pass

    @property
    def top_10_betweenness_central(self):
        pass

    @property
    def top_10_closeness_central(self):
        pass

    @property
    def avg_closeness_centrality(self):
        pass

    @property
    def avg_betweenness_centrality(self):
        pass




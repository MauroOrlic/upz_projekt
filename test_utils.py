from pathlib import Path
from utils import load_raw, load_graphml, dump_graphml, GraphMeasures
import pytest
from networkx import is_weighted, is_isomorphic, Graph, is_directed
from math import isclose


class TestGraphIO:

    def test_load_openflights(self):
        path = Path('raw_data/inf-openflights.edges')
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is True

    def test_load_power(self):
        path = Path('raw_data/inf-power.mtx')
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False

    def test_load_roadnet_ca(self):
        path = Path('raw_data/inf-roadNet-CA.mtx')
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False
        assert graph.has_edge('418', '5')
        assert graph.has_edge('108', '13')
        assert graph.has_edge('3248', '19')
        assert graph.has_edge('108', '8') is False
        assert graph.has_edge('16', '14') is False

    def test_load_roadnet_pa(self):
        path = Path('raw_data/inf-roadNet-PA.mtx')
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False
        pass

    def test_load_usair97(self):
        path = Path('raw_data/inf-USAir97.mtx')
        graph = load_raw(path)
        assert is_weighted(graph) is True
        assert is_directed(graph) is False
        assert graph['2']['1']['weight'] == 0.0436
        assert graph['13']['6']['weight'] == 0.0143
        assert graph['144']['8']['weight'] == 0.2746
        assert graph['119']['95']['weight'] == 0.0323
        assert graph.has_edge('321', '163') is False
        assert graph.has_edge('230', '168') is False


class TestGraphProperties:

    @pytest.mark.parametrize('graph_path, expected', [
        ('./processed_data/inf-openflights.graphml', 2.9e3),
        ('./processed_data/inf-power.graphml', 4.9e3),
        ('./processed_data/inf-roadNet-CA.graphml', 2e6),
        ('./processed_data/inf-roadNet-PA.graphml', 1.1e6),
        ('./processed_data/inf-USAir97.graphml', 332)
    ])
    def test_node_count(self, graph_path: str, expected: int):
        measures = GraphMeasures(load_graphml(Path(graph_path)))
        assert isclose(measures.node_count, expected, rel_tol=0.15)

    @pytest.mark.parametrize('graph_path, expected', [
        ('./processed_data/inf-openflights.graphml', 30.5e3),
        ('./processed_data/inf-power.graphml', 6.6e3),
        ('./processed_data/inf-roadNet-CA.graphml', 2.8e6),
        ('./processed_data/inf-roadNet-PA.graphml', 1.5e6),
        ('./processed_data/inf-USAir97.graphml', 2.1e3)
    ])
    def test_edge_count(self, graph_path: str, expected: int):
        measures = GraphMeasures(load_graphml(Path(graph_path)))
        assert isclose(measures.connection_count, expected, rel_tol=0.15)

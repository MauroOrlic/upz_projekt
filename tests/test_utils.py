from networkx import is_weighted, is_directed

from paths import raw_openflights, raw_power, raw_roadnet_ca, \
    raw_roadnet_pa, raw_usair97, processed_openflights, \
    processed_power, processed_roadmap_pa, processed_roadnet_ca, \
    processed_usair97
from utils import load_raw, dump_graphml


class TestGraphIO:

    def test_load_openflights(self):
        path = raw_openflights
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is True
        assert graph.has_edge('2', '4')
        assert graph.has_edge('4', '2')
        assert graph.has_edge('482', '61')
        assert graph.has_edge('592', '308')
        assert graph.has_edge('551', '375')
        assert graph.has_edge('375', '551') is False
        dump_graphml(graph, processed_openflights)

    def test_load_power(self):
        path = raw_power
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False
        assert graph.has_edge('387', '1')
        assert graph.has_edge('1813', '1308')
        assert graph.has_edge('1517', '1440')
        assert graph.has_edge('1527', '1440')
        assert graph.has_edge('4599', '4580')
        assert graph.has_edge('3797', '4724') is False
        assert graph.has_edge('2475', '1070') is False
        assert graph.has_edge('420', '425') is False
        assert graph.has_edge('465', '4576') is False
        dump_graphml(graph, processed_power)

    def test_load_roadnet_ca(self):
        path = raw_roadnet_ca
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False
        assert graph.has_edge('418', '5')
        assert graph.has_edge('108', '13')
        assert graph.has_edge('3248', '19')
        assert graph.has_edge('108', '8') is False
        assert graph.has_edge('16', '14') is False
        dump_graphml(graph, processed_roadnet_ca)

    def test_load_roadnet_pa(self):
        path = raw_roadnet_pa
        graph = load_raw(path)
        assert is_weighted(graph) is False
        assert is_directed(graph) is False
        assert graph.has_edge('6299', '1')
        assert graph.has_edge('1', '6299')
        assert graph.has_edge('98292', '98290')
        assert graph.has_edge('450790', '450673')
        assert graph.has_edge('1068204', '592388')
        assert graph.has_edge('783720', '733101') is False
        assert graph.has_edge('290980', '168570') is False
        assert graph.has_edge('98260', '98318') is False
        dump_graphml(graph, processed_roadmap_pa)

    def test_load_usair97(self):
        path = raw_usair97
        graph = load_raw(path)
        assert is_weighted(graph) is True
        assert is_directed(graph) is False
        assert graph['2']['1']['weight'] == 0.0436
        assert graph['13']['6']['weight'] == 0.0143
        assert graph['144']['8']['weight'] == 0.2746
        assert graph['119']['95']['weight'] == 0.0323
        assert graph.has_edge('321', '163') is False
        assert graph.has_edge('230', '168') is False
        dump_graphml(graph, processed_usair97)

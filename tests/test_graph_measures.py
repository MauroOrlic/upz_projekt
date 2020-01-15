from math import trunc, isclose
from operator import le, ge
from pathlib import Path
from typing import Any, Collection

import pytest

from graph_measures import GraphMeasures, MeasureError
from paths import processed_openflights, processed_power, \
    processed_roadmap_pa, processed_roadnet_ca, \
    processed_usair97
from utils import load_graphml

ids = [
    'openflights',
    'power',
    'roadnet_ca',
    'roadmap_pa',
    'usair97',
]


def issorted(collection: Collection, reverse=False) -> bool:
    length = len(collection)
    if length == 1:
        return True

    nxt = None
    prv = None

    comparison = le if reverse else ge
    for item in collection:
        if nxt is None:
            nxt = item
            continue
        prv = nxt
        nxt = item
        if comparison(prv, nxt):
            return False

    return True


class TestGraphProperties:
    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)

    ], ids=ids)
    def test_basic_measures(self, graph_path: Path, expected: Any):
        measure = GraphMeasures(load_graphml(graph_path))
        if measure.directed:
            measure.strongly_connected
            measure.weakly_connected
            with pytest.raises(MeasureError):
                measure.connected
        else:
            measure.connected
            with pytest.raises(MeasureError):
                measure.weakly_connected
            with pytest.raises(MeasureError):
                measure.strongly_connected

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 2.9e3),
        (processed_power, 4.9e3),
        (processed_roadnet_ca, 2e6),
        (processed_roadmap_pa, 1.1e6),
        (processed_usair97, 332)
    ], ids=ids)
    def test_node_count(self, graph_path: Path, expected: int):
        measure = GraphMeasures(load_graphml(graph_path))
        assert isclose(measure.node_count, expected, rel_tol=0.1)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 30.5e3),
        (processed_power, 6.6e3),
        (processed_roadnet_ca, 2.8e6),
        (processed_roadmap_pa, 1.5e6),
        (processed_usair97, 2.1e3)
    ], ids=ids)
    def test_edge_count(self, graph_path: Path, expected: int):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.edge_count, expected, rel_tol=0.1)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 20),
        (processed_power, 2),
        (processed_roadnet_ca, 2),
        (processed_roadmap_pa, 2),
        (processed_usair97, 12)

    ], ids=ids)
    def test_avg_edge_count(self, graph_path: Path, expected: Any):
        measures = GraphMeasures(load_graphml(graph_path))
        if measures.directed:
            assert trunc(sum(measures.avg_edge_count)) == expected
        else:
            assert trunc(measures.avg_edge_count) == expected

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)

    ], ids=ids)
    def test_avg_strength(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        if measures.weighted:
            if measures.directed:
                avg_strength_in, avg_strength_out = measures.avg_strength
                assert isinstance(avg_strength_in, float)
                assert isinstance(avg_strength_out, float)
            else:
                assert isinstance(measures.avg_strength, float)
        else:
            with pytest.raises(MeasureError):
                measures.avg_strength

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_component_count(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.component_count, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_largest_component_measures(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.largest_component_measures.node_count, int)
        assert isinstance(measures.largest_component_measures.edge_count, int)
        if measures.largest_component_measures.directed:
            assert measures.largest_component_measures.strongly_connected
        else:
            assert measures.largest_component_measures.connected

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_shortest_path_length(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.shortest_path_length, (int, float))

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_diameter(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.diameter, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_eccentricity(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.eccentricity, (int, float))

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_global_efficiency(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.global_efficiency, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.254926),
        (processed_power, 0.103153),
        (processed_roadnet_ca, 0.0603595),
        (processed_roadmap_pa, 0.0593855),
        (processed_usair97, 0.396392)
    ], ids=ids)
    def test_global_clustering_coefficient(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.global_clustering_coefficient, expected, rel_tol=0.15)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.396761),
        (processed_power, 0.0801036),
        (processed_roadnet_ca, 0.0464684),
        (processed_roadmap_pa, 0.046463),
        (processed_usair97, 0.625217)
    ], ids=ids)
    def test_avg_clustering_coefficient(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.avg_clustering_coefficient, expected, rel_tol=0.15)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.00706468),
        (processed_power, 0.000540303),
        (processed_roadnet_ca, 1.44147e-06),
        (processed_roadmap_pa, 2.60657e-06),
        (processed_usair97, 0.0386925)

    ], ids=ids)
    def test_degree_assortativity(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.degree_assortativity, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_degree_distribution(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        if measures.directed:
            assert isinstance(measures.degree_distribution, tuple)
            assert len(measures.degree_distribution) == 2
            assert isinstance(measures.degree_distribution[1], dict)
            for distribution in measures.degree_distribution:
                assert isinstance(distribution, dict)
                for degree, count in distribution.items():
                    assert isinstance(degree, int)
                    assert isinstance(count, int)
                assert issorted(list(distribution.keys()))
        else:
            assert isinstance(measures.degree_distribution, dict)
            for degree, count in measures.degree_distribution.items():
                assert isinstance(degree, int)
                assert isinstance(count, int)
            assert issorted(measures.degree_distribution.keys())

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_top10_central_degree(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        dc = measures.top10_central_degree
        assert len(dc) == 10
        for item in dc:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[1], float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_top10_central_betweenness(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        bc = measures.top10_central_betweenness
        assert len(bc) == 10
        for item in bc:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[1], float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_top10_central_closeness(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        cc = measures.top10_central_closeness
        assert len(cc) == 10
        for item in cc:
            assert isinstance(item, tuple)
            assert len(item) == 2
            assert isinstance(item[1], float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_avg_closeness_centrality(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.avg_closeness_centrality, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ], ids=ids)
    def test_avg_betweenness_centrality(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.avg_betweenness_centrality, float)

from math import trunc, isclose
from pathlib import Path
from typing import Any

import pytest

from graph_measures import GraphMeasures
from paths import processed_openflights, processed_power, \
    processed_roadmap_pa, processed_roadnet_ca, \
    processed_usair97
from utils import load_graphml


class TestGraphProperties:

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 2.9e3),
        (processed_power, 4.9e3),
        (processed_roadnet_ca, 2e6),
        (processed_roadmap_pa, 1.1e6),
        (processed_usair97, 332)
    ])
    def test_node_count(self, graph_path: Path, expected: int):
        measure = GraphMeasures(load_graphml(graph_path))
        assert isclose(measure.node_count, expected, rel_tol=0.1)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 30.5e3),
        (processed_power, 6.6e3),
        (processed_roadnet_ca, 2.8e6),
        (processed_roadmap_pa, 1.5e6),
        (processed_usair97, 2.1e3)
    ])
    def test_edge_count(self, graph_path: Path, expected: int):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.edge_count, expected, rel_tol=0.1)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 20),
        (processed_power, 2),
        (processed_roadnet_ca, 2),
        (processed_roadmap_pa, 2),
        (processed_usair97, 12)

    ])
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

    ])
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
            with pytest.raises(ValueError):
                measures.avg_strength

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_component_count(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.component_count, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_largest_component_properties(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        node_count, edge_count = measures.largest_component_properties
        assert isinstance(node_count, int)
        assert isinstance(edge_count, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_shortest_path_length(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.shortest_path_length, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_diameter(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.diameter, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_eccentricity(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.eccentricity, int)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_global_efficiency(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        if measures.directed:
            with pytest.raises(NotImplementedError):
                measures.global_efficiency
        else:
            assert isinstance(measures.global_efficiency, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.254926),
        (processed_power, 0.103153),
        (processed_roadnet_ca, 0.0603595),
        (processed_roadmap_pa, 0.0593855),
        (processed_usair97, 0.396392)
    ])
    def test_global_clustering_coefficient(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.avg_clustering_coefficient, expected, rel_tol=0.12)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.396761),
        (processed_power, 0.0801036),
        (processed_roadnet_ca, 0.0464684),
        (processed_roadmap_pa, 0.046463),
        (processed_usair97, 0.625217)
    ])
    def test_avg_clustering_coefficient(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isclose(measures.avg_clustering_coefficient, expected, rel_tol=0.12)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, 0.00706468),
        (processed_power, 0.000540303),
        (processed_roadnet_ca, 1.44147e-06),
        (processed_roadmap_pa, 2.60657e-06),
        (processed_usair97, 0.0386925)

    ])
    def test_assortativity(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.degree_assortativity, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_draw_degree_distribution_diagram(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_top10_central_degree(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_top10_central_betweenness(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert len(measures.top10_central_betweenness) == 10

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_top10_central_closeness(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert len(measures.top10_central_closeness) == 10

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_top10_central_table(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.top10_central_table, str)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_avg_closeness_centrality(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.avg_closeness_centrality, float)

    @pytest.mark.parametrize('graph_path, expected', [
        (processed_openflights, None),
        (processed_power, None),
        (processed_roadnet_ca, None),
        (processed_roadmap_pa, None),
        (processed_usair97, None)
    ])
    def test_avg_betweenness_centrality(self, graph_path: Path, expected):
        measures = GraphMeasures(load_graphml(graph_path))
        assert isinstance(measures.avg_betweenness_centrality, float)

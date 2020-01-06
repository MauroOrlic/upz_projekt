from pathlib import Path
from utils import load
import pytest
from networkx import is_weighted


def test_load_roadnetca():
    path = Path('data/inf-roadNet-CA/inf-roadNet-CA.mtx')
    graph = load(path)
    assert is_weighted(graph) is False
    assert graph.has_edge(418, 5)
    assert graph.has_edge(108, 13)
    assert graph.has_edge(3248, 19)
    assert not graph.has_edge(108, 8)
    assert not graph.has_edge(16, 14)


def test_load_usair97():
    path = Path('data/inf-USAir97/inf-USAir97.mtx')
    graph = load(path)
    assert is_weighted(graph) is True
    assert graph[2][1]['weight'] == 0.0436
    assert graph[13][6]['weight'] == 0.0143
    assert graph[144][8]['weight'] == 0.2746
    assert graph[119][95]['weight'] == 0.0323
    assert not graph.has_edge(321, 163)
    assert not graph.has_edge(230, 168)


@pytest.mark.parametrize('path,expected', [
    (Path('data/inf-power/inf-power.mtx'), False),
    (Path('data/inf-openflights/inf-openflights.edges'), False),
    (Path('data/inf-roadNet-CA/inf-roadNet-CA.mtx'), False),
    (Path('data/inf-roadNet-PA/inf-roadNet-PA.mtx'), False),
    (Path('data/inf-USAir97/inf-USAir97.mtx'), True),
    ])
def test_load_plain(path, expected):
    graph = load(path)
    assert is_weighted(graph) is expected

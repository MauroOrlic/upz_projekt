from pathlib import Path
from typing import Union

from networkx import Graph, DiGraph
from networkx import read_graphml, write_graphml

from readers.matrix_market import read_mtx
from readers.edges import read_edges


def load_raw(path: Path) -> Union[Graph, DiGraph]:
    if path.suffix == '.mtx':
        graph = read_mtx(path.as_posix())
    elif path.suffix == '.edges':
        graph = read_edges(path.as_posix(), comments='%')
    else:
        raise ValueError("Usupported format.")
    graph.name = path.stem
    return graph


def dump_graphml(graph: Graph, path: Path):
    with path.open('wb') as file:
        write_graphml(graph, file)


def load_graphml(path: Path) -> Graph:
    with path.open('r') as file:
        return read_graphml(file)



from pathlib import Path
from networkx import Graph


def load(path: Path) -> Graph:
    graph = Graph()
    with open(path.as_posix()) as file:
        for line in file:
            if line[0] != '%':
                line = line.rstrip()
                items = line.split(' ')
                if len(items) == 3:
                    graph.add_edge(int(items[0]), int(items[1]), weight=float(items[2]))
                else:
                    graph.add_edge(int(items[0]), int(items[1]))
    return graph

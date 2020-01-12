from __future__ import annotations

from typing import Union, Tuple

from networkx import Graph, DiGraph
from networkx import read_edgelist


def read_edges(path: str, comments='%', delimiter=None,
               nodetype=None, encoding='utf-8') -> Union[Graph, DiGraph]:
    reader = EdgesReader(comments=comments, delimiter=delimiter,
                         node_type=nodetype, encoding=encoding)
    return reader(path)


class EdgesReader:
    EDGES_UNDIRECTED = 'sym'
    EDGES_DIRECTED = 'asym'
    EDGES_BIPARTITE = 'bip'
    VALID_EDGES = (EDGES_UNDIRECTED, EDGES_DIRECTED, EDGES_BIPARTITE)
    WEIGHT_UNWEIGHTED = 'unweighted'
    WEIGHT_POSITIVE = 'positive'
    WEIGHT_POSWEIGHTED = 'posweighted'
    WEIGHT_SIGNED = 'signed'
    WEIGHT_MULTISIGNED = 'multisigned'
    WEIGHT_WEIGHTED = 'weighted'
    WEIGHT_MULTIWEIGHTED = 'multiweighted'
    WEIGHT_DYNAMIC = 'dynamic'
    WEIGHT_MULTIPOSWEIGHTED = 'multiposweighted'
    VALID_WEIGHT = (WEIGHT_UNWEIGHTED, WEIGHT_POSITIVE, WEIGHT_POSWEIGHTED,
                    WEIGHT_SIGNED, WEIGHT_MULTISIGNED, WEIGHT_WEIGHTED,
                    WEIGHT_MULTIWEIGHTED, WEIGHT_DYNAMIC, WEIGHT_MULTIPOSWEIGHTED)

    def __init__(self, comments='#', delimiter=None,
                 node_type=None, edge_key_type=None, encoding='utf-8'):
        self._comments = comments
        self._delimiter = delimiter
        self._node_type = node_type
        self._encoding = encoding
        self._edge_key_type = edge_key_type

    @property
    def comments(self):
        return self._comments

    @property
    def delimiter(self):
        return self._delimiter

    @property
    def node_type(self):
        return self._node_type

    @property
    def encoding(self):
        return self._encoding

    @property
    def edge_key_type(self):
        return self._edge_key_type

    def __call__(self, path: str) -> Union[Graph, DiGraph]:
        header, info = self.get_metadata(path)

        edges, weight = self.parse_header(header)
        edge_count, subject_count, object_count = self.parse_info(info)

        if edges in (self.EDGES_UNDIRECTED, self.EDGES_BIPARTITE):
            create_using = Graph
        elif edges in (self.EDGES_DIRECTED,):
            create_using = DiGraph
        else:
            raise ValueError(f"Invalid edges type '{edges}'")

        if weight in (self.WEIGHT_POSWEIGHTED, self.WEIGHT_SIGNED,
                      self.WEIGHT_MULTISIGNED, self.WEIGHT_WEIGHTED,
                      self.WEIGHT_MULTIWEIGHTED, self.WEIGHT_MULTIPOSWEIGHTED):
            data = (('weight', float),)
        elif weight in (self.WEIGHT_UNWEIGHTED, self.WEIGHT_POSITIVE,
                        self.WEIGHT_DYNAMIC):
            data = True
        else:
            raise ValueError(f"Invalid weight type '{weight}'")

        return read_edgelist(
            path,
            comments=self.comments,
            delimiter=self.delimiter,
            create_using=create_using,
            nodetype=self.node_type,
            data=data,
            edgetype=self.edge_key_type,
            encoding=self.encoding
        )

    @staticmethod
    def get_metadata(path: str) -> Tuple[str, str]:
        with open(path, 'r') as file:
            header = file.readline()
            info = file.readline()
        return header, info

    def parse_header(self, header: str) -> Tuple[str, str]:
        if not header.startswith(self.comments):
            raise ValueError(f"Invalid header format: {header}")
        header = header.lstrip(self.comments)
        params = header.split()
        if not len(params) == 2:
            raise ValueError(f"Invalid number of parameters: {len(params)}")
        if params[0] not in self.VALID_EDGES:
            raise ValueError(f"Invalid edge type '{params[0]}'.")
        if params[1] not in self.VALID_WEIGHT:
            raise ValueError(f"Invalid weight type '{params[1]}'")
        edges = params[0]
        weight = params[1]
        return edges, weight

    def parse_info(self, info: str) -> Tuple[int, int, int]:
        if not info.startswith(self.comments):
            raise ValueError(f"Invalid info format: {info}")
        info = info.lstrip(self.comments)
        params = info.split()
        if not len(params) == 3:
            raise ValueError(f"Invalid number of parameters: {len(params)}")
        edge_count, subject_count, object_count = map(int, params)
        return edge_count, subject_count, object_count

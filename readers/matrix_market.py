from __future__ import annotations

from io import TextIOBase
from typing import List, Union, Tuple, Type

from networkx import NetworkXError, Graph, DiGraph


def read_mtx(path: str, node_type=str, edge_key_type=int) -> Union[Graph, DiGraph]:
    reader = MatrixMarketReader(
        node_type=node_type,
        edge_key_type=edge_key_type
    )
    glist: List[Union[Graph, DiGraph]] = [reader(path=path)]
    if len(glist) == 0:
        raise NetworkXError('file not successfully read as mtx')
    return glist[0]


class MatrixMarketReader:
    def __init__(self, node_type=str, edge_key_type=int):
        self.node_type = node_type
        self.edge_key_type = edge_key_type
        self.edge_ids = {}

    def __call__(self, path: str = None, string: str = None):
        if path is not None:
            self.mtx = MatrixMarket(file=path)
        elif string is not None:
            self.mtx = MatrixMarket.from_string(string)

        if self.mtx.symmetry in (self.mtx.SYMMETRY_GENERAL,):
            graph = DiGraph()
        elif self.mtx.symmetry in (self.mtx.SYMMETRY_SYMMETRIC,
                                   self.mtx.SYMMETRY_HERMITIAN,
                                   self.mtx.SYMMETRY_SKEWSYMMETRIC):
            graph = Graph()
        else:
            raise ValueError(f"Unsupported symmetry '{self.mtx.symmetry}'")

        if self.mtx.format == self.mtx.FORMAT_COORDINATE:
            for coordinate in self.mtx.coordinates:
                source = self.node_type(coordinate[0])
                target = self.node_type(coordinate[1])
                if self.mtx.field == self.mtx.FIELD_PATTERN:
                    graph.add_edge(source, target)
                else:
                    graph.add_edge(source, target,
                                   weight=coordinate[2])
        elif self.mtx.format == self.mtx.FORMAT_ARRAY:
            raise NotImplementedError
        else:
            raise ValueError(f"Unsupported MatrixMarket "
                             f"format '{self.mtx.format}'.")
        return graph


class MatrixMarket:
    MMID = '%%MatrixMarket'
    MATRIX = 'matrix'
    FORMAT_COORDINATE = 'coordinate'
    FORMAT_ARRAY = 'array'
    FIELD_REAL = 'real'
    FIELD_INTEGER = 'integer'
    FIELD_COMPLEX = 'complex'
    FIELD_PATTERN = 'pattern'
    SYMMETRY_GENERAL = 'general'
    SYMMETRY_SYMMETRIC = 'symmetric'
    SYMMETRY_SKEWSYMMETRIC = 'skew-symmetric'
    SYMMETRY_HERMITIAN = 'Hermitian'
    VALID_MMID = (MMID,)
    VALID_MATRIX = (MATRIX,)
    VALID_FORMAT = (FORMAT_ARRAY, FORMAT_COORDINATE)
    VALID_FIELD = (FIELD_COMPLEX, FIELD_INTEGER, FIELD_PATTERN, FIELD_REAL)
    VALID_FIELD_TYPES = (int, float, complex, bool)
    VALID_SYMMETRY = (SYMMETRY_GENERAL, SYMMETRY_HERMITIAN,
                      SYMMETRY_SKEWSYMMETRIC, SYMMETRY_SYMMETRIC)

    def __init__(self, file: str = None):
        self._mmid = None
        self._matrix = None
        self._format = None
        self._field = None
        self._symmetry = None
        self._rows = None
        self._columns = None
        self._entries = None
        self._coordinates: List[
            Tuple[int, int, Union[int, float, complex, bool]]
        ] = None
        self._values = List[Union[int, float, complex]]
        if file:
            self.from_file(file)

    @property
    def mmid(self) -> str:
        return self._mmid

    @property
    def matrix(self) -> str:
        return self._matrix

    @property
    def format(self) -> str:
        return self._format

    @property
    def field(self) -> str:
        return self._field

    @property
    def field_type(self) -> Type[Union[int, float, complex, bool]]:
        if self._field == self.FIELD_INTEGER:
            return int
        elif self._field == self.FIELD_REAL:
            return float
        elif self._field == self.FIELD_COMPLEX:
            return complex
        elif self._field == self.FIELD_PATTERN:
            return bool
        else:
            raise ValueError(f"Invalid field type '{self._field}'")

    @property
    def symmetry(self) -> str:
        return self._symmetry

    @property
    def rows(self) -> int:
        return self._rows

    @property
    def columns(self) -> int:
        return self._columns

    @property
    def entries(self) -> int:
        return self._entries

    @property
    def coordinates(self):
        return self._coordinates

    @property
    def values(self):
        raise NotImplementedError
        return self._values

    @staticmethod
    def from_string(string: str) -> MatrixMarket:
        mtx = MatrixMarket()
        mtx.parse_lines(string.splitlines())
        return mtx

    def from_file(self, source: Union[TextIOBase, str], parser=None):
        close_source = False
        if not hasattr(source, "read"):
            source: TextIOBase = open(source, 'r')
            close_source = True

        try:
            self.parse_lines(source.readlines())
        finally:
            if close_source:
                source.close()

    def parse_lines(self, lines: List[str]):
        i = 0
        mmid, matrix, _format, field, symmetry = \
            [str(part.strip()) for part in lines[i].split()]
        if mmid not in self.VALID_MMID:
            raise ValueError('source is not in Matrix Market format')
        if matrix not in self.VALID_MATRIX:
            raise ValueError("Problem reading file header: " + lines[i])
        if _format not in self.VALID_FORMAT:
            raise ValueError(f"Invalid format '{_format}'")
        if field not in self.VALID_FIELD:
            raise ValueError(f"Invalid field type '{field}'")
        if symmetry not in self.VALID_SYMMETRY:
            raise ValueError(f"Invalid Symmetry '{symmetry}'")

        self.validate_header(mmid, matrix, _format, field, symmetry)
        self._mmid = mmid
        self._matrix = matrix
        self._format = _format
        self._field = field
        self._symmetry = symmetry
        i += 1

        while lines[i].startswith('%'):
            i += 1

        line = lines[i].split()
        if self.format == self.FORMAT_ARRAY:
            self._values = list()
            if not len(line) == 2:
                raise ValueError("Header line not of length 2.")
            rows, cols = map(int, line)
            entries = rows * cols
        elif self.format == self.FORMAT_COORDINATE:
            self._coordinates = list()
            if not len(line) == 3:
                raise ValueError("Header line not of length 3.")
            rows, cols, entries = map(int, line)
        else:
            raise ValueError(f"Invalid format '{_format}'")
        self._rows = rows
        self._columns = cols
        self._entries = entries

        len_expected = i + self.entries
        i += 1
        try:
            for entry_index in range(i, len_expected):
                self.process_line(lines[entry_index])
        except IndexError:
            raise ValueError(f"Missing {len_expected - entry_index - 1} "
                             f"entries.")

    def process_line(self, line: str):
        items = line.split()
        if self.format == self.FORMAT_COORDINATE:
            if self.field_type == bool:
                self.validate_entry_items(items, 2)
                self._coordinates.append((
                    int(items[0]), int(items[1]), True
                ))
            elif self.field_type == int:
                self.validate_entry_items(items, 3)
                self._coordinates.append((
                    int(items[0]), int(items[1]), int(items[2])
                ))
            elif self.field_type == float:
                self.validate_entry_items(items, 3)
                self._coordinates.append((
                    int(items[0]), int(items[1]), float(items[2])
                ))
            elif self.field_type == complex:
                self.validate_entry_items(items, 4)
                self._coordinates.append((
                    int(items[0]), int(items[1]),
                    complex(float(items[2]), float(items[3]))
                ))

        elif self.format == self.FORMAT_ARRAY:
            raise NotImplementedError
        else:
            raise ValueError(f"Invalid format '{self.format}'")

    @staticmethod
    def validate_entry_items(items: List[str], expected_count: int):
        if len(items) != expected_count:
            raise ValueError(f"Expected {expected_count} "
                             f"items for entry, not {len(items)}")

    def validate_header(self, mmid, matrix, _format, field, symmetry):
        if _format in (self.FORMAT_COORDINATE,
                       self.FORMAT_ARRAY) and \
                field in (self.FIELD_REAL,
                          self.FIELD_INTEGER,
                          self.FIELD_COMPLEX) and \
                symmetry in (self.SYMMETRY_GENERAL,
                             self.SYMMETRY_SYMMETRIC,
                             self.SYMMETRY_SKEWSYMMETRIC):
            return
        elif _format in (self.FORMAT_COORDINATE,
                         self.FORMAT_ARRAY) and \
                field in (self.FIELD_COMPLEX,) and \
                symmetry in (self.SYMMETRY_HERMITIAN,):
            return
        elif _format in (self.FORMAT_COORDINATE,) and \
                field in (self.FIELD_PATTERN,) and \
                symmetry in (self.SYMMETRY_GENERAL,
                             self.SYMMETRY_SYMMETRIC):
            return
        else:
            header_format = f"{mmid} {matrix} {_format} {field} {symmetry}"
            raise ValueError(f"Invalid header format '{header_format}'.")


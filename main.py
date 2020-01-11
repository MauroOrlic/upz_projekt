from utils import load_raw, dump_graphml, load_graphml
from pathlib import Path


path_raw_power = Path('raw_data/inf-power/inf-power.mtx')
path_raw_openflights= Path('raw_data/inf-openflights/inf-openflights.edges')
path_raw_roadnet_ca = Path('raw_data/inf-roadNet-CA/inf-roadNet-CA.mtx')
path_raw_roadnet_pa = Path('raw_data/inf-roadNet-PA/inf-roadNet-PA.mtx')
path_raw_usair97 = Path('raw_data/inf-USAir97/inf-USAir97.mtx')

paths_raw = [
    path_raw_power,
    path_raw_openflights,
    path_raw_roadnet_ca,
    path_raw_roadnet_pa,
    path_raw_usair97
]
for path in paths_raw:
    graph = load_raw(path)
    processed_path = Path(f"processed_data/{path.stem}.graphml")
    dump_graphml(graph, processed_path)

path_processed_power = Path('processed_data/inf-power.graphml')
path_processed_openflights = Path('processed_data/inf-openflights.graphml')
path_processed_roadnet_ca = Path('processed_data/inf-roadNet-CA.graphml')
path_processed_roadnet_pa = Path('processed_data/inf-roadNet-PA.graphml')
path_processed_usair97 = Path('processed_data/inf-USAir97.graphml')


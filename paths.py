from pathlib import Path
from os import environ

env_working_dir = 'WORKING_DIR_UPZ_PROJEKT'
try:
    working_dir = Path(environ[env_working_dir])
except KeyError:
    working_dir = Path('.').absolute()

raw = working_dir / 'raw_data'
raw_openflights = raw / 'inf-openflights.edges'
raw_power = raw / 'inf-power.mtx'
raw_roadnet_ca = raw / 'inf-roadNet-CA.mtx'
raw_roadnet_pa = raw / 'inf-roadNet-PA.mtx'
raw_usair97 = raw / 'inf-USAir97.mtx'

processed = working_dir / 'processed_data'
suffix_graphml = '.graphml'
processed_openflights = processed / f"{raw_openflights.stem}{suffix_graphml}"
processed_power = processed / f"{raw_power.stem}{suffix_graphml}"
processed_roadnet_ca = processed / f"{raw_roadnet_ca.stem}{suffix_graphml}"
processed_roadmap_pa = processed / f"{raw_roadnet_pa.stem}{suffix_graphml}"
processed_usair97 = processed / f"{raw_usair97.stem}{suffix_graphml}"

results = working_dir / 'results'

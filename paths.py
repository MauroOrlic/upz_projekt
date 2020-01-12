from pathlib import Path
raw = Path('raw_data/')
raw_openflights = Path(raw / 'inf-openflights.edges')
raw_power = Path(raw / 'inf-power.mtx')
raw_roadnet_ca = Path(raw / 'inf-roadNet-CA.mtx')
raw_roadnet_pa = Path(raw / 'inf-roadNet-PA.mtx')
raw_usair97 = Path(raw / 'inf-USAir97.mtx')

processed = Path('processed_data/')
suffix_graphml = '.graphml'
processed_openflights = Path(processed / raw_openflights.stem).with_suffix(suffix_graphml)
processed_power = Path(processed / raw_power.stem).with_suffix(suffix_graphml)
processed_roadnet_ca = Path(processed / raw_roadnet_ca.stem).with_suffix(suffix_graphml)
processed_roadmap_pa = Path(processed / raw_roadnet_pa.stem).with_suffix(suffix_graphml)
processed_usair97 = Path(processed / raw_usair97.stem).with_suffix(suffix_graphml)

from utils import load_raw, dump_graphml

from paths import raw_openflights, raw_power, raw_roadnet_ca, \
    raw_roadnet_pa, raw_usair97, processed_openflights, \
    processed_power, processed_roadmap_pa, processed_roadnet_ca, \
    processed_usair97


paths = [
    (raw_openflights, processed_openflights),
    (raw_power, processed_power),
    (raw_roadnet_ca, processed_roadnet_ca),
    (raw_roadnet_pa, processed_roadmap_pa),
    (raw_usair97, processed_usair97)
]
RAW = 'raw'
PROCESSED = 'procesed'
GRAPH = 'graph'
graphs = {
    graph_paths[0].stem: {
        RAW: graph_paths[0],
        PROCESSED: graph_paths[1],
        GRAPH: load_raw(graph_paths[0])}
    for graph_paths in paths
}

for graph in graphs.values():
    dump_graphml(graph[GRAPH], graph[PROCESSED])










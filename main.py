from datetime import datetime
from multiprocessing import Process
from pathlib import Path
from os import getpid

from matplotlib import pyplot as plt

from graph_measures import GraphMeasures
from paths import processed_openflights, processed_power, \
    processed_roadnet_ca, processed_roadmap_pa, \
    processed_usair97
from paths import results
from utils import load_graphml

import networkx as nx

graph_paths = {
    0: processed_openflights,
    1: processed_power,
    2: processed_roadnet_ca,
    3: processed_roadmap_pa,
    4: processed_usair97
}

MAX_GRAPH_SIZE = 10**4
UNAVAILABLE = 'N/A'

HISTOGRAM_BINS = 100


def write_basic(measures: GraphMeasures, name: str):
    print(f"{datetime.now()} - Graph {name}: STARTED - basic measures")
    results_basic: Path = results / f"{name}_basic.txt"
    with results_basic.open('w') as file:
        file.write(f"Tip\t{'' if measures.directed else 'ne'}usmjeren\t{'' if measures.weighted else 'ne'}težinski\n")

        file.write(f"Broj vrhova\t{measures.node_count}\n")

        if measures.directed:
            file.write(f"Broj veza\t{measures.edge_count[0]}\t{measures.edge_count[1]}\n")
        else:
            file.write(f"Broj veza\t{measures.edge_count}\n")

        if measures.directed:
            file.write(f"Prosječan broj veza\t{measures.avg_edge_count[0]}\t{measures.avg_edge_count[1]}\n")
        else:
            file.write(f"Prosječan broj veza\t{measures.avg_edge_count}\n")

        if measures.weighted:
            if measures.directed:
                file.write(f"Prosječna snaga\t{measures.avg_strength[0]}\t{measures.avg_strength[1]}\n")
            else:
                file.write(f"Prosječna snaga\t{measures.avg_strength}\n")

        file.write(f"Broj komponenti\t{measures.component_count}\n")

        if measures.directed:
            file.write(f"Veličina najveće komponente\t{measures.largest_component_measures.node_count}\t{sum(measures.largest_component_measures.edge_count)}\n")
        else:
            file.write(f"Veličina najveće komponente\t{measures.largest_component_measures.node_count}\t{measures.largest_component_measures.edge_count}\n")

        file.write(f"Prosječna duljina najkraćeg puta\t{measures.shortest_path_length if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
        file.write(f"Dijametar\t{measures.diameter if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
        file.write(f"Ekscentričnost\t{measures.eccentricity if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
        file.write(f"Globalna učinkovitost\t{measures.global_efficiency if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
        file.write(f"Prosječni koeficijent grupiranje\t{measures.avg_clustering_coefficient}\n")
        file.write(f"Asortativnost s obzirom na stupanj čvora\t{measures.degree_assortativity}\n")
        file.write(f"Prosječna centralnost blizine\t{measures.avg_closeness_centrality if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
        file.write(f"Prosječna međupoloženost\t{measures.avg_betweenness_centrality if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
    print(f"{datetime.now()} - Graph {name}: FINISHED - basic measures")


def write_centrality(measures: GraphMeasures, name: str):
    print(f"{datetime.now()} - Graph {name}: STARTED - centrality")
    results_centrality: Path = results / f"{name}_centrality.txt"
    with results_centrality.open('w') as file:
        file.write(f"Centralni čvorovi\n")
        file.write(f"Stupnja\tMeđupoloženosti\tBlizine\n")
        for i in range(10):
            file.write(f"{measures.top10_central_degree[i][0]}\t"
                       f"{measures.top10_central_betweenness[i][0] if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\t"
                       f"{measures.top10_central_closeness[i][0] if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
    print(f"{datetime.now()} - Graph {name}: FINISHED - centrality")


def write_modularity(measures: GraphMeasures, name: str):
    print(f"{datetime.now()} - Graph {name}: STARTED - modularity")
    results_modularity: Path = results / f"{name}_modularity.txt"
    with results_modularity.open('w') as file:
        try:
            file.write(f"Modularnost\t{measures.modularity if measures.node_count < MAX_GRAPH_SIZE else UNAVAILABLE}\n")
            file.write(f"Svojstva zajednica\n")
            if measures.node_count > MAX_GRAPH_SIZE:
                file.write("Greška: Preveliki graf.")
                return
            file.write(f"Broj čvorova\tBroj veza\n")
            for c_measures in measures.top10_community_measures:
                if measures.directed:
                    file.write(f"{c_measures.node_count}\t{sum(c_measures.edge_count)}\n")
                else:
                    file.write(f"{c_measures.node_count}\t{c_measures.edge_count}\n")
        except nx.algorithms.community.quality.NotAPartition:
            print(f"{datetime.now()} - Graph {name}: FAILED - modularity")
            file.write(f"FAILED")
    print(f"{datetime.now()} - Graph {name}: FINISHED - modularity")


def write_histograms(measures: GraphMeasures, name: str):
    print(f"{datetime.now()} - Graph {name}: STARTED - histograms")
    if measures.directed:
        results_hist_degree_in: Path = results / f"{name}_hist_degree_in.png"
        degrees_in = tuple(degree[1] for degree in measures.graph.in_degree())
        plt.xlabel('Stupanj')
        plt.xlabel('Frekvencija')
        plt.hist(degrees_in, bins=HISTOGRAM_BINS)
        plt.savefig(results_hist_degree_in.as_posix())
        plt.close()

        results_hist_degree_out: Path = results / f"{name}_hist_degree_out.png"
        degrees_out = tuple(degree[1] for degree in measures.graph.out_degree())
        plt.xlabel('Stupanj')
        plt.xlabel('Frekvencija')
        plt.hist(degrees_out, bins=HISTOGRAM_BINS)
        plt.savefig(results_hist_degree_out.as_posix())
        plt.close()
    else:
        degrees = tuple(degree[1] for degree in measures.graph.degree())
        plt.xlabel('Stupanj')
        plt.xlabel('Frekvencija')
        results_hist_degree: Path = results / f"{name}_hist_degree.png"
        plt.hist(degrees, bins=HISTOGRAM_BINS)
        plt.savefig(results_hist_degree.as_posix())
        plt.close()

    if measures.weighted:
        if measures.directed:
            results_hist_weight_in: Path = results / f"{name}_hist_weight_in.png"
            plt.xlabel('Snaga')
            plt.xlabel('Frekvencija')
            weights = tuple(in_edge[2]['weight'] for in_edge in measures.graph.in_edges().data())
            plt.hist(weights, bins=HISTOGRAM_BINS)
            plt.savefig(results_hist_weight_in.as_posix())
            plt.close()

            results_hist_weight_out: Path = results / f"{name}_hist_weight_out.png"
            plt.xlabel('Snaga')
            plt.xlabel('Frekvencija')
            weights = tuple(out_edge[2]['weight'] for out_edge in measures.graph.out_edges().data())
            plt.hist(weights, bins=HISTOGRAM_BINS)
            plt.savefig(results_hist_weight_out.as_posix())
            plt.close()
        else:
            results_hist_weight: Path = results / f"{name}_hist_weight.png"
            plt.xlabel('Snaga')
            plt.xlabel('Frekvencija')
            weights = tuple(edge[2]['weight'] for edge in measures.graph.edges().data())
            plt.hist(weights, bins=HISTOGRAM_BINS)
            plt.savefig(results_hist_weight.as_posix())
            plt.close()
    print(f"{datetime.now()} - Graph {name}: FINISHED - histograms")


stat_functions = (
    write_basic,
    write_histograms,
    write_centrality,
    write_modularity
)

if __name__ == '__main__':
    '''
    path = graph_paths[4]
    p = Process(target=write_modularity, args=(GraphMeasures(load_graphml(path)), path.stem))
    p.start()
    '''

    for graph_id in (0, 1, 2, 3, 4):
        path = graph_paths[graph_id]
        graph_measures = GraphMeasures(load_graphml(path))
        for func in stat_functions:
            process = Process(target=func, args=(graph_measures, path.stem))
            process.start()

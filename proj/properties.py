import networkx as nx
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from networkx.algorithms.community.centrality import girvan_newman
from scipy.io import mmread

# Možné optimalizace
# .tocsr() - vytvoření CSR matice (Compressed Sparse Row)
# .tocsc() - vytvoření CSC matice (Compressed Sparse Column)
matrix = mmread("web-indochina-2004/web-indochina-2004.mtx").tocsc()

# Počet uzlů (N)
N = matrix.shape[0]
print(f"Počet uzlů: {N}")

# Počet hran (E)
# Pokud je síť neorientovaná, počítáme pouze jednou každou hranu
E = matrix.nnz
print(f"Počet hran: {E}")

# Je graf symetrický ?
is_symmetric = (matrix != matrix.T).nnz == 0

# Kontrola symetrie matice
if is_symmetric:
    print("Matice je symetrická")
    print(f"Počet hran je ve skutečnosti {E / 2}")
    density = E / (N * (N - 1))
else:
    print("Matice není symetrická")
    density = 2 * E / (N * (N - 1))

# Průměrný a maximální stupeň
if is_symmetric:
    # avg_degree = E / N <- taky možnost výpočtu průměrného stupně
    degrees = np.array(matrix.sum(axis=1)).flatten()
else:
    # avg_degree = 2 * E / N <- taky možnost výpočtu průměrného stupně
    in_degrees = np.array(matrix.sum(axis=0)).flatten()  # In-degree (sloupce)
    out_degrees = np.array(matrix.sum(axis=1)).flatten()  # Out-degree (řádky)
    degrees = in_degrees + out_degrees

# Import do NetworkX
# note: existuje nx.DiGraph pro orientovaný graf
G = nx.Graph(matrix)
print(f"G je orientovaný: {nx.is_directed(G)}")


def nodewise_clustering(G):
    clustering_coeffs = nx.clustering(G)

    # Manuální výpočet průměrného shlukovacího koeficientu
    # (Pro cross-check s nx.average_clustering)
    avg_clustering = np.mean(list(clustering_coeffs.values()))
    print(f"Průměrný shlukovací koeficient (CC): {avg_clustering}")

    # Výpočet shlukovacího efektu (CC vs stupeň)
    degrees = dict(G.degree())
    degree_to_cc = {}

    for node, degree in degrees.items():
        if degree not in degree_to_cc:
            degree_to_cc[degree] = []
        degree_to_cc[degree].append(clustering_coeffs[node])

    # Průměrný CC pro každý stupeň
    avg_cc_per_degree = {k: np.mean(v) for k, v in degree_to_cc.items()}

    # Graf shlukovacího efektu
    plt.figure(figsize=(16, 6))
    plt.scatter(avg_cc_per_degree.keys(), avg_cc_per_degree.values())
    plt.title("Shlukovací efekt: CC vůči stupni")
    plt.xlabel("Stupeň uzlu")
    plt.ylabel("Průměrný shlukovací koeficient (CC)")
    plt.grid(True)
    plt.xticks(range(0, 201, 2), rotation=90)
    plt.show()


def degree_distribution(G):
    degree_sequence = [d for n, d in G.degree()]

    plt.figure(figsize=(16, 6))

    from collections import Counter
    degree_count = Counter(degree_sequence)
    degrees, counts = zip(*sorted(degree_count.items()))

    plt.scatter(degrees, counts)

    plt.grid(True)
    plt.xticks(range(0, 201, 2), rotation=90)
    plt.title("Distribuce stupňů uzlů")
    plt.xlabel("Stupeň")
    plt.ylabel("Počet uzlů (log)")

    plt.yscale("log")

    plt.show()

    # Kontrola
    print(f"Kontrola: Počet uzlů: {len(degree_sequence)}")
    print(f"Kontrola: Počet hran: {sum(degree_sequence) // 2}")


def community_distribution(G, communities):
    community_mapping = {
        node: idx for idx, community in enumerate(communities) for node in community
    }
    community_sizes = np.bincount(list(community_mapping.values()))
    min_size = np.min(community_sizes)
    max_size = np.max(community_sizes)

    community_sizes = sorted(community_sizes, reverse=True)

    plt.figure(figsize=(16, 6))
    plt.bar(range(len(community_sizes)), community_sizes)
    plt.title("Distribuce velikostí komunit")
    plt.xlabel("Komunita")
    plt.ylabel("Velikost komunity")
    plt.grid(True)
    plt.show()

    print(f"Počet komunit: {len(community_sizes)}")
    print(f"Minimální velikost komunity: {min_size}")
    print(f"Průměrná velikost komunity: {np.mean(community_sizes)}")
    print(f"Maximální velikost komunity: {max_size}")


# CC
nodewise_clustering(G)
clustering = nx.average_clustering(G)
print(f"Shlukovací koeficient: {clustering}")

# Počet trojúhelníků
triangles = sum(nx.triangles(G).values()) // 3
print(f"Počet trojúhelníků: {triangles}")

# Gephi dává vyšší výsledek, protože počítá trojúhelníky pouze pro uzly se stupněm > 1
# Tento výpočet jde mimikovat následovně:
clustering_coeffs = nx.clustering(G)
filtered_coeffs = [
    coeff for node, coeff in clustering_coeffs.items() if G.degree[node] > 1
]

# Vypočítat průměrný shlukovací koeficient po filtraci
avg_clustering_filtered = np.mean(filtered_coeffs)
print(f"Průměrný CC (filtrovaný pouze uzly se stupněm > 1): {avg_clustering_filtered}")

# Distribuce stupňů uzlů
degree_distribution(G)

# Girvan Newman
# girvan_newman_communities = next(girvan_newman(G))
# girvan_newman_result = \
#     {
#         node: idx for idx, community in
#         enumerate(girvan_newman_communities)
#         for node in community
#     }

# nepoužito kvůli výpočetní náročnosti

# Label Propagation
label_propagation_communities = nx.community.label_propagation_communities(G)
# lpc_modularity = nx.community.quality.modularity(G, label_propagation_communities)
lpc_community_mapping = {
    node: idx for idx, community in enumerate(label_propagation_communities) for node in community
}

# nefungoval úplně dobře

# Louvain
louvain_communities = nx.community.louvain_communities(G)
# louvain_modularity = nx.community.quality.modularity(G, louvain_communities)
louvain_community_mapping = {
    node: idx for idx, community in enumerate(louvain_communities) for node in community
}

# infomap
from cdlib import algorithms

infomap_communities = algorithms.infomap(G)
node_community_mapping = {
    node: idx for idx, community in enumerate(infomap_communities.communities) for node in community
}

# markov
# import markov_clustering as mc
# adjacency_matrix = nx.to_numpy_array(G)

# Run MCL
# result = mc.run_mcl(adjacency_matrix)
# clusters = mc.get_clusters(result)

# Nepoužito z důvodu výpočetní náročnosti


results_df = pd.DataFrame({
    "Id": list(G.nodes),
    "Label Propagation Community": [lpc_community_mapping[node] for node in G.nodes],
    "Louvain Community": [louvain_community_mapping[node] for node in G.nodes],
    "infomap": list(node_community_mapping.values()),
    # "markov": [idx for idx, cluster in enumerate(clusters) for node in cluster]
})

# Uložení do CSV pro import do Gephi
# results_df.to_csv("community_detection_results.csv", index=False)

# modularita
lpc_modularity = nx.community.quality.modularity(G, label_propagation_communities)
louvain_modularity = nx.community.quality.modularity(G, louvain_communities)
infomap_modularity = nx.community.quality.modularity(
    G,
    [set(community) for community in infomap_communities.communities]
)


print(f"Louvain Communities modularity: {louvain_modularity:.2f}")
community_distribution(G, louvain_communities)

print(f"Label Propagation Communities modularity: {lpc_modularity:.2f}")
community_distribution(G, label_propagation_communities)

print(f"Infomap Communities modularity: {infomap_modularity:.2f}")
community_distribution(G, infomap_communities.communities)


print(f"Průměrný stupeň: {np.mean(degrees)}")
print(f"Maximální stupeň: {np.max(degrees)}")
print(f"Hustota sítě: {density}")

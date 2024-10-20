import os
from collections import defaultdict

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

f = open("KarateClub.csv", "r")
G=nx.read_edgelist(f, delimiter=';', nodetype=int)

# list s lokálními koeficienty shlukování
# 1 - všichni sousedé vi jsou propojeni
# 0 - žádný soused vi není propojen navzájem
local_indices_clustering = nx.clustering(G)

###
# Úkol 1
###

# rozmístíme vrcholy grafu
pos = nx.spring_layout(G)
# matplotlib figura
plt.figure(figsize=(10, 10))
# vykreslení původního grafu
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, font_color='black', edge_color='gray')

# dictionary o velikosti 34 s hodnotami lokálních koeficientů shlukování
clustering_labels = {node: f'{local_indices_clustering[node]:.2f}' for node in G.nodes()}
# vezmeme z pos.items() node a coords, a coords posuneme podél y-axis
offset_pos = {node: (coords[0], coords[1] + 0.05) for node, coords in pos.items()}
# vykreslení
nx.draw_networkx_labels(G, offset_pos, labels=clustering_labels, font_color='red', font_size=10)
plt.title("Shlukovací lokální koeficienty")
plt.show()

# tranzitivita sítě - průměrný shlukovací koeficient
transitivity = nx.transitivity(G)
transitivity_manual = sum(local_indices_clustering.values()) / len(local_indices_clustering)
transitivity_average = nx.average_clustering(G)
print(f"Průměrný shlukovací koeficient (nx.transitivity): {transitivity:.2f}")
print(f"Průměrný shlukovací koeficient (druhá kalkulace - pravý průměr): {transitivity_manual:.2f}")
print(f"Průměrný shlukovací koeficient (nx.average_clustering): {transitivity_average:.2f}")

#
### Úkol 2
#
len_G = len(G.nodes())
degrees = dict(G.degree())
degrees_dict = defaultdict(list)
for v, deg in degrees.items():
    degrees_dict[deg].append(v)
    
degrees_final = defaultdict(float)
for deg, vertices in degrees_dict.items():
    sum_vertices_local_clustering = sum([local_indices_clustering[v] for v in vertices])
    avg_vertices_local_clustering = sum_vertices_local_clustering / len(vertices)
    degrees_final[deg] = avg_vertices_local_clustering    
    

plt.bar(list(degrees_final.keys()), list(degrees_final.values()))
plt.xlim(0, 20)
plt.xticks(range(0, 20, 1))
plt.show()

###
# Úkol 3
###

# closeness centrality
closeness = nx.closeness_centrality(G)
# note: ordering not strictly kept in zip
nodes_csv, degrees_csv = zip(*G.degree())
final_csv = zip(nodes_csv, degrees_csv, closeness.values(), list(local_indices_clustering.values()))

with open("KarateClub_centrality.csv", "w") as f:
    f.write("vertex;degree;closeness;clustering\n")
    for a, b, c, d in final_csv:
        f.write(f"{a};{b};{c:.2f};{d:.2f}\n")

print("done")
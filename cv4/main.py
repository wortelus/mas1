from collections import defaultdict

import networkx as nx
from matplotlib import pyplot as plt

network_x_colors = ['red', 'blue', 'green', 'yellow', 'purple', 'orange', 'black', 'pink', 'brown', 'gray']

def plot_g_set(G, sets, title):
    nodes = G.nodes()
    colors_communities = []
    for node_id in nodes:
        for i, community in enumerate(sets):
            if node_id in community:
                colors_communities.append(network_x_colors[i])
    
    print(f"{title}: {sets}")
    
    # rozmístíme vrcholy grafu
    pos = nx.spring_layout(G)
    # matplotlib figura
    plt.figure(figsize=(10, 10))
    # vykreslení původního grafu
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_color=colors_communities, node_size=500, font_size=10, font_color='black', edge_color='gray')
    plt.show()
    
    
def plot_g_set_multicolor(G, sets, title):
    nodes = G.nodes()
    colors_communities = {}
    default_node_colors = []
    for node_id in nodes:
        colors_node_id = []
        for i, community in enumerate(sets):
            if node_id in community:
                colors_node_id.append(network_x_colors[i])
        colors_communities[node_id] = ", ".join(colors_node_id)
        if len(colors_node_id) == 1:
            default_node_colors.append(colors_node_id[0])
        else:
            default_node_colors.append('white')

    # rozmístíme vrcholy grafu
    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 10))
    plt.title(title)
    nx.draw(G, pos, with_labels=True, node_color=default_node_colors, node_size=500, font_size=10, font_color='black', edge_color='gray')

    offset_pos = {node: (coords[0], coords[1] + 0.05) for node, coords in pos.items()}
    # vykreslení
    nx.draw_networkx_labels(G, offset_pos, labels=colors_communities, font_color='black', font_size=10)
    plt.show()

def main():
    f = open("KarateClub.csv", "r")
    G=nx.read_edgelist(f, delimiter=';', nodetype=int)
    
    # louvain
    louvain = nx.community.louvain_communities(G)
    plot_g_set(G, louvain, "Louvain")
    louvain_modularity = nx.community.quality.modularity(G, louvain)
    
    # label_propagation_communities
    label_propagation_communities = nx.community.label_propagation_communities(G)
    plot_g_set(G, label_propagation_communities, "Label Propagation Communities")
    lpc_modularity = nx.community.quality.modularity(G, label_propagation_communities)
    
    # girvan newman
    # girvan_newman = nx.community.label_propagation_communities(G)
    # plot_g_set(G, girvan_newman, "Girvan Newman")

    # kerninghan
    # to je ta kde se minimalizuje funkce g()
    # končí s 2 komunitama
    # chceme 4...
    kernighan_lin_bisection = nx.community.kernighan_lin_bisection(G)
    klb_a_subgraph = G.subgraph(kernighan_lin_bisection[0])
    klb_b_subgraph = G.subgraph(kernighan_lin_bisection[1])
    
    klb_a = nx.community.kernighan_lin_bisection(klb_a_subgraph)
    klb_b = nx.community.kernighan_lin_bisection(klb_b_subgraph)
    
    klb_four_communities = list(klb_a + klb_b)
    plot_g_set(G, klb_four_communities, "Kernighan Lin Bisection")
    klb_four_communities_modularity = nx.community.quality.modularity(G, klb_four_communities)
    
    # jelikož edge betweeness je underlying algoritmus pro girvan newman
    # a chcemete 4 clustery
    # tak ho zavolám přímo...
    # vyjde stejně jako bruteforce pro girvan newman if n == 4
    edge_betweenness_partition = nx.community.edge_betweenness_partition(G, 4)
    plot_g_set(G, edge_betweenness_partition, "Edge Betweenness Partition")
    edge_betweenness_partition_modularity = nx.community.quality.modularity(G, edge_betweenness_partition)
    
    # Clique Percolation method
    # poznámka: tady se overlapují komunity
    # nevhodné pro velké grafy, jedná se spíše o pattern matching
    k_clique = nx.community.k_clique_communities(G, 3)
    k_clique = list(k_clique)
    plot_g_set_multicolor(G, k_clique, "K-Clique Communities")
    # k_clique_modularity = nx.community.quality.modularity(G, k_clique)
    
    # modularity
    print(f"Louvain modularity: {louvain_modularity}")
    print(f"Label Propagation Communities modularity: {lpc_modularity}")
    print(f"Kernighan Lin Bisection modularity: {klb_four_communities_modularity}")
    print(f"Edge Betweenness Partition modularity: {edge_betweenness_partition_modularity}")
    # print(f"K-Clique Communities modularity: {k_clique_modularity}")
    
    f_csv = open("KarateClub_cv3.csv", "r")
    f_csv_content = f_csv.read()
    f_csv_content_lines = f_csv_content.split('\n')
    f_csv_content_values = [a.split(';') for a in f_csv_content_lines if a]
    
    for i, the_rest in enumerate(f_csv_content_values):
        if i == 0:
            the_rest.append("Louvain communities")
            the_rest.append("Label Propagation Communities communities")
            the_rest.append("Kernighan Lin Bisection communities")
            the_rest.append("Edge Betweenness Partition communities")
            the_rest.append("K-Clique Communities communities")
            continue
        
        node_id = int(the_rest[0])
        # the_rest.append(f"{louvain_modularity:.2f}")
        # the_rest.append(f"{lpc_modularity:.2f}")
        # the_rest.append(f"{klb_four_communities_modularity:.2f}")
        # the_rest.append(f"{edge_betweenness_partition_modularity:.2f}")

        the_rest.append(
            "(" + ", ".join([str(i) for i, comm in enumerate(louvain) if int(node_id) in comm]) + ")")
        the_rest.append(
            "(" + ", ".join([str(i) for i, comm in enumerate(label_propagation_communities) if int(node_id) in comm]) + ")")
        the_rest.append(
            "(" + ", ".join([str(i) for i, comm in enumerate(klb_four_communities) if int(node_id) in comm]) + ")")
        the_rest.append(
            "(" + ", ".join([str(i) for i, comm in enumerate(edge_betweenness_partition) if int(node_id) in comm]) + ")")
        the_rest.append(
            "(" + ", ".join([str(i) for i, comm in enumerate(k_clique) if int(node_id) in comm]) + ")")
        
    csv_out = open("KarateClub_out.csv", "w")
    for line in f_csv_content_values:
        csv_out.write(";".join([str(a) for a in line]) + "\n")
    



if __name__ == "__main__":
    main()
def edge_graph_to_adj_list(edges: list[tuple[int, int]], directed=False):
    adj_list = {}
    for edge in edges:
        if edge[0] not in adj_list:
            adj_list[edge[0]] = set()
        adj_list[edge[0]].add(edge[1])
        if not directed:
            if edge[1] not in adj_list:
                adj_list[edge[1]] = set()
            adj_list[edge[1]].add(edge[0])
    return adj_list


# taken from cv7
def export_edge_list(graph, filename):
    with open(filename, "w") as f:
        f.write("source;target\n")
        for node, neighbors in enumerate(graph):
            for neighbor in neighbors:
                f.write(f"{node};{neighbor}\n")
from random import sample

from cv8.core import export_edge_list, edge_graph_to_adj_list


def snowball_sampling(g_adj_list: list[set[int]], n_total, n_snowballs):
    g_len = len(g_adj_list)

    discovered = set()
    discovered_edges = set()

    print(f"Graph has {g_len} nodes.")
    start_node = sample(range(g_len), 1)[0]
    visited = {start_node}
    i = 0
    while len(discovered) < n_total:
        i += 1
        print(f"Iteration {i}")
        for j in range(n_snowballs):
            if len(visited) == 0:
                print(f"Whole graph is processed for {j} bfs iteration.")
                break
            node = visited.pop()
            discovered.add(node)
            
            for neighbor in g_adj_list[node]:
                if len(discovered) >= n_total:
                    break
                if neighbor not in discovered:
                    discovered_edges.add(frozenset([node, neighbor]))
                    visited.add(neighbor)
                    discovered.add(neighbor)
            
            # solved by previous loop
            # visited.update(g_adj_list[node] - discovered)

        print(f"Snowball {i} is processed, discovered: {len(discovered)}, visited: {len(visited)}.")

    # export node list
    with open("snowball_nodes.csv", "w") as f:
        f.write("Id\n")
        for node in discovered:
            f.write(f"{node}\n")
            
    # vychází, pak zkusme filter nebo nevím
    final_edges = []
    for (node_a, node_b) in discovered_edges:
        if node_a in discovered and node_b in discovered:
            final_edges.append({node_a, node_b})
        else:
            print(f"wtf co tu dela {node_a} nebo {node_b}")
            assert False
    return final_edges


def main():
    filename = "ba_model_5000_m2.csv"
    
    with open(filename, "r") as f:
        lines = f.readlines()
        lines = lines[1:]
        edges = [tuple(map(int, line.strip(" \n").split(';'))) for line in lines]
        g_snowball_adj_list = edge_graph_to_adj_list(edges)
    
    target_nodes = len(g_snowball_adj_list) * 0.15
    g_snowball = snowball_sampling(g_snowball_adj_list, target_nodes, 10)
    
    # count to be sure final output is correct num of nodes (15% of original)
    g_snowball_total_count = set()
    for edge in g_snowball:
        [vertex_a, vertex_b] = list(edge)
        g_snowball_total_count.update([vertex_a, vertex_b])

    # unique_nodes = set()
    # for edge in g_snowball:
    #     unique_nodes.update(edge)
    #     print(f"Unique nodes in exported edge list: {len(unique_nodes)}")
    
    print(f"Target nodes: {target_nodes}")
    print(f"Final node count: {len(g_snowball_total_count)}")
    export_edge_list(g_snowball, "snowball.csv")
    

if __name__ == "__main__":
    main()
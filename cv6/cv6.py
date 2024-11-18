import random

import numpy as np


# Náhodný generátor grafu - n je počet vrcholů, p je pravděpodobnost existence hrany
def g_np(n, p):
    graph = {i: set() for i in range(n)}

    # Procházení všech možných dvojic vrcholů
    for i in range(n):
        # od i + 1, abychom nezahrnuli hrany vícekrát
        for j in range(i + 1, n):
            if random.random() < p:
                graph[i].add(j)
                # graph[j].add(i)

    return graph

def average_degree(graph):
    return sum(len(neighbors) for neighbors in graph.values()) / len(graph)


def export_edge_list(graph, filename):
    with open(filename, "w") as f:
        f.write("source;target\n")
        for node, neighbors in graph.items():
            for neighbor in neighbors:
                f.write(f"{node};{neighbor}\n")


def export_node_list(graph, filename):
    with open(filename, "w") as f:
        f.write("Id\n")
        for node, neighbors in graph.items():
            f.write(f"{node}\n")


def export_as_matrix(graph, filename):
    l = len(graph)
    matrix = np.zeros((l, l))
    
    for node, neighbors in graph.items():
        for neighbor in neighbors:
            matrix[node, neighbor] = 1

    with open(filename, "w") as f:
        f.write(";" + ";".join(str(i) for i in range(l)) + "\n")
        for i, row in enumerate(matrix):
            f.write(str(i) + ";")
            f.write(";".join(str(cell) for cell in row) + "\n")
            
            
def export_adjacency_list(graph, filename):
    with open(filename, "w") as f:
        for node, neighbors in graph.items():
            f.write(f"{node}{';' if len(neighbors) != 0 else ''}{';'.join(str(neighbor) for neighbor in neighbors)}\n")
            
            
def gen(n, p, name):
    graf = g_np(n, p)
    print(f"Množství hran: {sum(len(neighbors) for neighbors in graf.values())}")
    print(f"Průměrný stupeň: {average_degree(graf)}")

    export_node_list(graf, f"{name}_nodes.csv")
    # export_as_matrix(graf, f"{name}.csv")
    export_edge_list(graf, f"{name}_edges.csv")

def main():
    n = 550
    
    p = 1. / 550.
    gen(n, p, "graf1")
    
    p = 0.001
    gen(n, p, "graf_maly")
    
    p = 0.0001
    gen(n, p, "graf_mini")
    
    p = 0.1
    gen(n, p, "graf_maxi")
    
    p = 0.01
    gen(n, p, "graf_velky")
    


if __name__ == "__main__":
    main()
    
    

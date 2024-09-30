import math
import os
import sys

f = open("KarateClub.csv", "r")
content = f.read()

lines = content.split('\n')
values = [a.split(';') for a in lines if a]

incidences = {}

for i, (a, b) in enumerate(values):
    ak = int(a)
    bk = int(b)

    # a
    if ak not in incidences:
        incidences[ak] = []
    incidences[ak].append(bk)

    # b
    if bk not in incidences:
        incidences[bk] = []
    incidences[bk].append(ak)

vertices = len(incidences)

def print_matrix(matrix):
    for a in adj_matrix:
        for b in a:
            print(f"\t{b}", end="")
        print()

print("adjacency list")
for i, (key, l) in enumerate(incidences.items()):
    print(f"{key}: {l}")

print("\n\n")
print("matice sousednosti")
adj_matrix = [[math.inf] * vertices for _ in range(vertices)]
for i in range(vertices):
    adj_matrix[i][i] = 0

for i, (key, l) in enumerate(incidences.items()):
    for l_another in l:
        adj_matrix[key - 1][l_another - 1] = 1
        adj_matrix[l_another - 1][key - 1] = 1

print_matrix(adj_matrix)

print("\n\n")
print("floyd warshall")
for k in range(vertices):
    for i in range(vertices):
        for j in range(vertices):
            adj_matrix[i][j] = min(adj_matrix[i][j], adj_matrix[i][k] + adj_matrix[k][j])

print_matrix(adj_matrix)


print("\n\n")
print("closeness centrality")

# shortest_paths = {}
# for i in range(vertices):
#     for j in range(i+1, vertices):
#         shortest_paths[(i, j)] = adj_matrix[i][j]

# better calculation
mean_distance = [sum(a) for a in adj_matrix]
closeness_centrality = {i: vertices / mean_distance[i] for i in range(vertices)}
for i, cc in closeness_centrality.items():
    print(f"{i + 1}: {cc:.5f}")

print("\n\n")
# print("min distance {}".format(min([a for a in [min(a) for a in adj_matrix] if a != 2^32 - 1])))
print("average distance {}".format((sum(mean_distance) * 0.5) / (0.5 * (vertices * (vertices - 1)))))
print("diametr {}".format(max(max(adj_matrix))))
print("done")

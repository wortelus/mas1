import os

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

print("adjacency list")
for i, (key, l) in enumerate(incidences.items()):
    print(f"{key}: {l}")

print("\n\n")
print("matice sousednosti")
adj_matrix = [[0] * vertices for _ in range(vertices)]
for i, (key, l) in enumerate(incidences.items()):
    for l_another in l:
        adj_matrix[key - 1][l_another - 1] = 1
        adj_matrix[l_another - 1][key - 1] = 1

for a in adj_matrix:
    for b in a:
        print(f"\t{b}", end="")
    print()


print("\n\n")
print("tabulka klíču, četností, relativní četností")

degree = {key: len(l) for (i, (key, l)) in enumerate(incidences.items())}
degree_count = {i: 0 for i in range(1, vertices+1)}
for _, (key, deg) in enumerate(degree.items()):
    degree_count[deg] += 1

for _, (key, deg_count) in enumerate(degree_count.items()):
    if deg_count != 0:
        print(f"{key}: {deg_count}\t rel. č.: {deg_count/vertices}")



print("\n\n")
print("min, avg, max")
print(f"min: {min(degree.values())}")
print(f"avg: {float(sum(degree.values())) / float(vertices)}")
print(f"max: {max(degree.values())}")

import numpy as np
import matplotlib.pyplot as plt
fig = plt.figure(figsize = (7, 5))
plt.bar(list(degree_count.keys()), list(degree_count.values()))
plt.xlim(0, 20)
plt.xticks(np.arange(1 - 1, 20 + 2, 2))

plt.show()

print("done")


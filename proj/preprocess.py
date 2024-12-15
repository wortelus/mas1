from scipy.io import mmread

matrix = mmread("web-indochina-2004/web-indochina-2004.mtx")

# with open('graph_edges.csv', 'w') as f:
#     f.write('Source,Target\n')
#     for i, j in zip(*matrix.nonzero()):
#         f.write(f'{i + 1},{j + 1}\n')

# Sparse nebo Dense ?
is_sparse = hasattr(matrix, 'format')
print(f"Is sparse: {is_sparse}")
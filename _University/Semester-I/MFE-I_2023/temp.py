import numpy as np

# Create the matrices
S = np.array([[0], [0], [0], [0], [0]], dtype=np.int32)
A = np.array([[1], [1], [0], [0], [0]], dtype=np.int32)
B = np.array([[1], [1], [1], [0], [0]], dtype=np.int32)
C = np.array([[0], [1], [1], [1], [0]], dtype=np.int32)
D = np.array([[0], [1], [1], [0], [1]], dtype=np.int32)
E = np.array([[0], [0], [0], [1], [1]], dtype=np.int32)
T = np.array([[0], [0], [0], [1], [1]], dtype=np.int32)

new_matrix = np.hstack((A, B, C, D, E), dtype=np.int32)

print(new_matrix)

import numpy as np

conect = np.array([
  [0, 0, 5, 2],
  [1, 0, 6, 3],
  [2, 0, 7, 4],
  [3, 0, 8, 0],
  [0, 1, 9, 6],
  [5, 2, 10, 7],
  [6, 3, 11, 8],
  [7, 4, 12, 0],
  [0, 5, 13, 10],
  [9, 6, 14, 11],
  [10, 7, 15, 12],
  [11, 8, 16, 0],
  [0, 9, 0, 14],
  [13, 10, 0, 15],
  [14, 11, 0, 16],
  [15, 12, 0, 0],
])

nn = len(conect)

cc = np.array([
  [1, 100],
  [1, 75],
  [1, 75],
  [1, 0],
  [1, 100],
  [0,0],
  [0, 0],
  [1, 0],
  [1, 100],
  [0, 0],
  [0, 0],
  [1, 0],
  [1, 100],
  [1, 25],
  [1, 25],
  [1, 0]
])

A = np.zeros((nn, nn))
b = np.zeros((nn, 1))

bloco = [1, 1, 1, 1]

for e in range(nn):
  if (cc[e, 0] == 0):
    A[e, e] = -4
    for j in range(4):
      A[e,conect[e, j]-1] = bloco[j]
  else:
    A[e, e] = 1
    b[e, 0] = cc[e, 1]

x = np.linalg.solve(A, b)

AA = np.array([
  [-4, 1, 1, 0],
  [1, -4, 0, 1],
  [1, 0, -4, 1],
  [0, 1, 1, -4]
])

bb = np.array([
  [-125],
  [-25],
  [-175],
  [-75]
])

xx = np.linalg.solve(AA, bb)

print("x")
print(x)
print("xx")
print(xx)
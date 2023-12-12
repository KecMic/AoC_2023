#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm

"""
orientation:
          , N
         /|\
          | 
  W <-----+-----> E
          |
         \|/
          ' S

pipes:
|   N <-> S
-   W <-> E
L   N <-> E     90°
J   N <-> W
7   S <-> W
F   S <-> E
.   ground (no pipe)
S   starting pos

e.g.:
   . . . . .
   . F - 7 .
   . | . | .
   . L - J .
   . . . . .

possible valid (4-)neighbors (current pos: S==i,j==y,x, next pos: #):

   . . .    . | .    # 7 .    . F #
   . S .    . S .    . S .    . S .    NORTH
   . . .    . . .    . . .    . . .

   . . .    . . .    . . .    . . #
   . S .    . S -    . S 7    . S J    EAST
   . . .    . . .    . . #    . . .

   . . .    . . .    . . .    . . .
   . S .    . S .    . S .    . S .
   . . .    . | .    # J .    . L #    SOUTH

   . . .    . . .    . . .    # . .
   . S .    - S .    F S .    L S .    WEST
   . . .    . . .    # . .    . . .

   if i-2 >= 0 and a[i-1,j] == '|':
      next = i-2,j
   if i-1 >= 0 and j-1 >= 0 and a[i-1,j] == '7':
      next = i-1,j-1
   if i-1 >= 0 and j+1 < W and a[i-1,j] == 'F':
      next = i-1,j+1
   
   if j+2 < W and a[i,j+1] == '-':
      next = i,j+2
   if j+1 < W and i+1 < H and a[i,j+1] == '7':
      next = i+1,j+1
   if j+1 < W and i-1 >= 0 and a[i,j+1] == 'J':
      next = i-1,j+1
   
   if i+2 < H and a[i+1,j] == '|':
      next = i+2,j
   if i+1 < H and j-1 >= 0 and a[i+1,j] == 'J':
      next = i+1,j-1
   if i+1 < H and j+1 < W and a[i+1,j] == 'L':
      next = i+1,j+1
   
   if j-2 >= 0 and a[i,j-1] == '-':
      next = i,j-2
   if j-1 >= 0 and i+1 < H and a[i,j-1] == 'F':
      next = i-1,j+1
   if j-1 >= 0 and i-1 >= 0 and a[i,j-1] == 'L':
      next = i-1,j-1

"""

"""
   functions check_next_pos_*(i, j, a, H, W):
      i, j: curren pos
      a: array
      H, W: height (y-extend), width (x-extend) of array a
      returns next pos as (i_next, j_next) if a valid pos was found, else None
"""
def check_next_pos_NORTH(i, j, a, H, W):
   if i-2 >= 0 and a[i-1,j] == '|': return i-2,j
   if i-1 >= 0 and j-1 >= 0 and a[i-1,j] == '7': return i-1,j-1
   if i-1 >= 0 and j+1 < W and a[i-1,j] == 'F': return i-1,j+1
   return None
def check_next_pos_EAST(i, j, a, H, W):
   if j+2 < W and a[i,j+1] == '-': return i,j+2
   if j+1 < W and i+1 < H and a[i,j+1] == '7': return i+1,j+1
   if j+1 < W and i-1 >= 0 and a[i,j+1] == 'J': return i-1,j+1
   return None
def check_next_pos_SOUTH(i, j, a, H, W):
   if i+2 < H and a[i+1,j] == '|': return i+2,j
   if i+1 < H and j-1 >= 0 and a[i+1,j] == 'J': return i+1,j-1
   if i+1 < H and j+1 < W and a[i+1,j] == 'L': return i+1,j+1
   return None
def check_next_pos_WEST(i, j, a, H, W):
   if j-2 >= 0 and a[i,j-1] == '-': return i,j-2
   if j-1 >= 0 and i+1 < H and a[i,j-1] == 'F': return i-1,j+1
   if j-1 >= 0 and i-1 >= 0 and a[i,j-1] == 'L': return i-1,j-1
   return None


sample_input_1_clean = [
".....\n",
".S-7.\n",
".|.|.\n",
".L-J.\n",
".....\n",
]
sample_input_1_noisy = [
"-L|F7\n",
"7S-7|\n",
"L|7||\n",
"-L-J|\n",
"L|-JF\n",
]
sample_input_2_clean = [
"..F7.\n",
".FJ|.\n",
"SJ.L7\n",
"|F--J\n",
"LJ...\n",
]
sample_input_2_noisy = [
"7-F7-\n",
".FJ|7\n",
"SJLL7\n",
"|F--J\n",
"LJ.LJ\n",
]

def arr_from_data(data):
   H, W = len(data), len(data[0])
   arr = np.chararray((H,W), unicode=True) # unicode=True, so it doesn' use byte-strings b'.', but plain strings '.'
   arr[:] = '.'
   for i in range(H):
      arr[i,:] = list(data[i])
   return arr

def find_starting_pos(arr):
   # returns (si, sj), the 2D starting index
   return np.where(arr.find('S')==0)

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   H, W = len(data), len(data[0])
   print(f"H, W: {H}, {W}")
   arr = arr_from_data(data)
   si, sj = find_starting_pos(arr)
   print(arr)
   print(f"starting @{arr[si,sj]}, located at i,j==y,x:", si, sj)

   def find_neighbors(u,mat):
      # 4-neighbors
      Ny,Nx = mat.shape
      neighbors = []
      if u[1] > 0    and mat[u[0]  ,u[1]-1] in ['-','F', 'L']: neighbors.append((u[0]  ,u[1]-1))  # L
      if u[1] < Nx-1 and mat[u[0]  ,u[1]+1] in ['-','7', 'J']: neighbors.append((u[0]  ,u[1]+1))  # R
      if u[0] > 0    and mat[u[0]-1,u[1]]   in ['|','7', 'F']: neighbors.append((u[0]-1,u[1]  ))  # U
      if u[0] < Ny-1 and mat[u[0]+1,u[1]]   in ['|','J', 'L']: neighbors.append((u[0]+1,u[1]  ))  # D
      return neighbors
   
   def Dijkstra(mat, src_idx):
      print(f"-- Dijkstra --")
      print(f"src_idx: {src_idx}")
      src_idx = src_idx[0][0], src_idx[1][0]
      print(f"src_idx: {src_idx}")
      # distances to src
      dist = np.ones(mat.shape, dtype=int)
      dist[:] = np.prod(mat.shape)*100 # np.inf
      dist[src_idx[0],src_idx[1]] = 0
      # previous node of mat[j,i] as (i,j)
      prev = np.ones(mat.shape, dtype=object)
      prev[:] = -1
      # queue
      #Q = [((i,j),v) for (i,j),v in np.ndenumerate(dist)]
      Q = [(src_idx,0)]

      H, W = mat.shape
      a = mat
      while Q:
         Q = [((i,j), dist[i,j]) for (i,j),v in Q] # recompute dist-vals, as Q works with indices, but we update dist
         Q = sorted(Q, reverse=True, key=lambda x: x[1]) # imitate prio-Q: sort so that smallest dist[i,j] is at back of list
         u, val = Q.pop()
         i, j = u
         valid_neighbors = find_neighbors(u,mat,)
         for n in valid_neighbors:
            alternative = dist[u[0],u[1]] + 1
            if alternative < dist[n[0],n[1]]:
               dist[n[0],n[1]] = alternative
               prev[n[0],n[1]] = u[0], u[1]
               if n in [q[0] for q in Q]:
                  # if n already in Q => decrease_prio (as my Q contains indices, no need to change element of Q directly)
                  pass
               else:
                  # if n not already in Q => add_with_prio
                  Q.append((n,-1)) # -1 doesn't matter, as we update at beginning of loop
      return dist,prev
   

   dist, prev = Dijkstra(arr, [si,sj])
   print(dist)
   print(prev)
   print(dist == np.prod(arr.shape)*100)
   dist[dist == np.prod(arr.shape)*100] = -1
   print(dist)
   print(np.max(dist))

   res = np.max(dist)
   if part2:
      print("_"*60)
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input_1_clean, part2=False)
   #solve(sample_input, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_10.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      #solve(file_data, part2=True)

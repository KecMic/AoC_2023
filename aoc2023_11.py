#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm
from aoc2023_10 import arr_from_data
from copy import deepcopy

sample_input = [
"...#......\n",
".......#..\n",
"#.........\n",
"..........\n",
"......#...\n",
".#........\n",
".........#\n",
"..........\n",
".......#..\n",
"#...#.....\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   H, W = len(data), len(data[0])
   print(f"H, W: {H}, {W}\n")
   arr = arr_from_data(data)
   
   def find_empty_rows(arr):
      rows_no_galax = []
      for i,l in enumerate(arr):
         if '#' not in ''.join(l):
            rows_no_galax.append(i)
      return rows_no_galax
         
   rows_no_galax = find_empty_rows(arr)
   cols_no_galax = find_empty_rows(arr.T)

   arr_framed = np.chararray((H+2,W+2), unicode=True)
   arr_framed[:] = '~'
   arr_framed[1:-1,1:-1] = arr
   [print(''.join(l)) for l in arr_framed]; print()
   for r in rows_no_galax:
      arr_framed[r+1,0] = '>'
      arr_framed[r+1,-1] = '<'
   for c in cols_no_galax:
      arr_framed[0,c+1] = 'v'
      arr_framed[-1,c+1] = '^'
   [print(''.join(l)) for l in arr_framed]; print()

   if part2:
      y_list, x_list = np.where(arr == '#')
      coords = [[y,x] for y,x in zip(y_list, x_list)]
      print("coords:", coords)
      N = len(coords)
      N_pairs = (N*(N-1))//2 # N choose 2
      print(f"N pairs: {N_pairs}")

      print("rows_no_galax:", rows_no_galax)
      print("cols_no_galax:", cols_no_galax)
      expansion_value = 1000000 # 2 -> 374, 10 -> 1030, 100 -> 8410, 1000000 -> 790194712336
      offset = expansion_value-1
      print("expansion_value, offset:", expansion_value, offset)
      
      coords = sorted(coords, key=lambda x: x[0]) # sort by y
      print("coords sorted by y:", coords)
      y_offsets = np.zeros(len(coords), dtype=int)
      for r in rows_no_galax:
         for i in range(len(coords)):
            coord_y = coords[i][0]
            if coord_y > r:
               y_offsets[i] += offset
      for i in range(len(coords)):
         coords[i][0] += y_offsets[i]
      print("coords after going row-by-row:", coords)
      
      coords = sorted(coords, key=lambda x: x[1]) # sort by x
      print("coords sorted by x:", coords)
      x_offsets = np.zeros(len(coords), dtype=int)
      for c in cols_no_galax:
         for i in range(len(coords)):
            coord_x = coords[i][1]
            if coord_x > c:
               x_offsets[i] += offset
      for i in range(len(coords)):
         coords[i][1] += x_offsets[i]
      print("coords after going col-by-col:", coords)

      shortest_paths = []
      for i in range(len(coords)):
         for j in range(i+1,len(coords)):
            d = np.sum(np.abs(np.array(coords[i]) - np.array(coords[j])))
            shortest_paths.append(d)
      res = np.sum(shortest_paths)

   else:
      # new dims: H + len(rows_no_galax), W + len(cols_no_galax)
      H_new, W_new = H + len(rows_no_galax), W + len(cols_no_galax)
      arr_expanded = np.chararray((H_new,W_new), unicode=True)
      arr_expanded[:] = '~'
      [print(''.join(l)) for l in arr_expanded]; print()

      #expand_arr_rows(arr_expanded, arr, rows_no_galax, cols_no_galax):
      offset = 0
      i = 0
      while i < H_new:
         print("i",i)
         if i in np.array(rows_no_galax) + offset:
            arr_expanded[[i,i+1],:-len(cols_no_galax)] = arr[i-offset,:]
            i += 1
            offset += 1
         else:
            arr_expanded[i,:-len(cols_no_galax)] = arr[i-offset,:]
         i += 1
      [print(''.join(l)) for l in arr_expanded]; print()

      #expand_arr_rows(arr_expanded.T, arr.T, cols_no_galax):
      offset = 0
      i = 0
      arr = deepcopy(arr_expanded)
      while i < W_new:
         if i in np.array(cols_no_galax) + offset:
            arr_expanded.T[[i,i+1],:] = arr.T[i-offset,:]
            i += 1
            offset += 1
         else:
            arr_expanded.T[i,:] = arr.T[i-offset,:]
         i += 1
      [print(''.join(l)) for l in arr_expanded]; print()

      x_list, y_list = np.where(arr_expanded == '#')
      coords = [[x,y] for x,y in zip(x_list, y_list)]
      print(coords)
      N = len(coords)
      N_pairs = (N*(N-1))//2 # N choose 2
      print(f"N pairs: {N_pairs}")
      shortest_paths = []
      for i in range(N):
         for j in range(i+1,N):
            d = np.sum(np.abs(np.array(coords[i]) - np.array(coords[j])))
            shortest_paths.append(d)
      res = np.sum(shortest_paths)

   if part2:
      print("_"*60)
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   #solve(sample_input, part2=False)
   solve(sample_input, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_11.txt', 'r') as f:
      file_data = f.readlines()
      #solve(file_data, part2=False)
      solve(file_data, part2=True)

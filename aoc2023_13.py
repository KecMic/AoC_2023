#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm
from aoc2023_10 import arr_from_data

sample_input = [
"#.##..##.\n",
"..#.##.#.\n",
"##......#\n",
"##......#\n",
"..#.##.#.\n",
"..##..##.\n",
"#.#.##.#.\n",
"\n",
"#...##..#\n",
"#....#..#\n",
"..##..###\n",
"#####.##.\n",
"#####.##.\n",
"..##..###\n",
"#....#..#\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print(data)
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))
   
   # add [] to the end for easier subsequent parsing
   if data[-1] != []:
      data.append("")
   print("data for parsing:")
   nums_fw = len(str(len(data)))
   num_spaces = 1
   border = '-'*(len(data[0]) + nums_fw + num_spaces)
   print(border)
   [print(f"{i:{nums_fw}}" + " "*num_spaces + l) for i,l in enumerate(data)]
   print(border)

   # split individual fields, with individual H,W
   fields = [] # list of fields
   field_dims = [] # list of [H,W]
   print(f"data contains {len(data)} rows")
   i, row_start = 0, 0
   while i < len(data):
      if len(data[i]) == 0: # found "", which was a '\n' before splitting
         print("row_start, row_end:", row_start, i)
         d = data[row_start:i]
         #print("d:\n", d)
         H, W = len(d), len(d[0])
         arr = arr_from_data(d)
         fields.append(arr)
         field_dims.append([H, W])
         #print(f"H, W: {H}, {W}, arr:\n",arr)
         row_start = i + 1
      i += 1
   print("="*60)
   
   reflection_lines_vertical = [[] for i in range(len(fields))]
   reflection_lines_horizontal = [[] for i in range(len(fields))]
   for n_field, (field, (H,W)) in enumerate(zip(fields, field_dims)):
      print(f"field {n_field+1}/{len(fields)} with H,W={H},{W}")
      max_half_width_vertical = W//2
      max_half_width_horizontal = H//2
      print(f"max_half_width_horizontal, max_half_width_vertical: {max_half_width_horizontal}, {max_half_width_vertical}")
      # vertical reflection line
      """
      # 9 columns: max_half_width_vertical == 4, 8 checks
      # 123456789
      1 => 1 -- 2
      2 => 1,2 -- 3,4
      3 => 1,2,3 -- 4,5,6
      4 => 1,2,3,4 -- 5,6,7,8
      5 => 2,3,4,5 -- 6,7,8,9
      6 => 4,5,6 -- 7,8,9
      7 => 6,7 -- 8,9
      8 => 8 -- 9
      """
      """
      # 10 columns: max_half_width_vertical == 5, 9 checks
      # 123456789x
      1 => 1 -- 2
      2 => 1,2 -- 3,4
      3 => 1,2,3 -- 4,5,6
      4 => 1,2,3,4 -- 5,6,7,8
      5 => 1,2,3,4,5 -- 6,7,8,9,10
      6 => 3,4,5,6 -- 7,8,9,10
      7 => 5,6,7 -- 8,9,10
      8 => 7,8 -- 9,10
      9 => 9 -- 10
      """
      for i in range(W-1):
         if i+1 <= max_half_width_vertical:
            r1 = np.arange(1, i+1+1)
            r2 = np.arange(i+1+1, i+1+1+len(r1))
         else:
            if W%2==0: # W even
               s = 1+(i-max_half_width_vertical)*2 + 2
            else: # W odd
               s = 1+(i-max_half_width_vertical)*2 + 1
            r1 = np.arange(s, i+1+1)
            r2 = np.arange(i+1+1, i+1+1+len(r1))
         #print(f"r1,r2: {r1},{r2}")
         
         all_cols_same = True
         for c1,c2 in zip(reversed(r1),r2): # c1,c2 are column indices
            #print(f"c1,c2: {c1},{c2}")
            #if not np.all(field[:,c1-1] == field[:,c2-1]):
            if np.any(field[:,c1-1] != field[:,c2-1]):
               #print(field[:,c1-1])
               #print(field[:,c2-1])
               #print("c1 != c2: ", [c1,c2])
               all_cols_same = False
               break
         if all_cols_same:
            reflection_lines_vertical[n_field].append([r1,r2])
      print()

      # horizontal reflection line
      for i in range(H-1):
         if i+1 <= max_half_width_horizontal:
            r1 = np.arange(1, i+1+1)
            r2 = np.arange(i+1+1, i+1+1+len(r1))
         else:
            if W%2==0: # W even
               s = 1+(i-max_half_width_horizontal)*2 + 2
            else: # W odd
               s = 1+(i-max_half_width_horizontal)*2 + 1
            r1 = np.arange(s, i+1+1)
            r2 = np.arange(i+1+1, i+1+1+len(r1))
         #print(f"r1,r2: {r1},{r2}")
         
         all_cols_same = True
         for c1,c2 in zip(reversed(r1),r2): # c1,c2 are row indices here...
            #print(f"c1,c2: {c1},{c2}")
            #if not np.all(field[:,c1-1] == field[:,c2-1]):
            if np.any(field[c1-1,:] != field[c2-1,:]):
               #print(field[:,c1-1])
               #print(field[:,c2-1])
               #print("c1 != c2: ", [c1,c2])
               all_cols_same = False
               break
         if all_cols_same:
            reflection_lines_horizontal[n_field].append([r1,r2])
      print()

      print(f"field {n_field+1}/{len(fields)} reflection_lines_vertical:")
      for p in reflection_lines_vertical[n_field]:
         print(f"\t{p[0]} -- {p[1]}")
      print(f"field {n_field+1}/{len(fields)} reflection_lines_horizontal:")
      for p in reflection_lines_horizontal[n_field]:
         print(f"\t{p[0]} -- {p[1]}")
      print()

   def generate_vertical_border_arr(arr, H, W):
      arr_framed = np.empty((H+4,W), dtype='str')
      arr_framed[:] = ' '
      arr_framed[2:-2,:] = arr
      #print("arr_framed.dtype:", arr_framed.dtype)
      #print(arr_framed)
      if W < 10:
         for i in range(W):
            arr_framed[[0,-1],i] = str(i+1)
      return arr_framed
   
   def generate_horizontal_border_arr(arr, H, W):
      arr_framed = np.empty((H,W+4), dtype='str')
      arr_framed[:] = ' '
      arr_framed[:,2:-2] = arr
      #print("arr_framed.dtype:", arr_framed.dtype)
      #print(arr_framed)
      if H < 10:
         for i in range(H):
            arr_framed[i,[0,-1]] = str(i+1)
      return arr_framed

   for n_field, (field, (H,W)) in enumerate(zip(fields, field_dims)):
      print(f"field {n_field+1}/{len(fields)} with H,W={H},{W}:")
      print(f"  contains {len(reflection_lines_vertical[n_field])} VERTICAL reflection lines")
      print(f"  contains {len(reflection_lines_horizontal[n_field])} HORIZONTAL reflection lines")

      arr_framed = generate_vertical_border_arr(field, H, W)
      if reflection_lines_vertical[n_field]:
         for r1,r2 in reflection_lines_vertical[n_field]:
            arr_framed[[1,-2],r1[-1]-1] = '>'
            arr_framed[[1,-2],r2[ 0]-1] = '<'
      #print('-'*len(arr_framed[0]))
      #[print(''.join(l)) for l in arr_framed]
      #print('-'*len(arr_framed[0]))
      #print()

      arr_framed = generate_horizontal_border_arr(field, H, W)
      if reflection_lines_horizontal[n_field]:
         for r1,r2 in reflection_lines_horizontal[n_field]:
            arr_framed[r1[-1]-1,[1,-2]] = 'v'
            arr_framed[r2[ 0]-1,[1,-2]] = '^'
      #print('-'*len(arr_framed[0]))
      #[print(''.join(l)) for l in arr_framed]
      #print('-'*len(arr_framed[0]))
      #print()
   print()

   # compute result
   res = 0
   for i in range(len(fields)):
      for r1,r2 in reflection_lines_vertical[i]:
         #print("vertical:", r1[-1])
         res += r1[-1]
      for r1,r2 in reflection_lines_horizontal[i]:
         #print("horizontal:", r1[-1])
         res += r1[-1] * 100

   if part2:
      print("_"*60)
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input, part2=False)
   #solve(sample_input, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_13.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      #solve(file_data, part2=True)

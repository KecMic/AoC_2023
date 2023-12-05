#!/usr/bin/env python3

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1.axes_divider import make_axes_locatable

sample_input = [
"467..114..\n",
"...*......\n",
"..35..633.\n",
"......#...\n",
"617*......\n",
".....+.58.\n",
"..592.....\n",
"......755.\n",
"...$.*....\n",
".664.598..\n",
]

def get_dat_from_list(data):
   H, W = len(data), len(data[0])
   dat = np.zeros(H*W)
   i = 0
   for l in data:
      for c in l:
         if c.isdigit(): dat[i] = 0
         elif c == '.': dat[i] = 1
         else: dat[i] = 2
         i += 1
   dat = dat.reshape((H,W))
   return dat

def show_data(dat):
   fig,ax = plt.subplots()
   fig.suptitle("numbers (0), '.' (1), symbols (2)")
   cax = make_axes_locatable(ax).append_axes('right', size='5%', pad='10%')
   im = ax.imshow(dat, cmap=plt.cm.get_cmap('turbo', 3)) # inferno, jet, Purples, turbo, bone
   #im = ax.imshow(dat, cmap=ListedColormap(['r','g','b'])) # rgb
   fig.colorbar(im, cax=cax, ticks=np.arange(np.min(dat), np.max(dat)+1, 1))
   plt.show()

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   dat = get_dat_from_list(data)
   print(f"dat, shape={dat.shape}, size={dat.size}")
   show_data(dat)
   #exit()

   H, W = len(data), len(data[0])
   print(f"H, W = {H}, {W}")
   
   nums = []
   syms = []
   for i,line in enumerate(data):
      nums_in_line = []
      syms_in_line = []
      pos_start, pos_end = -1, -1
      for j,c in enumerate(line):
         if c.isdigit():
            if pos_start == -1:
               pos_start = j
            if j == W-1 and pos_start != -1:
               # when at the last char in line that is a digit, must treat this here!
               p = [pos_start, W] # interval [s,e)
               nums_in_line.append(p)
               pos_start = -1
         else:
            pos_end = j
            if pos_start != -1:
               p = [pos_start, pos_end] # interval [s,e)
               """
               a number is represented by
                  [i, pos_start, pos_end], where i is the line_idx (i might be implicit via position in list)
               all neighbors of a number:
                  # line_idx, char_idx (starting from left, going clockwise)
                  # => chars to check in same line 'line_idx'
                     (line_idx, pos_start-1), (line_idx, pos_end+1)
                  # => chars to check in line above 'line_idx-1'
                     (line_idx-1, pos_start-1) ... (line_idx-1, pos_end+1)
                  # => chars to check in line below 'line_idx+1'
                     (line_idx+1, pos_start-1) ... (line_idx+1, pos_end+1)
               """
               nums_in_line.append(p)
               pos_start = -1
            if c != '.':
               syms_in_line.append(j)
      nums.append(nums_in_line)
      syms.append(syms_in_line)
      print(f"line {i} contains nums {nums_in_line}")
      print(f"line {i} contains syms {syms_in_line}")
   print(f"nums: {nums}")
   print(f"syms: {syms}")
   
   all_nums = [data[i][n[0]:n[1]] for i,nums_in_line in enumerate(nums) for n in nums_in_line]
   print(f"all found nums: {all_nums}")
   print(f"all nums summed up: {np.sum([int(n) for n in all_nums])}")

   def find_adjacent_syms(i, num, syms, H, W):
      # i: line_idx, num: number in format [s,e), syms: all symbols, H: height, W: width
      s, e = num
      adjacent_syms = []
      print(f"\n[s,e): [{s},{e}) ({data[i][num[0]:num[1]]})")
      if s-1 >= 0 and s-1 in syms[i]:
         print("to the left")
         adjacent_syms.append([i,s-1])
      if e < W and e in syms[i]:
         print("to the right")
         adjacent_syms.append([i,e])
      if i-1 >= 0:
         for x in range(s-1, e+1):
            #print(f"i-1: {i-1}")
            if x >= 0 and x < W and x in syms[i-1]:
               adjacent_syms.append([i-1,x])
      if i+1 < H:
         for x in range(s-1, e+1):
            #print(f"i+1: {i+1}")
            if x >= 0 and x < W and x in syms[i+1]:
               adjacent_syms.append([i+1,x])
      return adjacent_syms

   part_nums = []
   for i,nums_in_line in enumerate(nums):
      for n in nums_in_line:
         adjacent_syms = find_adjacent_syms(i, n, syms, H, W)
         if len(adjacent_syms) > 0:
            print(f"line {i} :: number {data[i][n[0]:n[1]]} has adjacent syms: ", end='')
            for s in adjacent_syms:
               print(f"{data[s[0]][s[1]]}, ", end='')
            print()
            part_nums.append(data[i][n[0]:n[1]])
   print(f"part_nums ({len(part_nums)} nums): {part_nums}")
   res = np.sum([int(s) for s in part_nums])

   #unique_part_nums = np.unique([int(s) for s in part_nums])
   #res = np.sum(unique_part_nums)

   if part2:
      def find_adjacent_nums(line_idx, char_idx):
         # line_idx: row, char_idx: col
         line_indices = [line_idx-1, line_idx, line_idx+1]
         adjacent_nums = []
         for i in line_indices:
            nums_in_line = nums[i]
            for n in nums_in_line:
               s, e = n
               num = data[i][s:e]
               if i == line_idx and (e == char_idx or (s in [char_idx-1, char_idx+1])): # same line
                  adjacent_nums.append([i, num])
               elif i != line_idx and ((e-1 in [char_idx-1, char_idx, char_idx+1]) or (s in [char_idx-1, char_idx, char_idx+1]) or (s<char_idx-1 and e-1>char_idx+1)): # above or below
                  adjacent_nums.append([i, num])
         return adjacent_nums

      print("="*60)
      gear_ratios = []
      for i,syms_in_line in enumerate(syms):
         #print(f"line {i} :: syms: {syms_in_line}")
         for sym_idx in syms_in_line:
            sym = data[i][sym_idx]
            if sym == '*':
               print(f"line {i} contains '*' @ idx {sym_idx}")
               adjacent_nums = find_adjacent_nums(i, sym_idx)
               print(f"  adjacent nums: {adjacent_nums}")
               if len(adjacent_nums) == 2:
                  print(f"  ~~> gear found")
                  gear_ratio = np.prod([int(n) for _,n in adjacent_nums])
                  gear_ratios.append(gear_ratio)
      res = np.sum(gear_ratios)
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
   with open('input_03.txt', 'r') as f:
      file_data = f.readlines()
      #solve(file_data, part2=False)
      solve(file_data, part2=True)

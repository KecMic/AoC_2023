#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm

sample_input = [
"0 3 6 9 12 15\n",
"1 3 6 10 15 21\n",
"10 13 16 21 30 45\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   next_vals = []
   for l in tqdm(data):
      nums = np.array([int(v) for v in l.split()])
      last_vals = [nums[-1]]
      print(f"nums: {nums}")
      while not np.all(nums==0):
         nums = np.diff(nums)
         last_vals.append(nums[-1])
         print(f"diff: {nums}")
      print(f"last_vals: {last_vals}")
      next_val = np.sum(last_vals)
      next_vals.append(next_val)
   
   res = np.sum(next_vals)

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
   with open('input_09.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      #solve(file_data, part2=True)

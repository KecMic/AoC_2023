#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm

sample_input = [
"Time:      7  15   30\n",
"Distance:  9  40  200\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   if part2:
      split_line = lambda l: [int(''.join(l.strip().split(":")[1].split()))]
   else:
      split_line = lambda l: list(map(int, l.strip().split(":")[1].split()))
   ts = split_line(data[0])
   ds = split_line(data[1])
   print("ts:", ts)
   print("ds:", ds)
   ways_to_win = []
   for t,d in zip(ts,ds):
      print("t, d:", t, d)
      wins = 0
      for t_hold in tqdm(range(1,t)):
         t_travel = t - t_hold
         dd = t_hold * t_travel
         if dd > d: wins += 1
      ways_to_win.append(wins)
   print("ways_to_win:", ways_to_win)

   res = np.prod(ways_to_win)

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
   with open('input_06.txt', 'r') as f:
      file_data = f.readlines()
      #solve(file_data, part2=False)
      solve(file_data, part2=True)

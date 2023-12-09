#!/usr/bin/env python3

import numpy as np
from tqdm import tqdm

"""
     R      L
AAA --> CCC --> ZZZ

"""
sample_input = [
"RL\n",
"\n",
"AAA = (BBB, CCC)\n",
"BBB = (DDD, EEE)\n",
"CCC = (ZZZ, GGG)\n",
"DDD = (DDD, DDD)\n",
"EEE = (EEE, EEE)\n",
"GGG = (GGG, GGG)\n",
"ZZZ = (ZZZ, ZZZ)\n",
]

"""
     L      L       R   #  L       L        R
AAA --> BBB --> AAA --> BBB --> AAA --> BBB --> ZZZ

"""
sample_input_2 = [
"LLR\n",
"\n",
"AAA = (BBB, BBB)\n",
"BBB = (AAA, ZZZ)\n",
"ZZZ = (ZZZ, ZZZ)\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[2]))
   [print(l) for l in data]
   print('-'*len(data[2]))

   RL_seq, network = data[0], data[2:]
   print(f"RL_seq: {RL_seq}")
   print(f"network: {network}")

   m = {}
   for line in network:
      l = line.split("=")
      k = l[0].strip()
      v = [v.strip() for v in l[1].strip()[1:-1].split(",")]
      print(f"k,v: {k},{v}")
      m[k] = v
   print("m:", m)
   
   k = 'AAA'
   target = 'ZZZ'
   found_target = False
   i = 0
   N = len(RL_seq)
   map_RL = {'L':0,'R':1}
   while True:
      rl = map_RL[RL_seq[i%N]]
      k = m[k][rl]
      if k == 'ZZZ':
         break
      i += 1
   
   num_steps = i+1
   print(f"taken steps: {num_steps}")

   res = []
   if part2:
      print("_"*60)
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input, part2=False)
   solve(sample_input_2, part2=False)
   #solve(sample_input, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_08.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      #solve(file_data, part2=True)

#!/usr/bin/env python3

import numpy as np

"""
map:
destination_range_start  source_range_start  range_length

seed-to-soil map:
50 98 2     => src_range: [98,98+2), dst_range: [50,50+2)
            => diff := dst-src == 50-98 == -48
52 50 48    => src_range: [50,50+48), dst_range: [52,52+48)
            => diff := dst-src == 52-50 == 2

soil-to-fertilizer map:
0 15 37     => src_range: [15,15+37), dst_range: [0,0+37)
            => diff := dst-src == 0-15 == -15
37 52 2     => src_range: [52,52+2), dst_range: [37,37+2)
            => diff := dst-src == 37-52 == -15
39 0 15     => src_range: [0,0+15), dst_range: [39,39+15)
            => diff := dst-src == 39-0 == 39

=> seed number 98 <==> soil number 50
=> save as data structure:
      [
         # src-range  # diff
         [[98,98+2)   , -48]
         [[50,50+48)  , 2]
      ]

TODO
- for each seed, find its location number
- res = min(all_location_numbers)

e.g.:
seed 79
   => 79 in range [52,52+48) => 79+2==81
   => 81 in no range => 81
"""
sample_input = [
"seeds: 79 14 55 13\n",
"\n",
"seed-to-soil map:\n",
"50 98 2\n",
"52 50 48\n",
"\n",
"soil-to-fertilizer map:\n",
"0 15 37\n",
"37 52 2\n",
"39 0 15\n",
"\n",
"fertilizer-to-water map:\n",
"49 53 8\n",
"0 11 42\n",
"42 0 7\n",
"57 7 4\n",
"\n",
"water-to-light map:\n",
"88 18 7\n",
"18 25 70\n",
"\n",
"light-to-temperature map:\n",
"45 77 23\n",
"81 45 19\n",
"68 64 13\n",
"\n",
"temperature-to-humidity map:\n",
"0 69 1\n",
"1 0 69\n",
"\n",
"humidity-to-location map:\n",
"60 56 37\n",
"56 93 4\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   seeds = [int(v) for v in data[0].split(":")[1].split()]
   print(f"seeds: {seeds}")
   maps = []   
   i = 1
   while i < len(data):
      l = data[i]
      #if len(l) == 0:
      #   i += 1
      #   continue
      if len(l) > 0 and l[-1] == ":":
         i += 1
         m = []
         print("-"*30)
         while i < len(data) and data[i] != "":
            nums = [int(v) for v in data[i].split()]
            src_range = [nums[1], nums[1]+nums[2]]
            diff = nums[0]-nums[1]
            print(f"src_range: {src_range}, diff: {diff}")
            m.append([src_range, diff])
            i += 1
         maps.append(m)
      i += 1
   
   print("-"*30)
   print(f"seeds: {seeds}")
   print(f"maps: {maps}")
   
   def print_maps(maps):
      n_chars = 20
      print("\nmaps (src-range, diff):")
      print("~"*n_chars)
      for m in maps:
         for r,d in m:
            print(f"{r}, {d}")
         print("~"*n_chars)
      print()
   print_maps(maps)

   locations = []
   for s in seeds:
      for m in maps:
         for r,d in m:
            if s >= r[0] and s < r[1]:
               s += d
               break
      locations.append(s)
   
   for s,l in zip(seeds, locations):
      print(f"seed {s} -> location {l}")
   res = np.min(locations)

   if part2:
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
   with open('input_05.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      #solve(file_data, part2=True)

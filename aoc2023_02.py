#!/usr/bin/env python3

import numpy as np


sample_input = [
"Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green\n",
"Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue\n",
"Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red\n",
"Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red\n",
"Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green\n",
]


def solve(data, part2=False):
   print(f"data: {data}")
   ids = []
   for l in data:
      line = l.strip().split(":")
      print("line:", [line])
      id = line[0].split(" ")[1]
      subsets = line[1].split(";")
      #print("subsets:", subsets)
      game_rounds = []
      for s in subsets:
         pairs = [e.split() for e in s.split(",")]
         game_rounds.append(pairs)
      print("id:", id)
      print("game_rounds:", game_rounds)
      is_possible = True
      for r in game_rounds:
         for p in r:
            if p[1] == "red" and int(p[0]) > 12: is_possible = False; break
            if p[1] == "green" and int(p[0]) > 13: is_possible = False; break
            if p[1] == "blue" and int(p[0]) > 14: is_possible = False; break
      if is_possible: ids.append(int(id))
   
   print("possible ids:", ids)
   res = np.sum(ids)
   if part2:
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input, part2=False)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_02.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)

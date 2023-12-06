#!/usr/bin/env python3

import numpy as np

sample_input = [
"Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53\n",
"Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19\n",
"Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1\n",
"Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83\n",
"Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36\n",
"Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11\n",
]

def solve(data, part2=False):
   data = [l.strip() for l in data] # remove '\n'
   print("data:")
   print('-'*len(data[0]))
   [print(l) for l in data]
   print('-'*len(data[0]))

   nums = []
   for l in data:
      line_nums = l.split(":")[1].split("|")
      winning_nums, my_nums = line_nums[0].split(), line_nums[1].split()
      print(f"winning_nums, my_nums:\n{winning_nums}, {my_nums}")
      nums.append([winning_nums, my_nums])
   print(f"nums: {nums}")
   
   scores = []
   num_matches = []
   for l in nums:
      winning_nums, my_nums = l
      score = -1
      found_winner = False
      n_matches = 0
      for m in my_nums:
         if m in winning_nums:
            n_matches += 1
            if found_winner:
               score *= 2
            else:
               score = 1
               found_winner = True
      num_matches.append(n_matches)
      if found_winner:
         scores.append(score)
   print(f"all found scores: {scores}")
   res = np.sum([int(s) for s in scores])
   print(f"final score: {res}")

   if part2:
      print("="*60)
      N_cards = len(data)
      print(f"num of cards: {N_cards}")
      card_counts = {k: 1 for k in range(N_cards)}
      print(f"card_counts: {card_counts}")
      print(f"num_matches: {num_matches}")
      for i,m in enumerate(num_matches):
         if m > 0:
            add_counts = card_counts[i]
            copy_cards = np.arange(i+1, i+1+m)
            for c in copy_cards:
               card_counts[c] += add_counts
      print(f"card_counts: {card_counts}")

      res = np.sum([v for v in card_counts.values()])
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")

if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input, part2=False)
   solve(sample_input, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_04.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=False)
      solve(file_data, part2=True)

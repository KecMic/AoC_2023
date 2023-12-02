#!/usr/bin/env python3

import numpy as np

sample_input = [
"1abc2\n",
"pqr3stu8vwx\n",
"a1b2c3d4e5f\n",
"treb7uchet\n",
]

sample_input_2 = [
"two1nine\n",
"eightwothree\n",
"abcone2threexyz\n",
"xtwone3four\n",
"4nineeightseven2\n",
"zoneight234\n",
"7pqrstsixteen\n",
]

num_str2int = {
"one":   "1",
"two":   "2",
"three": "3",
"four":  "4",
"five":  "5",
"six":   "6",
"seven": "7",
"eight": "8",
"nine":  "9",
}


def solve(data, part2=False):
   print(f"data: {data}")
   nums = []
   for l in data:
      line = l.strip()
      # *** Part 2 - START ***
      if part2:
         print(f"before: {line}")
         """
         for k,v in num_str2int.items():
            print(f"{k} -> {v}")
            line = line.replace(k,v)
         """
         new_line = []
         i = 0
         while i < len(line):
            c = line[i]
            #print(f"c: {c}")
            if c.isdigit(): new_line.append(c); i += 1
            # why "-1" => https://www.reddit.com/r/adventofcode/comments/1884fpl/2023_day_1for_those_who_stuck_on_part_2/
            elif c == "o" and line[i:i+3] == "one":   new_line.append("1"); i += 3-1
            elif c == "t" and line[i:i+3] == "two":   new_line.append("2"); i += 3-1
            elif c == "t" and line[i:i+5] == "three": new_line.append("3"); i += 5-1
            elif c == "f" and line[i:i+4] == "four":  new_line.append("4"); i += 4-1
            elif c == "f" and line[i:i+4] == "five":  new_line.append("5"); i += 4-1
            elif c == "s" and line[i:i+3] == "six":   new_line.append("6"); i += 3-1
            elif c == "s" and line[i:i+5] == "seven": new_line.append("7"); i += 5-1
            elif c == "e" and line[i:i+5] == "eight": new_line.append("8"); i += 5-1
            elif c == "n" and line[i:i+4] == "nine":  new_line.append("9"); i += 4-1
            else: i += 1
         line = ''.join(new_line)
         print(f"after:  {line}")
      # 55362 (too large)
      # 55358 => YES!
      # *** Part 2 - END ***
      indices = []
      for i,c in enumerate(line):
         if c.isdigit():
            indices.append(i)
      n = line[indices[0]] + line[indices[-1]]
      num = int(n)
      nums.append(num)
      print(f"num: {num}")
   res = np.sum(nums)
   if part2:
      print(f"~~~~~~~~~> SOLUTION Part 2: {res}")
   else:
      print(f"~~~~~~~~~> SOLUTION Part 1: {res}")


if __name__ == "__main__":
   #––– sample input
   print("for sample input:")
   solve(sample_input)
   solve(sample_input_2, part2=True)
   #exit()

   #––– Part 1 and Part 2
   print("for input file:")
   with open('input_01.txt', 'r') as f:
      file_data = f.readlines()
      solve(file_data, part2=True)

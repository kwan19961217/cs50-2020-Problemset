import sys
import csv
import re
# check if DNA database and DNA sequence is included
if len(sys.argv) != 3:
    print("Usage: python dna.py data.csv sequence.txt")
    False
# open Database and save it in a list
with open(sys.argv[1], newline='') as csvfile:
    dnadb = csv.reader(csvfile)
    table = list(dnadb)
# sequence
count = []
row = len(table)
column = len(table[0])
# open Sequence and save it as a string
with open(sys.argv[2], "r") as file:
    sequence = file.read().replace('\n', '')
# count the number of repeated STR and put in a list called "count"
# the list is in order with the DNA database's first row
for i in range(1, column):
    # res is the repeated string
    res = max(re.findall('((?:' + re.escape(table[0][i]) + ')*)', sequence), key=len)
    count.append(int(len(res) / len(table[0][i])))
# compare count with databases
# match = 1 so that it matches the number of elements in a row (Name, STR1, STR2,...,)
match = 1
for h in range(1, row):
    for k in range(1, column):
        if int(count[k-1]) != int(table[h][k]):
            # reset the number of matched STR
            match = 1
            break
        else:
            match += 1
        if match == int(column):
            print(f"{table[h][0]}")
            quit()
if match != int(column):
    print("No match")

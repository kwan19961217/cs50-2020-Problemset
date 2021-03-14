# TODO
import sys
import csv
import cs50

# check if house is included
if len(sys.argv) != 2:
    print("Usage: python roster.py house")
    False
# link python program with db
db = cs50.SQL("sqlite:///students.db")
# print students
for row in db.execute("SELECT first, middle, last, birth FROM students WHERE house = ? ORDER BY last, first;", sys.argv[1]):
    # check if the student has a middle name
    if row['middle'] != None:
        print(f"{row['first']} {row['middle']} {row['last']}, {row['birth']}")
    else:
        print(f"{row['first']} {row['last']}, born {row['birth']}")

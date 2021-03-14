# TODO
import sys
import csv
import cs50

# Link python program with db
db = cs50.SQL("sqlite:///students.db")
# check if csv is imported
if len(sys.argv) != 2:
    print("Usage: python import.py csv")
    False
# read through the csv file
with open(sys.argv[1], "r") as students:
    reader = csv.DictReader(students, delimiter=",")
    # insert the csv details into the db
    for row in reader:
        # .split() means split the whole string into words
        if len(row["name"].split()) == 3:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       row["name"].split()[0], row["name"].split()[1], row["name"].split()[2], row["house"], row["birth"])
        elif len(row["name"].split()) == 2:
            db.execute("INSERT INTO students (first, middle, last, house, birth) VALUES(?, ?, ?, ?, ?)",
                       row["name"].split()[0], None, row["name"].split()[1], row["house"], row["birth"])

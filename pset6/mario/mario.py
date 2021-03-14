from cs50 import get_int
n = get_int("Height: ")
# set m for the #
m = 1
# ask until input is correct
while n > 8 or n < 1:
    n = get_int("Height: ")
# create variable temp for space at the left edge
temp = n
# check if input is correct
if(n <= 8 and n > 0):
    # nested loop for multiple rows
    for a in range(n):
        # for printig space at the left edge
        for a in range(temp - 1):
            print(" ", end="")
        # for #
        for a in range(m):
            print("#", end="")
        # for space in the middle
        print("  ", end="")
        # for # on the right side
        for a in range(m):
            print("#", end="")
        print("\n", end="")
        # change the variables to match the case in the next row
        m += 1
        temp -= 1

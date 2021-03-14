from cs50 import get_int
card = get_int("What's your credit card number?\n")
# check which digit is being checked
currentDigitPosition = 1
temp = card
doubleeven = 0
sum = 0
doublesum = 0
# assign length so that the loop does not need to calculate the length of the card number everytime
length = range(len(str(temp)))
for digit in length:
    # check if the the current digit's position is odd number from the last
    if(currentDigitPosition % 2 == 1):
        sum += temp % 10
    # check if even
    elif(currentDigitPosition % 2 == 0):
        doubleeven = temp % 10 * 2
        # int() because the return value of dividend from python will have decimal point
        sum += doubleeven % 10 + int(doubleeven / 10)
    temp = int(temp / 10)
    # change digit [position]
    currentDigitPosition += 1
    # check credit card type
if(sum % 10 == 0):
    if(int(card / 10000000000000) == 34 or int(card / 10000000000000) == 37):
        print("AMEX")
    elif(int(card / 100000000000000) > 50 and int(card / 100000000000000) < 56):
        print("MASTERCARD")
    elif(int(card / 1000000000000000) == 4 or int(card / 1000000000000) == 4):
        print("VISA")
else:
    print("INVALID\n")

from cs50 import get_string
text = get_string("Text: ")
letter = 0
# set word = 1 because word count is always higher than space character by 1
word = 1
sentence = 0
for a in range(len(text)):
    # count letter
    if (text[a] >= 'a' and text[a] <= 'z'):
        letter += 1
    elif (text[a] >= 'A' and text[a] <= 'Z'):
        letter += 1
    # count word
    elif (text[a] == ' '):
        word += 1
    # count sentence
    elif (text[a] == '.' or text[a] == '?' or text[a] == '!'):
        sentence += 1
# apply the formula
# round the index because int() alone will round down 
i = int(round(0.0588 * 100 * letter / word - 0.296 * 100 * sentence / word - 15.8))
# check the grade with index i
if (i < 1):
    print("Before Grade 1")
elif (i >= 16):
    print("Grade 16+")
else:
    print(f"Grade {i}")

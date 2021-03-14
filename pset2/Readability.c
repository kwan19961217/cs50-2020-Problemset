#include <stdio.h>
#include <cs50.h>
//<string.h> so that more function of data type is available
#include <string.h>
//<math.h> so that rounding off is available
#include <math.h>

int letter;
int word;
int sentence;

int main(void)
{
    string t = get_string("Text： ");
//For loop to count letter, word and sentence
    for (int i = 0; i < strlen(t); i++)
    {
        if (t[i] >= 'a' && t[i] <= 'z')
        {
            letter++;
        }
        else if (t[i] >= 'A' && t[i] <= 'Z')
        {
            letter++;
        }
        else if (t[i] == ' ')
        {
            word++;
        }
        else if (t[i] == '.' || t[i] == '?' || t[i] == '!')
        {
            sentence++;
        }
    }
//These are to calculate the index
//word + 1 because number of space between words is always less than number of words by 1
    float average_letter = (float) letter / ((float) word + 1) * 100;
    float average_sentence = (float) sentence / ((float) word + 1) * 100;
    float index = 0.0588 * average_letter - 0.296 * average_sentence - 15.8;
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
//round(index) to mathematically round off the index number, (int) is to transform the data type
    else if ((int) round(index) >= 16)
    {
        printf("Grade 16+\n");
    }
    else 
    {
        printf("Grade %d\n", (int) round(index));
    }
}

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    long card = get_long("What's your credit card number?");
    int currentDigitPos = 1;
//temp to replace card to avoid messing with the initial card number
    long temp;
//doubleeven stands for the multiple of two of the selected digits
    long doubleeven = 0;
//Checksum
    long sum = 0;
//For loop to check select every other digit
    for (temp = card; temp > 0; temp = temp / 10)
    {
        if (currentDigitPos % 2 == 0)
        {
            doubleeven = temp % 10 * 2;
//For loop to multiply the number and add the digits, int i = 0 to avoid messing with the current variable
            for (int i = 0; doubleeven > 0; doubleeven = doubleeven / 10)
            {
                sum += doubleeven % 10;
            }
        }
//Add the remaining digits
        if (currentDigitPos % 2 == 1)
        {
            sum += temp % 10;
        }
        currentDigitPos++;
    }
//Check which credit card number it is
    if (sum % 10 == 0)
    {
        if (card / 10000000000000 == 34 || card / 10000000000000 == 37)
        {
            printf("AMEX\n");
        }
        else if (card / 100000000000000 > 50 && card / 100000000000000 < 56)
        {
            printf("MASTERCARD\n");
        }
        else if (card / 1000000000000 == 4 || card / 1000000000000000 == 4)
        {
            printf("VISA\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

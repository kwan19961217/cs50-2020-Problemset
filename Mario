#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int h;
    do
    {
        h = get_int("height: ");
    }   
    while (h > 8 || h < 1);
//This for loop is to define how many times (how many rows)the whole loop is going to run.
//If h = 8, the whole loop will be executed 8 times( 1st: i = 0 < h = 8, 2nd: 1<8,...., 8th: 7<8 )
    for (int i = 0; i < h; i++)
    {
//This for loop is to decide how many " " for each row.
//For example, for the first loop (i = 0), since s = h-1 = 0, therefore the loop will not be executed, thus zero dot.
//For the second loop (i = 1), since s= h-1 =1, therefore the loop will be executed for once, thus one dot for the first row.
        for (int s = h - 1; s > i; s--)
        {
            printf(" ");
        }
//This for loop is to decide how many "#" for each row.
//For example, for the first loop (i = 0), since b < 1, therefore the loop will be excuted for once, thus one #.
        for (int b = 0; b < i + 1; b++)
        {
            printf("#");
        }
        printf("  ");
//This for loop is similar to the one with int b.
        for (int r = 0; r < i + 1; r++)
        {
            printf("#");
        }
        printf("\n");
    }
}

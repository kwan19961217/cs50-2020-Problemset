#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //This is to ask user's name
    string x = get_string("What's your name?\n");
    //This is to print their name
    printf("Hello, %s\n", x);
} 

#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(int argc, string argv[])
{
//check if there is a key
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
//check if the key contains all 26 letters
    else if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 letters.\n");
        return 1;
    }
    else
//check if the key has repeated value, the loop is to match first letter with the last letter,
//then first letter with the second last letter,...., second letter with the last letter,....,etc.
    {
        for (int i = 0; i < 26; i++)
        {
            for (int j = 25; i != j; j--)
            {
                if (argv[1][i] == argv[1][j])
                {
                    printf("Key should not have repeated values.\n");
                    return 1;
                }
            }
        }
//check if the characters in the key are all alphabet
        for (int i = 0; i < 26; i++)
        {
            if ((int)argv[1][i] < 65 || (int)argv[1][i] > 122)
            {
                printf("Key must not contain non-alphabetical value.\n");
                return 1;
            }
            else if ((int)argv[1][i] >= 91 && (int)argv[1][i] <= 96)
            {
                printf("Key must not contain non-alphabetical value.\n");
                return 1;
            }
        }
        string t = get_string("plaintext: ");
//string s so that it does not mess with the original message
        string s = t;
//convert all the letters to capital letters
        for (int i = 0; i < strlen(argv[1]); i++)
        {
            if (argv[1][i] >= 'a' && argv[1][i] <= 'z')
            {
                argv[1][i] = argv[1][i] - 32;
            }
        }
//map capital letter to ASCII table to find out the letters' position, then align it with the key
        for (int i = 0; i < strlen(t); i++)
        {
            if (t[i] >= 'A' && t[i] <= 'Z')
            {
                s[i] = t[i] + -65;
                s[i] = argv[1][(int) s[i]];
            }
//map lowercase letter to ASCII table to find out the letters' position, then align it with the key, and then map to ASCII table again
            else if (t[i] >= 'a' && t[i] <= 'z')
            {
                s[i] = t[i] + -97;
                s[i] = argv[1][(int) s[i]];
                s[i] = s[i] + 32;
            }
        }
        printf("ciphertext: %s\n", s);
        return 0;
    }
}

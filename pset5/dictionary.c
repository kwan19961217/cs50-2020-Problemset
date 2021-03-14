// Implements a dictionary's functionality

#include <stdbool.h>

#include "dictionary.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>
// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Number of buckets in hash table
const unsigned int N = 26;

// Hash table
node *table[N];

int i;
int number;

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    i = hash(word);
    if (table[i]->next != NULL)
    {
        node *cursor = NULL;
        for(cursor = table[i]->next; cursor != NULL; cursor = cursor->next)
        {
            //for words instead of character
            if (strlen(word) > 1)
            {
                //+1 for NULL terminator
                if (strncasecmp(cursor->word, word, strlen(word) + 1) == 0)
                {
                    return true;
                }
            }
            else
            {
                //hardcode these two because character does not have a NULL terminator
                if (*word == 'A' || *word == 'a' || *word == 'I' || *word == 'i')
                {
                    return true;
                }
            }
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // TODO
    int j = 0;
    //hash word according to the initial
    if(word[0] >= 'A' && word[0] <= 'Z')
    {
        j = word[0] - 65;
    }
    else if(word[0] >= 'a' && word[0] <= 'z')
    {
        j = word[0] - 97;
    }
    return j;
}

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // TODO
    // malloc for each table
    for (int j = 0; j < N; j++)
    {
        table[j] = malloc(sizeof(node));
        table[j]->next = NULL;
    }

    //open dictionary
    FILE *dict = fopen(dictionary, "r");
    if (dict == NULL)
    {
        return false;
    }
    int d = 0;
    char *word = malloc(LENGTH + 1);
    while(d != EOF)
    {
        //take words from dictionary and save in variable "word"
        d = fscanf(dict, "%s", word);
        if (d == 1)
        {
            i = hash(word);
            node *n = malloc(sizeof(node));
            if (n == NULL)
            {
                return 1;
            }
            //copy the word into the linked list
            strcpy(n->word, word);
            n->next = table[i]->next;
            table[i]->next = n;
            //word count
            number++;
        }
    }
    fclose(dict);
    free(word);
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    return number;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    for (int j = 0; j < 26; j++)
    {
        while (table[j]->next != NULL)
        {
            node *temp = table[j]->next;
            free(table[j]);
            table[j] = temp;
        }
        free(table[j]);
    }
    return true;
}

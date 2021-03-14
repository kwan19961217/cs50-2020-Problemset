#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;
int voter_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }
    
    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // TODO
    for (int i = 0; i < candidate_count; i++)
    {
// if name of voters' choice is same as candidate's name, vote + 1
        if (strcmp(name, candidates[i].name) == 0)
        {
            candidates[i].votes++;
            return true;

        }
    }
    return false;

}
// Print the winner (or winners) of the election
void print_winner(void)
{
    // TODO
    for (int j = 0; j < candidate_count - 1; j++)
    {
        for (int i = 0; i < candidate_count - 1; i++)
        {
            if (candidates[i].votes > candidates[i + 1].votes)
            {
// use temp_candidates to avoid messing with the original record
// use bubble sort because the max number of candidates is small 
                candidate temp_candidates = candidates[i];
                candidates[i] = candidates[i + 1];
                candidates[i + 1] = temp_candidates;
            }
        }
    }
// print max vote
    printf("%s\n", candidates[candidate_count - 1].name);
// print remaining candidates who has the same vote as the max vote candidate
    for (int i = candidate_count - 1; candidates[i].votes == candidates[i - 1].votes; i--)
    {
        if (candidates[i].votes == candidates[i - 1].votes)
        {
            printf("%s\n", candidates[i - 1].name);
        }
    }
    return;
}


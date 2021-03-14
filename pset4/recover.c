#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    //check argument
    if (argc != 2)
    {
        printf("Usage: ./recover image");
        return 1;
    }
    //Open file
    FILE *file = fopen(argv[1], "r");
    if (!file)
    {
        return 1;
    }
    //Read First 3 Bytes
    //set variable for the loop
    int first_file = 0;
    int file_count = 0;
    char *filename = malloc(sizeof(char) * 8);
    FILE *img = NULL;
    //Assign variable to store read bits
    unsigned char *bytes = malloc(sizeof(char) * 512);
    //use a loop to keep read and write
    //since fread can read the file one by one, we do not have to teach it how to look for the start of the second set of byte chunks
    //so does fwrite
    //fread == 1 means fread has not reached the end of the file yet
    while (fread(bytes, 512, 1, file) == 1)
    {
        //check if the byte chunk is a start of JPEG
        //0xf0 = 11110000
        //0xe0 = 11100000
        if (bytes[0] == 0xff && bytes[1] == 0xd8 && bytes[2] == 0xff && (bytes[3] & 0xf0) == 0xe0)
        {
            //since first file does not have a file to close beforehead, we have to treat it with a unique case
            if (first_file == 0)
            {
                first_file++;
            }
            else
            {
                //if it is not the first file, we have to close one before we starting writing to another file
                fclose(img);
            }
            //filename is a string we declared for the name of the file (e.g. 000.jpg) we are going to write into
            sprintf(filename, "%03i.jpg", file_count);
            //open a file (000.jpg) to write
            img = fopen(filename, "w");
            file_count++;
        }
        //After the first_file of JPEG is opened, we can start writing,
        //and if the header for the next bytes chunks is not the magic number, the above loop will be skipped 
        //and thus keep writing in the current file
        if (first_file == 1)
        {
            fwrite(bytes, 512, 1, img);
        }
    }
    fclose(img);
    fclose(file);
    free(bytes);
    free(filename);
}

#include "helpers.h"
#include "math.h"

// Convert image to grayscale
//All the dividend are with "." so that we can get a value with decimal point
// and then we have to round it off to get the most precise colour
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <  height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float temp = (image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.;
            image[i][j].rgbtRed = round(temp);
            image[i][j].rgbtGreen = image[i][j].rgbtRed;
            image[i][j].rgbtBlue = image[i][j].rgbtRed;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i <  height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float temp_Red = image[i][j].rgbtRed;
            float temp_Green = image[i][j].rgbtGreen;
            float temp_Blue = image[i][j].rgbtBlue;
            temp_Red = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            temp_Green = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            temp_Blue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;
            //Because Colours are from 0 to 255
            if (temp_Red > 255)
            {
                image[i][j].rgbtRed = 255;
            }
            else
            {
                image[i][j].rgbtRed = round(temp_Red);
            }
            if (temp_Green > 255)
            {
                image[i][j].rgbtGreen = 255;
            }
            else
            {
                image[i][j].rgbtGreen = round(temp_Green);
            }
            if (temp_Blue > 255)
            {
                image[i][j].rgbtBlue = 255;
            }
            else
            {
                image[i][j].rgbtBlue = round(temp_Blue);
            }
        }
    }
    return;
}

// Reflect image horizontally
// Replace the left value with the right value
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2 ; j++)
        {
            float temp_Red = image[i][j].rgbtRed;
            float temp_Green = image[i][j].rgbtGreen;
            float temp_Blue = image[i][j].rgbtBlue;
            image[i][j].rgbtRed = image[i][width - 1 - j].rgbtRed;
            image[i][width - 1 - j].rgbtRed = temp_Red;
            image[i][j].rgbtGreen = image[i][width - 1 - j].rgbtGreen;
            image[i][width - 1 - j].rgbtGreen = temp_Green;
            image[i][j].rgbtBlue = image[i][width - 1 - j].rgbtBlue;
            image[i][width - 1 - j].rgbtBlue = temp_Blue;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    float temp_Red[height][width];
    float temp_Green[height][width];
    float temp_Blue[height][width];
    //Corner Case
    //Add four values around
    //Top Left
    temp_Red[0][0] = (image[0][0].rgbtRed + image[0][1].rgbtRed + image[1][0].rgbtRed + image[1][1].rgbtRed) / 4.;
    temp_Green[0][0] = (image[0][0].rgbtGreen + image[0][1].rgbtGreen + image[1][0].rgbtGreen + image[1][1].rgbtGreen) / 4.;
    temp_Blue[0][0] = (image[0][0].rgbtBlue + image[0][1].rgbtBlue + image[1][0].rgbtBlue + image[1][1].rgbtBlue) / 4.;
    //Top Right
    temp_Red[0][width - 1] = (image[0][width - 1].rgbtRed + image[0][width - 2].rgbtRed + image[1][width - 1].rgbtRed +
                              image[1][width - 2].rgbtRed) / 4.;
    temp_Green[0][width - 1] = (image[0][width - 1].rgbtGreen + image[0][width - 2].rgbtGreen + image[1][width - 1].rgbtGreen +
                                image[1][width - 2].rgbtGreen) / 4.;
    temp_Blue[0][width - 1] = (image[0][width - 1].rgbtBlue + image[0][width - 2].rgbtBlue + image[1][width - 1].rgbtBlue +
                               image[1][width - 2].rgbtBlue) / 4.;
    //Bottom Left
    temp_Red[height - 1][0] = (image[height - 1][0].rgbtRed + image[height - 1][1].rgbtRed + image[height - 2][0].rgbtRed +
                               image[height - 2][1].rgbtRed) / 4.;
    temp_Green[height - 1][0] = (image[height - 1][0].rgbtGreen + image[height - 1][1].rgbtGreen + image[height - 2][0].rgbtGreen +
                                 image[height - 2][1].rgbtGreen) / 4.;
    temp_Blue[height - 1][0] = (image[height - 1][0].rgbtBlue + image[height - 1][1].rgbtBlue + image[height - 2][0].rgbtBlue +
                                image[height - 2][1].rgbtBlue) / 4.;
    //Bottom Right
    temp_Red[height - 1][width - 1] = (image[height - 1][width - 1].rgbtRed + image[height - 1][width - 2].rgbtRed +
                                       image[height - 2][width - 1].rgbtRed + image[height - 2][width - 2].rgbtRed) / 4.;
    temp_Green[height - 1][width - 1] = (image[height - 1][width - 1].rgbtGreen + image[height - 1][width - 2].rgbtGreen +
                                         image[height - 2][width - 1].rgbtGreen + image[height - 2][width - 2].rgbtGreen) / 4.;
    temp_Blue[height - 1][width - 1] = (image[height - 1][width - 1].rgbtBlue + image[height - 1][width - 2].rgbtBlue +
                                        image[height - 2][width - 1].rgbtBlue + image[height - 2][width - 2].rgbtBlue) / 4.;
    //Edge Case
    //Add six values around
    //Top Edge
    for (int i = 1; i < width - 1; i++)
    {
        temp_Red[0][i] = (image[0][i - 1].rgbtRed + image[0][i].rgbtRed + image[0][i + 1].rgbtRed + image[1][i - 1].rgbtRed +
                          image[1][i].rgbtRed + image[1][i + 1].rgbtRed) / 6.;
        temp_Green[0][i] = (image[0][i - 1].rgbtGreen + image[0][i].rgbtGreen + image[0][i + 1].rgbtGreen + image[1][i - 1].rgbtGreen +
                            image[1][i].rgbtGreen + image[1][i + 1].rgbtGreen) / 6.;
        temp_Blue[0][i] = (image[0][i - 1].rgbtBlue + image[0][i].rgbtBlue + image[0][i + 1].rgbtBlue + image[1][i - 1].rgbtBlue +
                           image[1][i].rgbtBlue + image[1][i + 1].rgbtBlue) / 6.;
    }
    //Left Edge
    for (int i = 1; i < height - 1; i++)
    {
        temp_Red[i][0] = (image[i - 1][0].rgbtRed + image[i][0].rgbtRed + image[i + 1][0].rgbtRed + image[i - 1][1].rgbtRed + 
                          image[i][1].rgbtRed + image[i + 1][1].rgbtRed) / 6.;
        temp_Green[i][0] = (image[i - 1][0].rgbtGreen + image[i][0].rgbtGreen + image[i + 1][0].rgbtGreen + image[i - 1][1].rgbtGreen +
                            image[i][1].rgbtGreen + image[i + 1][1].rgbtGreen) / 6.;
        temp_Blue[i][0] = (image[i - 1][0].rgbtBlue + image[i][0].rgbtBlue + image[i + 1][0].rgbtBlue + image[i - 1][1].rgbtBlue +
                           image[i][1].rgbtBlue + image[i + 1][1].rgbtBlue) / 6.;
    }
    //Right Edge
    for (int i = 1; i < height - 1; i++)
    {
        temp_Red[i][width - 1] = (image[i - 1][width - 1].rgbtRed + image[i][width - 1].rgbtRed + image[i + 1][width - 1].rgbtRed +
                                  image[i - 1][width - 2].rgbtRed + image[i][width - 2].rgbtRed + image[i + 1][width - 2].rgbtRed) / 6.;
        temp_Green[i][width - 1] = (image[i - 1][width - 1].rgbtGreen + image[i][width - 1].rgbtGreen + image[i + 1][width - 1].rgbtGreen +
                                    image[i - 1][width - 2].rgbtGreen + image[i][width - 2].rgbtGreen + 
                                    image[i + 1][width - 2].rgbtGreen) / 6.;
        temp_Blue[i][width - 1] = (image[i - 1][width - 1].rgbtBlue + image[i][width - 1].rgbtBlue + image[i + 1][width - 1].rgbtBlue +
                                   image[i - 1][width - 2].rgbtBlue + image[i][width - 2].rgbtBlue + image[i + 1][width - 2].rgbtBlue) / 6.;
    }
    //Bottom Edge
    for (int i = 1; i < width - 1; i++)
    {
        temp_Red[height - 1][i] = (image[height - 1][i - 1].rgbtRed + image[height - 1][i].rgbtRed + image[height - 1][i + 1].rgbtRed +
                                   image[height - 2][i - 1].rgbtRed + image[height - 2][i].rgbtRed + 
                                   image[height - 2][i + 1].rgbtRed) / 6.;
        temp_Green[height - 1][i] = (image[height - 1][i - 1].rgbtGreen + image[height - 1][i].rgbtGreen + 
                                     image[height - 1][i + 1].rgbtGreen +
                                     image[height - 2][i - 1].rgbtGreen + image[height - 2][i].rgbtGreen + 
                                     image[height - 2][i + 1].rgbtGreen) / 6.;
        temp_Blue[height - 1][i] = (image[height - 1][i - 1].rgbtBlue + image[height - 1][i].rgbtBlue + image[height - 1][i + 1].rgbtBlue +
                                    image[height - 2][i - 1].rgbtBlue + image[height - 2][i].rgbtBlue + 
                                    image[height - 2][i + 1].rgbtBlue) / 6.;
    }
    //Middle Case
    //Add all the nine values around
    for (int i = 1; i < height - 1; i++)
    {
        for (int j = 1; j < width - 1; j++)
        {
            temp_Red[i][j] = (image[i - 1][j - 1].rgbtRed + image[i - 1][j].rgbtRed + image[i - 1][j + 1].rgbtRed + image[i][j - 1].rgbtRed + 
                              image[i][j].rgbtRed + image[i][j + 1].rgbtRed + image[i + 1][j - 1].rgbtRed + 
                              image[i + 1][j].rgbtRed + image[i + 1][j + 1].rgbtRed) / 9.;
            temp_Green[i][j] = (image[i - 1][j - 1].rgbtGreen + image[i - 1][j].rgbtGreen + image[i - 1][j + 1].rgbtGreen + 
                                image[i][j - 1].rgbtGreen + image[i][j].rgbtGreen + image[i][j + 1].rgbtGreen + 
                                image[i + 1][j - 1].rgbtGreen + image[i + 1][j].rgbtGreen + 
                                image[i + 1][j + 1].rgbtGreen) / 9.;
            temp_Blue[i][j] = (image[i - 1][j - 1].rgbtBlue + image[i - 1][j].rgbtBlue + image[i - 1][j + 1].rgbtBlue + 
                               image[i][j - 1].rgbtBlue + image[i][j].rgbtBlue + image[i][j + 1].rgbtBlue + 
                               image[i + 1][j - 1].rgbtBlue + image[i + 1][j].rgbtBlue + 
                               image[i + 1][j + 1].rgbtBlue) / 9.;
        }
    }
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j].rgbtRed = round(temp_Red[i][j]);
            image[i][j].rgbtGreen = round(temp_Green[i][j]);
            image[i][j].rgbtBlue = round(temp_Blue[i][j]);
        }
    }
    return;
}

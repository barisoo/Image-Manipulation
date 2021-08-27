"""
Convert image to stylised dots according to the desired settings and color palette.
"""


"""
SETTINGS
"""
#input_img  specified in command line arg
r, dist = 20, 6 #radius of dots and distance between dots
max_dim = 100 #max dimension (resolution) of width or height 
thumbnail_size = (max_dim,max_dim)
output_img = "dots.png" #name of output image
colours = ['#f2d3bf','#231b10','#37556a','#f5f5ee', '#d17f76', '#9cb8cd', '#cca062'] #Color Palette (as hex)



"""
CODE EXECUTION
"""
import numpy as np
from os import listdir
from PIL import Image
from PIL import ImageDraw
import sys

def hex_to_rgb(color_string):
    h = color_string.lstrip('#')
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))

def get_average_color(pixels):
    """
    Take: list of RGBA or RGB pixel tuples. 
    Return: single averaged tuple of color
    """
    summation = np.array([0.0,0.0,0.0])
    for pixel in pixels:
        summation += np.array(pixel)
    summation /= len(pixels)
    return summation


def resize_big(big_in, big_out,thumbnail_size):
    """
    Take:
    big_in[string], the name/address of the input image
    big_out[string], the name/address of the resultant image
    thumbnail_size[tuple], the max dimensions of the resultant image
    
    Return: None
    """
    img = Image.open(big_in)
    img.thumbnail(thumbnail_size)
    img.save(big_out)
    return None



def most_similar_color(current_pixel, tile_colours): 
    """
    Take:
    current_pixel[tuple] and tile_dict[dict]
    
    Return:
    Most similar tile name[string]
    """
    current_min = 10**20 #max similar, min distance
    current_col = ""
    for colour in tile_colours:
        summation = 0
        for colour_index in range(len(colour)):
            summation += (colour[colour_index] - current_pixel[colour_index])**2
        if summation < current_min:
            current_min = summation
            current_col = colour
    return current_col

if __name__ == "__main__":
    tile_colours = [ hex_to_rgb(i) for i in colours]
    big_in  = sys.argv[-1]
    big_out =  big_in[:-4] + "_resized.png"
    resize_big(big_in, big_out,thumbnail_size)
    img = Image.open(big_out)
    width, height = img.size
    pixels = list(img.getdata())
    
    if type(pixels[0]) == int:
        pixels = [(i,i,i) for i in img.getdata()]
    
    selected_colours = []
    
    for pixel in pixels:
        selection = most_similar_color(pixel, tile_colours)
        selected_colours.append(selection)
    
    img2 = Image.new(mode="RGB", size=(width*2*(r+dist),height*2*(r+dist)))
    draw = ImageDraw.Draw(img2)
    
    for i in range(len(selected_colours)):
        x = 2*(r+dist)*(i%width) + 2 
        y =  2*(r+dist)*(i//width) + 2
        leftUpPoint = (x-r, y-r)
        rightDownPoint = (x+r, y+r)
        twoPointList = [leftUpPoint, rightDownPoint]
        draw.ellipse(twoPointList, fill=selected_colours[i])
    
    img2.save(output_img)

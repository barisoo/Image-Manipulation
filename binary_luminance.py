"""
Takes image as command line argument, creates ASCII-style art with 1s and 0s.

Creates a text file where the luminance of pixels is converted to 1s and 0s
Though additional numbers/characters could have been used, limiting it to 1s and 0s (and the absence of either) allowed the script to avoid becoming unnecessarily complex. I had seen ASCII style art as a kid and thought it was impressive, by limiting the art to the simplest form of computer data I felt it became symbolic of the pursuit to learn Comp Sci which I am undertaking.
"""

"""
SETTINGS - Edit the variables here to optimise the script!
"""

lower_ranges = {0:" ", 6000:"1",12000:"0"} #used for Girl with Pearl Earrings
max_dim = 300 #max dimension in width or height can be individually 
thumbnail_size = (max_dim,max_dim)
font_ratio  = 0.5 #width to height ratio of font used. Often this is around 0.5
print_luminance_range = True 


"""
CODE and EXECUTION
"""

from PIL import Image
import sys
import os


def calc_lumin(pixel):
    #Take RGBA tuple, returns Luminance
    R,G,B = pixel[0],pixel[1],pixel[2]
    return ( 0.299*(R**2) + 0.587*(G**2) + 0.114*(B**2) )**1/2

if __name__ == "__main__":
    input_img  = sys.argv[-1]
    img = Image.open(input_img)
    img_inter = sys.argv[-1][:-4]+"_inter.png"#intermediate 
    img.thumbnail(thumbnail_size)
    img.save(img_inter)
    #img.save(img_inter, dpi=(dpi_setting,dpi_setting))
    img = Image.open(img_inter)
    width, height = img.size
    new_image = img.resize((width, int(height*font_ratio)))
    new_image.save(img_inter)
    
    img = Image.open(img_inter)
    pixels = list(img.getdata())

    newpixels_str = ""
    lumins_all = []
    width, height = img.size
    pixel_count = 0
    for pixel in pixels:
        current = ""
        lumin = calc_lumin(pixel)
        lumins_all.append(lumin)
        for lower_bound in lower_ranges:
            if lumin > lower_bound:
                current = lower_ranges[lower_bound]
        newpixels_str += current
        pixel_count +=1 
        if pixel_count % width ==0:
            newpixels_str+="\n"
    
    #print(newpixels_str)
    print(newpixels_str)
    if print_luminance_range:
        print(min(lumins_all), max(lumins_all))
    filename = sys.argv[-1][:-4]+".txt"
    f = open(filename, "w+")
    f.write(newpixels_str)
    f.close()
    os.remove(img_inter)
    
    
    
    
    
    
    
    
    
    

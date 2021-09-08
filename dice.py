"""
Takes image as command line argument, creates an image that can be created using dice 
"""

"""
SETTINGS - Edit the variables here to optimise the script!
"""


max_dim = 100 #max dimension in width or height can be individually 
thumbnail_size = (max_dim,max_dim)
#----ALSO CHECK THE "DICE" SETTINGS IN THE PIXEL IMAGE CLASS!-----

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

class pixel_image:
    def __init__(self, img_intermediate, output_img_name):
        self.output_img = output_img_name
        self.img = Image.open(img_intermediate)
        self.pixels = list(img.getdata())
        self.og_width, self.og_height = self.img.size
        self.lumins_all = [calc_lumin(i) for i in self.pixels]
        self.sorted_lumins =  sorted(self.lumins_all)
        count = len(self.pixels)
        i1,i4,i5,i8 = (count//9),4*(count//9),5*(count//9),8*(count//9) 
        self.first, self.fourth, self.fifth, self.eighth = self.sorted_lumins[i1],self.sorted_lumins[i4],self.sorted_lumins[i8],self.sorted_lumins[i8]
        self.dice_width  = 3  #must match the width  of the dice described below
        self.dice_height = 3  #must match the height of the dice described below
        self.dice = {0: [[0,0,0],[0,0,0],[0,0,0]], self.first:[[0,0,0],[0,1,0],[0,0,0]], self.fourth: [[0,1,0],[1,0,1],[0,1,0]], self.fifth:[[1,0,1],[0,1,0],[1,0,1]], self.eighth:[[1,1,1],[1,1,1],[1,1,1]]}
        self.diced_pixels = [[0 for i in range(self.og_width*self.dice_width)] for j in range(self.og_height*self.dice_height) ]
        self.diced_pixels_singleArray = [];
        self.diced_pixel_sring = ""
        
    def get_dice(self, lumin):
        keys  = [i for i in self.dice]
        category = 0 #the range category that the lumin falls into
        for  key in keys:
            if lumin>key:
                category = key
        return self.dice[category]
    
    def place_dice(self):
        for pixel_index in range(len(self.pixels)):
            lumin = self.lumins_all[pixel_index]
            row_ind = (pixel_index // self.og_width)*self.dice_height
            col_start_ind = (pixel_index %  self.og_width)*self.dice_width
            dice2use = self.get_dice(lumin)
            for dice_row_ind in range(len(dice2use)):
                col_ind = col_start_ind
                dice_row = dice2use[dice_row_ind]
                for lumin in dice_row:
                    self.diced_pixels[row_ind][col_ind] = tuple(lumin*255 for i in range(3))
                    col_ind +=1
                row_ind +=1
            
    def write2image(self):
        for row_array in self.diced_pixels: 
            for pixel in row_array:
                self.diced_pixels_singleArray.append(pixel)
        img2 = Image.new(mode="RGB", size=(self.og_width*self.dice_width,self.og_height*self.dice_height))
        img2.putdata(data = self.diced_pixels_singleArray, scale = 1, offset= 0)
        img2.save(self.output_img)
        
    
    def main(self):
        self.place_dice()
        self.write2image()
        
        
        
            

if __name__ == "__main__":
    input_img  = sys.argv[-1]
    img = Image.open(input_img)
    img_inter = sys.argv[-1][:-4]+"_inter.png"#intermediate 
    img.thumbnail(thumbnail_size)
    img.save(img_inter)
    
    output_img_name  = sys.argv[-1][:-4]+"_final.png"
    
    diced_img = pixel_image(img_inter, output_img_name)
    diced_img.main()
    
    os.remove(img_inter)
    
    
    
    
    
    
    
    
    
    

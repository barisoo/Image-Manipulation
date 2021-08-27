"""
The idea behind this was to be able create game assets in the pixel art style from svg files. 
From a personal point of view, drawing in SVG (with the help of inkscape etc.) was easier than drawing directly to pixel art. 
There is also the benefit of being able to easily change the resolution of the image.
Minor editing may be required following the stylisation.
"""


import cairosvg
from PIL import Image
import sys

if __name__ == "__main__":
    input_svg  = sys.argv[-1]
    output_png =  input_svg[:-4] + ".png"
    print(f'File taken: {input_svg}')
    print(f'Saving output to: {output_png}')
    
    cairosvg.svg2png(url=input_svg, write_to=output_png,dpi=16)
    img = Image.open(output_png)
    pixels = list(img.getdata())

    newpixels = []
    for pixel in pixels:
        if pixel[-1] < 255 and sum(pixel[:-1])>0:
            newpixels.append((0,0,0,255))
        else:
            newpixels.append(pixel)

    img.putdata(newpixels)
    img.save(output_png)

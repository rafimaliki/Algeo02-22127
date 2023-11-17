from PIL import Image
import os
def convert_to_grayscale(input):
    image = Image.open(input)
    grayscale_image = image.convert("RGB")

    width, height = grayscale_image.size
    for x in range(width):
        for y in range(height):
            r, g, b = grayscale_image.getpixel((x, y))
            gray = int(0.299 * r + 0.587 * g + 0.114 * b)
            grayscale_image.putpixel((x, y), (gray,gray,gray))

    # grayscale_image.save(output)
    return grayscale_image

# dir = os.path.dirname(os.path.abspath(__file__))
# input = dir + "\input.jpg"  
# output = dir +"\output.jpg"  
# convert_to_grayscale(input, output)

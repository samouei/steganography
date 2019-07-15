
from PIL import Image
import numpy as np

def generate_matrix(color):
    """
    Generates a transformation matrix for the specified color.
    Inputs:
        color: string with exactly one of the following values:
               'red', 'blue', 'green', or 'none'
    Returns:
        matrix: a transformation matrix corresponding to
                deficiency in that color
    """
    # You do not need to understand exactly how this function works.
    if color == 'red':
        c = [[.567, .433, 0],[.558, .442, 0],[0, .242, .758]]
    elif color == 'green':
        c = [[0.625,0.375, 0],[ 0.7,0.3, 0],[0, 0.142,0.858]]
    elif color == 'blue':
        c = [[.95, 0.05, 0],[0, 0.433, 0.567],[0, 0.475, .525]]
    elif color == 'none':
        c = [[1, 0., 0],[0, 1, 0.],[0, 0., 1]]
    return c


def matrix_multiply(m1,m2):
    """
    Multiplies the input matrices.
    Inputs:
        m1,m2: the input matrices
    Returns:
        result: matrix product of m1 and m2
        in a list of floats
    """

    product = np.matmul(m1,m2)
    if type(product) == np.int64:
        return float(product)
    else:
        result = list(product)
        return result


def convert_image_to_pixels(image):
    """
    Takes an image (must be inputted as a string
    with proper file attachment ex: .jpg, .png)
    and converts to a list of tuples representing pixels.
    Each pixel is a tuple containing (R,G,B) values.

    Returns the list of tuples.

    Inputs:
        image: string representing an image file, such as 'lenna.jpg'
        returns: list of pixel values in form (R,G,B) such as
                 [(0,0,0),(255,255,255),(38,29,58)...]
    """
    
    # Open image
    im = Image.open(image) 
    
    # Get pixel values
    pixel_values = list(im.getdata())
    
    return pixel_values


def convert_pixels_to_image(pixels, size, mode):
    """
    Creates an Image object from a inputted set of RGB tuples.

    Inputs:
        pixels: a list of pixels such as the output of
                convert_image_to_pixels.
        size: a tuple of (width,height) representing
              the dimensions of the desired image. Assume
              that size is a valid input such that
              size[0] * size[1] == len(pixels).
        mode: 'RGB' or 'L' to indicate an RGB image or a 
              BW image, respectively
    returns:
        img: Image object made from list of pixels
    """
    
    # Create a new image (essentially an empty "canvas")
    image = Image.new(mode, size)
    
    # Copy pixel data to the image ("paint on blank canvas")
    image.putdata(pixels)
    
    return image

def apply_filter(pixels, color):
    """
    pixels: a list of pixels in RGB form, such as 
            [(0,0,0),(255,255,255),(38,29,58)...]
    color: 'red', 'blue', 'green', or 'none', must be a string representing 
           the color
    deficiency that is being simulated.
    returns: list of pixels in same format as earlier functions,
    transformed by matrix multiplication
    """
    
    # Create an empty list for storing filtered pixels
    filtered_pixels = []
    
    # Get color matrix (call generate_matrix function)
    color_matrix = generate_matrix(color)
    
    # Iterate through pixel values
    for p in pixels:
        
        # Transform/filter pixels using the color matrix (*returns a list of floats!*)
        filtered_pixel = matrix_multiply(color_matrix, p)
        
        # Create an empty list for storing int version of flitered pixels
        filtered_pixels_int = []
        
        # Get and store int values for filtered pixels
        for i in filtered_pixel:
            i = int(i)
            filtered_pixels_int.append(i)
        
        # Create and store tuples of filtered pixels
        filtered_pixels_tuple = tuple(filtered_pixels_int)
        filtered_pixels.append(filtered_pixels_tuple)
 
    return filtered_pixels        
    

def reveal_image(filename):
    """
    Extracts the single LSB (for a BW image) or the 2 LSBs (for a 
    color image) for each pixel in the input image. Hint: you can
    use a function to determine the mode of the input image (BW or
    RGB) and then use this mode to determine how to process the image.
    Inputs:
        filename: string, input BW or RGB file to be processed
    Returns:
        result: an Image object containing the hidden image
    """
     
    # Create and empty list for storing hidden image pixels
    hidden_image_pixels = []
    # Open image
    im = Image.open(filename)
    # Get list of pixel values
    image_pixels = convert_image_to_pixels(filename)
    # Get image mode
    image_mode = im.mode


    # For RGB (color) images:
    if image_mode == 'RGB':
        
        # Iterate through pixels
        for p in image_pixels:

            
            hidden_color_tuple_list = []
            # Iterate through R, G, B values
            for c in p:

                # Extract and map 2 LSBs
                hidden_c = int((c % 4) * (255 // 3))
                hidden_color_tuple_list.append(hidden_c)
         
            pixel_tuple = tuple(hidden_color_tuple_list)
            hidden_image_pixels.append(pixel_tuple)

    # For BW images:
    else:
        for p in image_pixels:
            
            # Extract and map single LSB
            hidden_p = (p % 2) * 255
            hidden_image_pixels.append(hidden_p)
        
    return convert_pixels_to_image(hidden_image_pixels, im.size, image_mode)


def main():
#    pass

    # Uncomment the following lines to test part 1

     im = Image.open('image_15.png')
     width, height = im.size
     pixels = convert_image_to_pixels('image_15.png')
     image = apply_filter(pixels,'none')
     im = convert_pixels_to_image(image, (width, height), 'RGB')
     im.show()
     new_image = apply_filter(pixels,'red')
     im2 = convert_pixels_to_image(new_image,(width,height), 'RGB')
     im2.show()

    # Uncomment the following lines to test part 2

     im3 = reveal_image('hidden1.bmp')
     im3.show()
     im4 = reveal_image('hidden2.bmp')
     im4.show()




if __name__ == '__main__':
    main()

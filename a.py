import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from PIL import Image


def intensity(image, grayscale_arrray):
    a=3
    b=2
    c=5
    d=4
    width, height = image.size
    intensity_array = np.zeros((height, width), dtype=np.uint8)
    for y in range(height-1):
        for x in range(width-1):
            intensity_array[y,x] = grayscale_arrray[y,x]*a+grayscale_arrray[y,x+1]*b+grayscale_arrray[y+1,x]*c+grayscale_arrray[y+1,x+1]*d

    return intensity_array


# Convert an RGB image to grayscale manually
def rgb_to_grayscale(image):
    width, height = image.size
    grayscale_array = np.zeros((height, width), dtype=np.uint8)
    
    # Loop through each pixel, calculate grayscale value
    for y in range(height):
        for x in range(width):
            r, g, b = image.getpixel((x, y))
            grayscale_value = int(0.2989 * r + 0.5870 * g + 0.1140 * b)
            grayscale_array[y, x] = grayscale_value
            
    return grayscale_array

# Modify grayscale array by adding a constant
def modify_grayscale_array(grayscale_array, operator, constant):
    # Initialize the modified array
    modified_array = np.zeros_like(grayscale_array)

    # Perform the operation based on the operator
    if operator == '+':
        modified_array = np.clip(grayscale_array + constant, 0, 255)  
    elif operator == '-':
        modified_array = np.clip(grayscale_array - constant, 0, 255)  
    elif operator == '*':
        modified_array = np.clip(grayscale_array * constant, 0, 255)  
    elif operator == '/':
        if constant != 0:
            modified_array = np.clip(grayscale_array / constant, 0, 255)  
        else:
            raise ValueError("Cannot divide by zero.")
    else:
        raise ValueError("Invalid operator. Use +, -, *, or /.")

    return modified_array

# Store grayscale array in a file
def save_grayscale_to_file(grayscale_array, filename="grayscale_values_file.txt"):
    np.savetxt(filename, grayscale_array, fmt='%d', delimiter=',')
    print(f"Grayscale values saved to {filename}")

def subtract_from_255(grayscale_array):
    modified_array = np.clip(255-grayscale_array, 0, 255)  # Clip to stay in valid range
    return modified_array

# Display the image using matplotlib
def display_image_from_array(image_array, cmap='gray'):
    plt.imshow(image_array, cmap=cmap, vmin=0, vmax=255)
    plt.axis('off')  # Hide axis
    plt.show()

# Main processing function
def process_image():
    # File selector dialog
    Tk().withdraw()  # Hide the root window
    image_path = askopenfilename()
    
    if not image_path:
        print("No file selected.")
        return
    
    try:
        # Load and display the image file path
        print(f"Selected file: {image_path}")
        image = Image.open(image_path)
        
        # Convert to grayscale and print array
        grayscale_array = rgb_to_grayscale(image)
        
        # Save grayscale array to a file
        save_grayscale_to_file(grayscale_array)
        display_image_from_array(grayscale_array)

        # Separate RGB channels
        r_channel, g_channel, b_channel = image.split()

        # Convert channels to numpy arrays
        r_array = np.array(r_channel)
        g_array = np.array(g_channel)
        b_array = np.array(b_channel)

        
        # User input for modifying grayscale image
        user_input = input("Enter an operation to modify the image (e.g., +2, *6): ")
        
        operator = user_input[0]  
        number = int(user_input[1:])

        # Modify grayscale array and show the image
        modified_array = modify_grayscale_array(grayscale_array, operator, number)
        subtract_array = subtract_from_255(grayscale_array)

        # Display modified grayscale and subtracted images
        display_image_from_array(modified_array)
        display_image_from_array(subtract_array)

        # Display the separate R, G, B channels
        display_image_from_array(r_array, cmap='Reds')
        display_image_from_array(g_array, cmap='Greens')
        display_image_from_array(b_array, cmap='Blues')
        display_image_from_array(intensity(image,grayscale_array))

    
    except Exception as e:
        print(f"Error processing the image: {e}")

# Call the function with file selector
process_image()

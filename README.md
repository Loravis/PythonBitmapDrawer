# Python Bitmap Drawer
This is the result of an IT school project. The task was to create a python class, that can create, load, edit and save bitmap (BMP) image files. 
The class is found in the *bitmap.py* file. *main.py* contains a script that I used to test the functionality of the Bitmap class. 

## How to use
```py
# Create a bitmap object containing data for an empty bitmap with a specified size
bmp = Bitmap(800, 600)

# Overwrite the stored image data with an existing bitmap file
bmp.load("file.bmp")

# Draw multiple shapes
bmp.draw_circle(100, 200, 50, 0xb342f5)
bmp.draw_rectangle(600, 300, 100, 10, 0x42f5bf)
bmp.draw_half_circle(100, 500, 50, False, 0x9ba322)

# Save the image data to a new file
bmp.save("new_file.bmp")
```
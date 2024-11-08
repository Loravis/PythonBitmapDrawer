# Bitmap example program

from bitmap import Bitmap as bmp

if __name__ == "__main__":
    try:
        # Create an empty 100x100 bitmap file and save it to test.bmp
        bitmap = bmp(100, 100)
        bitmap.save("test.bmp")

        # Load an existing bitmap file
        bitmap.load("LoadTest.bmp")
        
        # Draw several different shapes
        bitmap.draw_pokeball(400, 200, 100)
        bitmap.draw_circle(100, 200, 50, 0xb342f5)
        bitmap.draw_rectangle(600, 300, 100, 10, 0x42f5bf)
        bitmap.draw_half_circle(100, 500, 50, False, 0x9ba322)

        # Save the modified bitmap to a new file
        bitmap.save("LoadTestCopy.bmp")

    except Exception as err: print(err)

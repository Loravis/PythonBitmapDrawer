import math


class Header:
    def __init__(self, file_type: str, size: int, reserved: int, offbits: int):
        """Speichert die Headerdaten der Bitmap in einem Objekt."""
        self.type = file_type
        self.size = size
        self.reserved = reserved
        self.offbits = offbits


class Infoblock:
    def __init__(self, header_size: int, width: int, height: int,
                 planes: int, bit_count: int, compression: int,
                 image_size: int, x_pixels_per_meter: int,
                 y_pixels_per_meter: int, clr_used: int, clr_important: int):
        """Speichert die Infodaten der Bitmap in einem Objekt."""
        self.header_size = header_size
        self.width = width
        self.height = height
        self.planes = planes
        self.bit_count = bit_count
        self.compression = compression
        self.image_size = image_size
        self.x_pixels_per_meter = x_pixels_per_meter
        self.y_pixels_per_meter = y_pixels_per_meter
        self.clr_used = clr_used
        self.clr_important = clr_important


def hex_to_rgb(hex_color):
    """
    Converts HEX color codes into three RGB values
    """
    try:
        red = (hex_color >> 16) & 0xFF  
        green = (hex_color >> 8) & 0xFF  
        blue = hex_color & 0xFF  
        return (red, green, blue)
    except Exception as err: 
        raise Exception(f'There was an error converting the HEX value {hex_color} into an RGB color. Ensure that you\'ve provided a valid HEX color code.')

class Bitmap:
    @staticmethod
    def __read_int(byte_number, file):
        """Helper method, which reads a specified number of Bytes from an open File."""
        return int.from_bytes(file.read(byte_number), "little")

    def __init__(self, width: int, height: int):
        """Create a new, empty method with a specified width and height"""
        self.__header = Header("BM", 0, 0, 54)
        bit_count = 24
        self.__infoblock = Infoblock(40, width, height, 0, bit_count, 0,
                                     bit_count * width * height, 0,
                                     0, 0, 0)
        self.__pixels = []
        for y in range(1, self.__infoblock.height):
            row = []
            for x in range(1, self.__infoblock.width):
                blue = 0
                green = 0
                red = 0
                row.append((red, green, blue))
            div_four = 3 * self.__infoblock.width / 4
            self.__pixels.append(row)

    def load(self, file_path: str):
        """Loads an existing bitmap file"""
        with open(file_path, "rb") as bitmap:
            self.__header = Header(bitmap.read(2).decode("utf-8"),
                                   Bitmap.__read_int(4, bitmap),
                                   Bitmap.__read_int(4, bitmap),
                                   Bitmap.__read_int(4, bitmap))

            self.__infoblock = Infoblock(Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(2, bitmap),
                                         Bitmap.__read_int(2, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap),
                                         Bitmap.__read_int(4, bitmap))

            # Read pixels
            bitmap.seek(self.__header.offbits)
            self.__pixels = []
            for y in range(self.__infoblock.height):
                row = []
                for x in range(self.__infoblock.width): # TODO: fix
                    blue = Bitmap.__read_int(1, bitmap)
                    green = Bitmap.__read_int(1, bitmap)
                    red = Bitmap.__read_int(1, bitmap)
                    row.append((red, green, blue))
                div_four = 3 * self.__infoblock.width / 4
                if div_four.is_integer() is not True:
                    offset = (math.ceil(div_four) * 4) - (3 * self.__infoblock.width)
                    bitmap.seek(offset, 1)
                self.__pixels.append(row)


    
    def get_pixels(self):
        """Returns a 2D array containing pixel data."""
        return self.__pixels
    
    def get_pixel(self, x: int, y: int):
        """Returns a specific pixel's data"""
        return self.__pixels[y + 1][x - 1]

    def set_pixel(self, x: int, y: int, red: int, green: int, blue: int):
        """Modify the color of a specified pixel"""
        x = x - 1
        y = y - 1
        if 0 <= x <= self.__infoblock.width and 0 <= y <= self.__infoblock.height:
            if 0 <= red <= 255 and 0 <= green <= 255 and 0 <= blue <= 255:
                self.__pixels[len(self.__pixels) - 2 - y][x - 1] = (red, green, blue)
            else:
                raise ValueError(f'The specified color ({red}, {green}, {blue}) is not a valid RGB color.')
        else: 
            raise ValueError("The specified object does not fit into the bitmap of size " +  
                             f'{self.__infoblock.width}x{self.__infoblock.height}.')
        
    def draw_rectangle(self, upper_left_x: int, upper_left_y: int, width: int, height: int, color: int):
        rgb = hex_to_rgb(color)
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        for x in range(upper_left_x, width + upper_left_x):
            for y in range(upper_left_y, height + upper_left_y):
                self.set_pixel(x, y, red, green, blue)

    def draw_circle(self, center_x: int, center_y: int, radius: int, color: int):
        rgb = hex_to_rgb(color)
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        
        upper_left_x = center_x - radius + 1
        upper_left_y = center_y - radius + 1
        lower_right_x = center_x + radius
        lower_right_y = center_y + radius

        for x in range(upper_left_x, lower_right_x):
            for y in range(upper_left_y, lower_right_y):
                hyp = (center_x - x) * (center_x - x) + (center_y - y) * (center_y - y)
                if hyp <= (radius * radius):
                    self.set_pixel(x, y, red, green, blue)

    def draw_half_circle(self, center_x: int, center_y: int, radius: int, upper_half: bool, color: int):
        rgb = hex_to_rgb(color)
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        if upper_half:
            upper_left_x = center_x - radius + 1
            upper_left_y = center_y - radius + 1
            lower_right_x = center_x + radius
            lower_right_y = center_y
        else:
            upper_left_x = center_x - radius + 1
            upper_left_y = center_y + 1
            lower_right_x = center_x + radius
            lower_right_y = center_y + radius

        for x in range(upper_left_x, lower_right_x + 1):
            for y in range(upper_left_y, lower_right_y + 1):
                hyp = (center_x - x) * (center_x - x) + (center_y - y) * (center_y - y)
                if hyp <= (radius * radius):
                    self.set_pixel(x, y, red, green, blue)

    def draw_pokeball(self, center_x: int, center_y: int, radius: int):
        self.draw_circle(center_x, center_y, radius, 0x000000) # Draw the outer black border of the pokeball
        self.draw_half_circle(center_x, center_y, int(radius * 0.93), True, 0xff0000) # Draw the upper half circle of the pokeball
        self.draw_half_circle(center_x, center_y, int(radius * 0.93), False, 0xffffff) # Draw the lower half circle of the pokeball
        center_line_multiplier = 0.05 # The height of the horizontal line in the middle, in percentage
        self.draw_rectangle(center_x - radius + 1, int(center_y - radius * center_line_multiplier), radius * 2, int(radius * center_line_multiplier * 2), 0x000000)
        self.draw_circle(center_x, center_y, int(radius * 0.3), 0x000000)
        self.draw_circle(center_x, center_y, int(radius * 0.23), 0xffffff)

    def save(self, path: str):
        """
        Saves currently loaded bitmap data into a bitmap file 
        """
        with open(path, "wb") as bitmap:
            header = self.__header
            infoblock = self.__infoblock

            bitmap.write(header.type.encode("utf-8"))
            bitmap.write(header.size.to_bytes(4, byteorder="little"))
            bitmap.write(header.reserved.to_bytes(4, byteorder="little"))
            bitmap.write(header.offbits.to_bytes(4, byteorder="little"))

            bitmap.write(infoblock.header_size.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.width.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.height.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.planes.to_bytes(2, byteorder="little"))
            bitmap.write(infoblock.bit_count.to_bytes(2, byteorder="little"))
            bitmap.write(infoblock.compression.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.image_size.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.x_pixels_per_meter.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.y_pixels_per_meter.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.clr_used.to_bytes(4, byteorder="little"))
            bitmap.write(infoblock.clr_important.to_bytes(4, byteorder="little"))

            bitmap.seek(self.__header.offbits)
            for y in range(self.__infoblock.height):
                row = self.__pixels[y - 1]
                for x in range(self.__infoblock.width):
                    pixel = row[x - 1]
                    blue = pixel[2]
                    green = pixel[1]
                    red = pixel[0]
                    bitmap.write(blue.to_bytes(1, byteorder="little"))
                    bitmap.write(green.to_bytes(1, byteorder="little"))
                    bitmap.write(red.to_bytes(1, byteorder="little"))

                div_four = 3 * self.__infoblock.width / 4
                if div_four.is_integer() is not True:
                    offset = (math.ceil(div_four) * 4) - (3 * self.__infoblock.width)
                    bitmap.seek(offset, 1)

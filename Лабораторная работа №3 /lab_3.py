from math import sin, pi
from struct import pack

width = 200
height = 200
t = 0
step = 0.01
pixels = []
x_min = float('inf')
y_min = float('inf')

while t <= 2 * pi:
    x = round(sin(t+pi/2) , 2)
    if x <= x_min:
        x_min = x
    y = round(sin(2*t), 2)
    if y <= y_min:
        y_min = y
    pixels.append((x, y))
    t += step

pixels.reverse()

def createBitmapHeader(width, height):
    file_type = 19778
    reserved_1 = 0
    reserved_2 = 0
    offset = 62
    file_size = offset + 1 * width * height
    return pack("<HL2HL", file_type, file_size, reserved_1, reserved_2, offset)


def createInfoHeader(width, height):
    header_size = 40
    planes = 1
    bits_per_pixel = 8
    compression = 0
    image_size = 0
    x_pixel_per_meter = 0
    y_pixel_per_meter = 0
    total_colors = 2
    important_colors = 0
    return pack("<3L2H6L", header_size, width, height, planes, bits_per_pixel, compression, image_size, x_pixel_per_meter,
                y_pixel_per_meter, total_colors, important_colors)


def createColorPallet():
    color1 = (0, 0, 0, 0)
    color2 = (255, 255, 255, 0)
    return pack("<8B", *color1, *color2)


with open('test.bmp', "wb") as f:
    f.write(createBitmapHeader(width, height))
    f.write(createInfoHeader(width, height))
    f.write(createColorPallet())

    y_pix = y_min
    for y_val in range(height):
        x_pix = x_min
        for x_val in range(width):
            if (x_pix, y_pix) in pixels:
                f.write(pack("<B", 0))
            else:
                f.write(pack("<B", 1))
            x_pix = round(x_pix + step, 2)
        y_pix = round(y_pix + step, 2)

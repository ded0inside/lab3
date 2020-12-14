from math import sin, pi
from struct import pack

width = 200
heigh = 200
t = 0
step = 0.01
pixels = []
xMin = float('inf')
yMin = float('inf')

while t <= 2 * pi:
    x = round(sin(t+pi/2) , 2)
    if x <= xMin:
        xMin = x
    y = round(sin(2*t), 2)
    if y <= yMin:
        yMin = y
    pixels.append((x, y))
    t += step

pixels.reverse()



def createBitmapHeader(width, heigh):
    filetype = 19778
    reserved1 = 0
    resreved2 = 0
    offset = 62
    filesize = offset + 1 * width * heigh
    return pack("<HL2HL", filetype, filesize, reserved1, resreved2, offset)


def createInfoHeader(width, heigh):
    headerSize = 40
    planes = 1
    bitsPerPixel = 8
    compression = 0
    imageSize = 0
    xPixelPerMeter = 0
    yPixelPerMeter = 0
    totalColors = 2
    importantColors = 0
    return pack("<3L2H6L", headerSize, width, heigh, planes, bitsPerPixel, compression, imageSize, xPixelPerMeter,
                yPixelPerMeter, totalColors, importantColors)


def createColorPallet():
    color1 = (0, 0, 0, 0)
    color2 = (255, 255, 255, 0)
    return pack("<8B", *color1, *color2)


with open('test.bmp', "wb") as f:
    f.write(createBitmapHeader(width, heigh))
    f.write(createInfoHeader(width, heigh))
    f.write(createColorPallet())

    yPix = yMin
    for yVal in range(heigh):
        xPix = xMin
        for xVal in range(width):
            if (xPix, yPix) in pixels:
                f.write(pack("<B", 0))
            else:
                f.write(pack("<B", 1))
            xPix = round(xPix + step, 2)
        yPix = round(yPix + step, 2)

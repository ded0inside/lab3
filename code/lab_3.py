from math import sin, pi
from struct import pack


class BitmapGenerator:
    def __init__(self, filename, width, height, x, y, t_start, t_stop, t_step):
        self.file = filename
        self.width = width
        self.height = height
        self.x_func = x
        self.y_func = y
        self.x_min = float("inf")
        self.y_min = float("inf")
        self.t_start = t_start
        self.t_stop = t_stop
        self.t_step = t_step
        self.round_to = len(str(t_step)) - 2

    def __createBitmapHeader(self):
        file_type = 19778
        reserved_1 = 0
        reserved_2 = 0
        offset = 62
        file_size = offset + self.width * self.height
        return pack("<HL2HL", file_type, file_size, reserved_1, reserved_2, offset)

    def __createInfoHeader(self):
        header_size = 40
        planes = 1
        bits_per_pixel = 8
        compression = 0
        image_size = 0
        x_pixel_per_meter = 0
        y_pixel_per_meter = 0
        total_colors = 2
        important_colors = 0
        return pack(
            "<3L2H6L",
            header_size,
            self.width,
            self.height,
            planes,
            bits_per_pixel,
            compression,
            image_size,
            x_pixel_per_meter,
            y_pixel_per_meter,
            total_colors,
            important_colors,
        )

    def __createColorPallet(self):
        color1 = (0, 0, 0, 0)
        color2 = (255, 255, 255, 0)
        return pack("<8B", *color1, *color2)

    def __createPixels(self):
        pixels = []
        t = self.t_start
        while t <= self.t_stop:
            x = round(self.x_func(t), self.round_to)
            if x <= self.x_min:
                self.x_min = x
            y = round(self.y_func(t), self.round_to)
            if y <= self.y_min:
                self.y_min = y
            pixels.append((x, y))
            t += self.t_step
        pixels.reverse()
        return pixels

    def createBmp(self):
        with open(f"{self.file}.bmp", "wb") as f:
            f.write(self.__createBitmapHeader())
            f.write(self.__createInfoHeader())
            f.write(self.__createColorPallet())
            pixels = self.__createPixels()

            y_pix = self.y_min
            for y_val in range(self.height):
                x_pix = self.x_min
                for x_val in range(self.width):
                    if (x_pix, y_pix) in pixels:
                        f.write(pack("<B", 0))
                    else:
                        f.write(pack("<B", 1))
                    x_pix = round(x_pix + self.t_step, self.round_to)
                y_pix = round(y_pix + self.t_step, 2)


if __name__ == "__main__":

    bitmap = BitmapGenerator(
        filename="test2",
        width=200,
        height=200,
        t_start=0,
        t_stop=2 * pi,
        t_step=0.01,
        x=lambda t: sin(t + pi / 2),
        y=lambda t: sin(2 * t),
    )
    bitmap.createBmp()

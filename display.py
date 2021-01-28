from pygame import display, HWSURFACE, DOUBLEBUF, Color, draw

DISPLAY_DEPTH = 8

PIX_COLORS = {
    0: Color(0, 0, 0, 255),
    1: Color(250, 250, 250, 255)
}


class Display:

    def __init__(self, scale_factor=16):
        self.height = 32
        self.width = 64
        self.scale_factor = scale_factor
        self.initialize_window()

    def initialize_window(self):
        display.init()
        self.surface = display.set_mode(
            ((self.width * self.scale_factor),
             (self.height * self.scale_factor)),
            HWSURFACE | DOUBLEBUF,
            DISPLAY_DEPTH)
        self.clear_screen()
        self.update()

    def update(self):
        display.flip()

    def draw_sprite(self, x, y, sprite):
        flag = 0
        for byte in sprite:
            for bit in range(8):
                color = (byte >> (7 - bit)) & 1
                previous = self.get_pixel(x, y)
                if previous == 1 and color == 1:
                    flag = 1
                self.draw_pixel(x + bit, y, color)
            y += 1
        self.update()
        return flag

    def draw_pixel(self, x, y, color):
        x_coord = (x % 64) * self.scale_factor
        y_coord = (y % 32) * self.scale_factor
        previous = self.get_pixel(x, y)
        # noinspection PyUnresolvedReferences
        new_color = previous ^ color
        draw.rect(self.surface,
                  PIX_COLORS[new_color],
                  (x_coord, y_coord, self.scale_factor, self.scale_factor))

    def get_pixel(self, x, y):
        x_coord = (x % 64) * self.scale_factor
        y_coord = (y % 32) * self.scale_factor
        pixel_color = self.surface.get_at((x_coord, y_coord))
        if pixel_color == PIX_COLORS[0]:
            return 0
        return 1

    def clear_screen(self):
        self.surface.fill(PIX_COLORS[0])

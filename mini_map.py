from settings import *
from tools import *
from math import cos, sin
from map import mini_map


class MiniMap:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.pos = MINI_MAP_POS
        self.x, self.y = self.pos
        self.square_side = SQUARE_SIDE // MINI_MAP_SCALE

    def player_render(self):
        x0 = self.player.x // MINI_MAP_SCALE
        y0 = self.player.y // MINI_MAP_SCALE
        self.screen.create_oval(x0 - PLAYER_SIZE // 2, y0 - PLAYER_SIZE // 2,
                                x0 + PLAYER_SIZE // 2, y0 + PLAYER_SIZE // 2,
                                fill=PLAYER_COLOR)
        xm, ym = mini_mapping(x0, y0)

        sin_a = sin(self.player.angle)
        cos_a = cos(self.player.angle)
        sin_a = sin_a if sin_a else 0.000001
        cos_a = cos_a if cos_a else 0.000001

        # verticals
        x, dx = (xm + self.square_side, 1) if cos_a >= 0 else (xm, -1)
        for i in range(0, MINI_MAP_WIDTH, self.square_side):
            depth_v = (x - x0) / cos_a
            y = y0 + depth_v * sin_a
            if mini_mapping(x + dx, y) in mini_map:
                break
            x += dx * self.square_side

        x1, y1 = x, y
        # horizontals

        y, dy = (ym + self.square_side, 1) if sin_a >= 0 else (ym, -1)
        for i in range(0, MINI_MAP_HEIGHT, self.square_side):
            depth_h = (y - y0) / sin_a
            x = x0 + depth_h * cos_a
            if mini_mapping(x, y + dy) in mini_map:
                break
            y += dy * self.square_side
        x2, y2 = x, y

        if depth_h > depth_v:
            self.screen.create_line(x0, y0, x1, y1, fill=WHITE)
        else:
            self.screen.create_line(x0, y0, x2, y2, fill=WHITE)

    def map_render(self):
        for x, y in mini_map:
            self.screen.create_rectangle(x, y, x + self.square_side, y + self.square_side, outline=WHITE)

    def drawing(self):
        self.screen.delete("all")
        self.map_render()
        self.player_render()

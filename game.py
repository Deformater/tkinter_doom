from settings import *
from map import world_map
from math import sin, cos
from tools import *


class Game:
    def __init__(self, screen, player, mini_map):
        self.screen = screen
        self.player = player
        self.mini_map = mini_map

        for btn in KEY_BUTTONS:
            screen.bind_all(btn, self.update)

    def ray_casting(self):
        ox, oy = self.player.pos
        xm, ym = mapping(ox, oy)
        cur_angle = self.player.angle - HALF_FOV
        for ray in range(NUM_RAYS):
            sin_a = sin(cur_angle)
            cos_a = cos(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.000001

            # verticals
            x, dx = (xm + SQUARE_SIDE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, WIDTH, SQUARE_SIDE):
                depth_v = (x - ox) / cos_a
                y = oy + depth_v * sin_a
                if mapping(x + dx, y) in world_map:
                    break
                x += dx * SQUARE_SIDE

            # horizontals
            y, dy = (ym + SQUARE_SIDE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, HEIGHT, SQUARE_SIDE):
                depth_h = (y - oy) / sin_a
                x = ox + depth_h * cos_a
                if mapping(x, y + dy) in world_map:
                    break
                y += dy * SQUARE_SIDE

            # projection
            depth = min([depth_v, depth_h])
            depth *= cos(self.player.angle - cur_angle)
            proj_height = PROJ_COEFF / depth
            c = int(255 / (1 + depth * depth * 0.00002))
            self.screen.create_rectangle(ray * SCALE, HALF_HEIGHT - proj_height // 2,
                                         (ray + 1) * SCALE, HALF_HEIGHT + proj_height // 2,
                                         fill=rgb_to_hex(c, c // 2, c // 3),
                                         outline=rgb_to_hex(c, c // 2, c // 3))
            cur_angle += DELTA_ANGLE

    def drawing(self):
        self.screen.delete("all")
        self.screen.create_rectangle(0, 0, WIDTH, HALF_HEIGHT, fill=rgb_to_hex(*BLUE))
        self.screen.create_rectangle(0, HALF_HEIGHT, WIDTH, HALF_HEIGHT, fill=BLACK)
        self.ray_casting()

    def update(self, event):
        self.player.update(event.keysym)
        self.drawing()
        self.mini_map.drawing()

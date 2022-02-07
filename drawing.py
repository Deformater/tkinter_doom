from settings import *
from map import world_map
from math import sin, cos


class Drawing:
    @staticmethod
    def rgb_to_hex(r, g, b):
        return f'#{r:02x}{g:02x}{b:02x}'

    @staticmethod
    def mapping(x, y):
        return (x // SQUARE_SIDE) * SQUARE_SIDE, (y // SQUARE_SIDE) * SQUARE_SIDE

    def __init__(self, screen, player):
        self.screen = screen
        self.player = player

        for btn in KEY_BUTTONS:
            screen.bind_all(btn, self.update)

    def player_render(self):
        self.screen.create_oval(self.player.x - PLAYER_SIZE // 2, self.player.y - PLAYER_SIZE // 2,
                                self.player.x + PLAYER_SIZE // 2, self.player.y + PLAYER_SIZE // 2,
                                fill=PLAYER_COLOR)

    def map_render(self):
        for x, y in world_map:
            self.screen.create_rectangle(x, y, x + SQUARE_SIDE, y + SQUARE_SIDE, outline=WHITE)

        x0 = self.player.x
        y0 = self.player.y

        for depth in range(MAX_DEPTH):
            x = x0 + depth * cos(self.player.angle)
            y = y0 + depth * sin(self.player.angle)
            self.screen.create_line(x0, y0, x, y, fill=WHITE)
            if (x // SQUARE_SIDE * SQUARE_SIDE,
               y // SQUARE_SIDE * SQUARE_SIDE) in world_map:
                break

    def ray_casting(self):
        depth_h = depth_v = 0
        x0, y0 = self.player.pos
        xm, ym = self.mapping(x0, y0)
        angle = self.player.angle
        cur_angle = angle - HALF_FOV
        for ray in range(NUM_RAYS):
            cos_a = cos(cur_angle)
            sin_a = sin(cur_angle)
            sin_a = sin_a if sin_a else 0.000001
            cos_a = cos_a if cos_a else 0.00000

            # vertical
            x, dx = (xm + SQUARE_SIDE, 1) if cos_a >= 0 else (xm, -1)
            for i in range(0, WIDTH, SQUARE_SIDE):
                depth_v = (x - x0) / cos_a
                y = y0 + depth_v * sin_a
                if self.mapping(x + dx, y) in world_map:
                    break
                x += dx * SQUARE_SIDE

            # horizontal
            y, dy = (ym + SQUARE_SIDE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, HEIGHT, SQUARE_SIDE):
                depth_h = (y - y0) / sin_a
                x = x0 + depth_h * cos_a
                if self.mapping(x, y + dy) in world_map:
                    break
                y += dy * SQUARE_SIDE

            depth = min([depth_v, depth_h])
            depth *= cos(angle - cur_angle)
            height = PROJ_COEFF / depth
            color = int(255 / (1 + depth * 0.005))
            self.screen.create_rectangle(ray * SCALE, HALF_HEIGHT - height // 2,
                                         ray * (SCALE + 1), HALF_HEIGHT + height // 2,
                                         fill=self.rgb_to_hex(color, color, color),
                                         outline=self.rgb_to_hex(color, color, color))
            cur_angle += DELTA_ANGLE

    def drawing(self):
        self.screen.delete("all")
        self.screen.create_rectangle(0, 0, WIDTH, HALF_HEIGHT, fill=self.rgb_to_hex(*BLUE))
        self.screen.create_rectangle(0, HALF_HEIGHT, WIDTH, HALF_HEIGHT, fill=BLACK)
        # self.player_render()
        # self.map_render()
        self.ray_casting()

    def update(self, event):
        self.player.update(event.keysym)
        self.drawing()

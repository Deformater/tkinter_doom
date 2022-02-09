from settings import *
from map import world_map
from math import sin, cos, degrees
from tools import *
from tkinter import *
from PIL import Image, ImageTk


class Game:
    def __init__(self, screen: Canvas, player, mini_map):
        self.screen = screen
        self.player = player
        self.mini_map = mini_map

        self.image = PhotoImage(file='img/sky1.png')
        self.texture = Image.open('img/wall1.png')

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
                yv = oy + depth_v * sin_a
                if mapping(x + dx, yv) in world_map:
                    break
                x += dx * SQUARE_SIDE

            # horizontals
            y, dy = (ym + SQUARE_SIDE, 1) if sin_a >= 0 else (ym, -1)
            for i in range(0, HEIGHT, SQUARE_SIDE):
                depth_h = (y - oy) / sin_a
                xh = ox + depth_h * cos_a
                if mapping(xh, y + dy) in world_map:
                    break
                y += dy * SQUARE_SIDE

            # projection
            depth, offset = (depth_v, yv) if depth_v < depth_h else (depth_h, xh)
            offset = int(offset) % SQUARE_SIDE
            depth *= cos(self.player.angle - cur_angle)
            depth = max(depth, 0.000001)
            proj_height = min(int(PROJ_COEFF / depth), 2 * HEIGHT)
            c = int(255 / (1 + depth * depth * 0.00002))

            self.screen.create_rectangle(ray * SCALE, HALF_HEIGHT - proj_height // 2,
                                         (ray + 1) * SCALE, HALF_HEIGHT + proj_height // 2,
                                         fill=rgb_to_hex(c, c // 2, c // 3),
                                         outline=rgb_to_hex(c, c // 2, c // 3))

            # rendering
            # im_crop = self.texture.crop((offset * TEXTURE_SCALE, 0, (offset + 1) * TEXTURE_SCALE, TEXTURE_HEIGHT))
            # im_crop = im_crop.transform((SCALE, proj_height), Image.EXTENT,
            #                             [0, 0, im_crop.width, im_crop.height])
            # im_crop = ImageTk.PhotoImage(im_crop)
            # self.screen.create_image(ray * SCALE, HALF_HEIGHT - proj_height // 2, image=im_crop, anchor="nw")

            cur_angle += DELTA_ANGLE

    def background(self):
        sky_offset = -5 * degrees(self.player.angle) % WIDTH
        self.screen.create_rectangle(0, HALF_HEIGHT, WIDTH, HEIGHT, fill=BLACK)
        self.screen.create_image(sky_offset, 0, image=self.image, anchor="nw")
        self.screen.create_image(sky_offset - WIDTH, 0, image=self.image, anchor="nw")
        self.screen.create_image(sky_offset + WIDTH, 0, image=self.image, anchor="nw")

    def drawing(self):
        self.screen.delete("all")
        self.background()
        self.ray_casting()

    def update(self, event):
        self.player.update(event.keysym)
        self.drawing()
        self.mini_map.drawing()

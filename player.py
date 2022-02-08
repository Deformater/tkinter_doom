from settings import *
from math import sin, cos


class Player:
    def __init__(self):
        self.pos = PLAYER_POS
        self.angle = PLAYER_ANGLE
        self.speed = PLAYER_SPEED
        self.angle_speed = PLAYER_ANGLE_SPEED
        self.x = self.pos[0]
        self.y = self.pos[1]

    def update(self, key):
        if key == 'w':
            self.x += self.speed * cos(self.angle)
            self.y += self.speed * sin(self.angle)
        if key == 's':
            self.x -= self.speed * cos(self.angle)
            self.y -= self.speed * sin(self.angle)
        if key == 'a':
            self.x += self.speed * sin(self.angle)
            self.y -= self.speed * cos(self.angle)
        if key == 'd':
            self.x -= self.speed * sin(self.angle)
            self.y += self.speed * cos(self.angle)
        if key == 'Right':
            self.angle += self.angle_speed
        if key == 'Left':
            self.angle -= self.angle_speed

        self.pos = self.x, self.y

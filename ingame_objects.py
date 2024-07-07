import math
import random
from pygame import time
rocket_list = []
bullet_list = []
H = 600
W = 1200


class MovingObject:
    def move(self):
        self.x += self.vx
        self.y += self.vy


class Rocket(MovingObject):

    def __init__(self):
        self.x = random.randint(100, W - 100)
        self.y = 20
        v = 0.5
        self.angle = math.atan2(750 - self.x, 550 - self.y)
        self.vx = v * math.sin(self.angle)
        self.vy = v * math.cos(self.angle)


class Bullet(MovingObject):

    def __init__(self, x, y, t, angle):
        self.x = x
        self.y = y
        self.t = t
        self.angle = math.pi * (angle + 90) / 180
        self.v = 1.8
        self.vx = self.v * math.cos(self.angle)
        self.vy = -self.v * math.sin(self.angle)

    def change_speed(self):
        # print(self.vx, self.vy)
        a = -10 - 1.23 * self.v * abs(self.v) / 2 * 0.4 * 0.75 / 10
        self.vy = self.vy - a * (time.get_ticks() / 1000 - self.t) / 1000
        # print(self.vx, self.vy)


class Radar:

    def __init__(self, max_distance):
        self.max_distance = max_distance
        self.x = 300
        self.y = H

    def scan(self):
        r = self.max_distance
        re = []
        printer = "SCANNING: "
        for rocket in rocket_list:
            if (self.x - rocket.x) ** 2 + (self.y - rocket.y) ** 2 <= r ** 2 and rocket.y < H:
                angle = math.atan2(rocket.y - self.y, rocket.x - self.x)
                re.append((rocket, - (90 + angle * 180 / math.pi)))
                printer += f"({id(rocket)}, {round(180 * rocket.angle / math.pi)}, {round(((self.x - rocket.x) ** 2 + (self.y - rocket.y) ** 2) ** 0.5)}), "

        print(printer)
        return tuple(re)

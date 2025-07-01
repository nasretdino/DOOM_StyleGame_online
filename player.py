from settings import *
import pygame as pg
import math


class Player:
    def __init__(self, screen, world_map, delta_time):
        self.delta_time = delta_time
        self.screen = screen
        self.world_map = world_map
        self.x, self.y = PLAYER_POS
        self.angle = 1  # коэффициент, на который домножается DELTA_ANGLE
        self.get_table_sin()
        self.get_table_cos()
        self.reloading = False
        self.shot = False

        self.life = True
        self.life2 = True


        self.x2, self.y2 = PLAYER_POS  # Координаты второго игрока

    def single_fire_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1 and not self.reloading:
                self.shot = True
                self.reloading = True



    def get_table_sin(self):
        self.table_sin = {}
        angle = 0
        for i in range(0, int(NUM_ANGLES_360)):
            self.table_sin[i] = math.sin(math.radians(angle))
            angle = DELTA_ANGLE * i

    def get_table_cos(self):
        self.table_cos = {}
        angle = 0
        for i in range(0, int(NUM_ANGLES_360)):
            self.table_cos[i] = math.cos(math.radians(angle))
            angle = DELTA_ANGLE * i

    def movement(self):
        sin_a = self.table_sin[self.angle]
        cos_a = self.table_cos[self.angle]
        x, y = 0, 0
        speed = PLAYER_SPEED * self.delta_time
        speed_sin = speed * sin_a
        speed_cos = speed * cos_a

        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            x += speed_cos
            y += speed_sin
        if keys[pg.K_s]:
            x -= speed_cos
            y -= speed_sin
        if keys[pg.K_a]:
            x += speed_sin
            y -= speed_cos
        if keys[pg.K_d]:
            x -= speed_sin
            y += speed_cos

        self.check_wall_collision(x, y)

        # if keys[pg.K_LEFT]:
        #     self.angle -= self.delta_time * PLAYER_ROT_SPEED / DELTA_ANGLE
        # if keys[pg.K_RIGHT]:
        #     self.angle += self.delta_time * PLAYER_ROT_SPEED / DELTA_ANGLE
        #
        # self.angle = self.in_360(self.angle)

    @staticmethod
    def in_360(angle):
        while angle >= NUM_ANGLES_360 or angle < 0:
            if angle >= 360:
                angle -= NUM_ANGLES_360
            elif angle < 0:
                angle += NUM_ANGLES_360
        return angle

    def check_wall(self, x, y):
        return (x, y) not in self.world_map

    def check_wall_collision(self, x, y):
        scale = PLAYER_SIZE_SCALE / self.delta_time
        if self.check_wall(int(self.x + x * scale), int(self.y)): self.x += x
        if self.check_wall(int(self.x), int(self.y + y * scale)): self.y += y

    def mouse_control(self):
        mx, my = pg.mouse.get_pos()
        if mx < MOUSE_BORDER_LEFT or mx > MOUSE_BORDER_RIGHT:
            pg.mouse.set_pos([HALF_WIDTH, HALF_HEIGHT])
        self.rel = pg.mouse.get_rel()[0]
        self.rel = max(-MOUSE_MAX_REL, min(MOUSE_MAX_REL, self.rel))
        self.angle += self.rel * self.delta_time // (1 / MOUSE_SENSITIVITY)
        self.angle = self.in_360(self.angle)

    def update(self, delta_time):
        self.delta_time = delta_time
        self.movement()
        self.mouse_control()

    @property
    def pos(self):
        return self.x, self.y

    def set_coords_to_2(self, coords):
        self.x2, self.y2 = coords

    @property
    def map_pos(self):
        return int(self.x), int(self.y)

from collections import deque

import pygame as pg

from settings import HALF_WIDTH, HEIGHT


class Weapon:
    def __init__(self, screen, images, player):
        self.screen = screen
        self.animate_images = deque(images)
        self.start_image = images[0]
        self.shoot_image = images[1]
        self.image_to_animate = self.start_image
        self.player = player
        self.animation_time = 120
        self.animation_time_prev = pg.time.get_ticks()
        self.animation_trigger = False

    def animate(self, images):
        if self.animation_trigger:
            images.rotate(-1)
            return images[0]
        return images[0]

    def check_animation_time(self):
        self.animation_trigger = False
        time_now = pg.time.get_ticks()
        if time_now - self.animation_time_prev > self.animation_time:
            self.animation_time_prev = time_now
            self.animation_trigger = True

    def update(self):
        if self.player.reloading:
            self.check_animation_time()
            self.image_to_animate = self.animate(self.animate_images)
            if self.player.shot and self.image_to_animate == self.shoot_image: return True, False
            if self.image_to_animate == self.start_image: return False, False
        else:
            self.image_to_animate = self.start_image
            return False, False
        return True, self.player.shot

    def draw(self):
        im = self.image_to_animate
        self.screen.blit(im, (HALF_WIDTH - im.get_width() // 3 + 28, HEIGHT - im.get_height()))
import pygame as pg
from settings import *


class ObjectRender:
    def __init__(self, screen):
        self.screen = screen
        self.wall_textures = self.load_wall_textures()

        self.weapon_textures = self.load_weapon_textures()


    def draw(self, objects_to_render):
        self.render_game_objects(objects_to_render)


    def render_game_objects(self, objects_to_render):
        list_objects = objects_to_render
        for depth, image, pos in list_objects:
            self.screen.blit(image, pos)


    @staticmethod
    def get_texture(path, res=(TEXTURE_SIZE, TEXTURE_SIZE)):
        texture = pg.image.load(path).convert_alpha()
        return pg.transform.scale(texture, res)

    def load_wall_textures(self):
        return {
            1: self.get_texture('images/textures/wall_1.png'),
            2: self.get_texture('images/textures/wall_2.png'),
        }

    def load_weapon_textures(self):
        return [
            self.get_texture('images/weapon/1.png'),
            self.get_texture('images/weapon/2.png'),
            self.get_texture('images/weapon/3.png'),
            self.get_texture('images/weapon/4.png'),
            self.get_texture('images/weapon/5.png'),
            self.get_texture('images/weapon/6.png'),
            self.get_texture('images/weapon/7.png'),
            self.get_texture('images/weapon/8.png'),
            self.get_texture('images/weapon/9.png'),
            self.get_texture('images/weapon/10.png'),
            self.get_texture('images/weapon/11.png'),
        ]

import pygame as pg
from sys import exit
import os
import random


from settings import *
from map import *
from player import *
from raycasting import *
from object_render import *
from weapon import *
from network import*


class Game:
    def __init__(self):
        os.environ["SDL_WINDOWS_DPI_AWARENESS"] = "permonitorv2"
        os.environ["SDL_WINDOWS_DPI_SCALING"] = "0"
        pg.init()
        pg.mouse.set_visible(False)
        self.screen = pg.display.set_mode(RES)
        self.clock = pg.time.Clock()
        self.delta_time = 1
        self.new_game()

    def new_game(self):
        self.map = Map(self.screen)
        self.player = Player(self.screen, self.map.world_map, self.delta_time)
        self.object_render = ObjectRender(self.screen)
        self.raycasting = RayCasting(self.screen, self.map.world_map, self.player, self.object_render.wall_textures)
        self.weapon = Weapon(self.screen, self.object_render.weapon_textures, self.player)

        #self.network = Network(self.player,"0.0.0.0" ,"SERVER")
        self.network = Network(self.player, "10.194.17.128")
    def update(self):
        self.player.update(self.delta_time)
        self.network.update()
        self.raycasting.update()
        self.weapon.draw()
        pg.draw.circle(self.screen, "red" if self.player.shot else "white", (HALF_WIDTH, HALF_HEIGHT), 5)
        self.player.reloading, self.player.shot = self.weapon.update()
        if not self.player.life: self.show_end_screen()
        pg.display.flip()
        self.delta_time = self.clock.tick(FPS)
        pg.display.set_caption(f"{int(self.clock.get_fps())}")

    def show_end_screen(self):
        flag = False
        while True:
            self.screen.fill("black")
            f1 = pg.font.Font(None, 72)
            text1 = f1.render('Вы умерли. Нажмите пробел, чтобы воскреснуть', 1, "red")
            self.screen.blit(text1, (HALF_WIDTH - text1.get_width() // 2, HALF_HEIGHT - text1.get_height()))
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    pg.quit()
                    exit()
                if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                    self.player.life = True
                    coords = (random.randint(0, 15), random.randint(0, 8))
                    while coords not in self.map.world_map_not_wall:
                        coords = (random.randint(0, 15), random.randint(0, 8))
                    self.player.x, self.player.y = coords[0] + 0.5, coords[1] + 0.5
                    flag = True
                    self.network.update()
            if flag: break
            self.network.update()
            pg.display.flip()


    def draw(self):
        self.screen.fill("black")
        self.object_render.draw(self.raycasting.get_objects_to_render())

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                exit()
            self.player.single_fire_event(event)

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    game = Game()
    game.run()
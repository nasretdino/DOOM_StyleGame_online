import pygame as pg

from settings import *
import math


class RayCasting:
    def __init__(self, screen, new_map, player, wall_textures):
        self.screen = screen
        self.map = new_map
        self.player = player
        self.objects_to_render = []
        self.textures = wall_textures

    def get_objects_to_render(self):
        self.objects_to_render = []
        for ray, values in enumerate(self.ray_casting_result):
            depth, proj_height, texture, offset = values

            if proj_height < HEIGHT:
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), 0, SCALE, TEXTURE_SIZE
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, proj_height))
                wall_pos = (ray * SCALE, HALF_HEIGHT - proj_height // 2)
            else:
                texture_height = TEXTURE_SIZE * HEIGHT / proj_height
                wall_column = self.textures[texture].subsurface(
                    offset * (TEXTURE_SIZE - SCALE), HALF_TEXTURE_SIZE - texture_height // 2,
                    SCALE, texture_height
                )
                wall_column = pg.transform.scale(wall_column, (SCALE, HEIGHT))
                wall_pos = (ray * SCALE, 0)

            self.objects_to_render.append((depth, wall_column, wall_pos))

        return self.objects_to_render

    def ray_cast(self):
        self.ray_casting_result = []
        px, py = self.player.pos
        x_map, y_map = self.player.map_pos

        ray_angle = self.player.angle - HALF_FOV / DELTA_ANGLE - 1
        ray_angle = self.player.in_360(ray_angle)

        for ray in range(NUM_RAYS_FOV + 1):
            cos_a = self.player.table_cos[ray_angle] + 1e-6
            sin_a = self.player.table_sin[ray_angle] + 1e-6

            # horizontals
            y_hor, dy = (y_map + 1, 1) if sin_a > 0 else (y_map - 1e-6, -1)
            depth_hor = (y_hor - py) / sin_a
            x_hor = px + depth_hor * cos_a

            delta_depth = dy / sin_a
            dx = delta_depth * cos_a

            for i in range(MAX_DEPTH):
                tile_hor = (int(x_hor), int(y_hor))
                texture_hor = self.map[0, 0]
                if tile_hor in self.map:
                    texture_hor = self.map[tile_hor]
                    break
                x_hor += dx
                y_hor += dy
                depth_hor += delta_depth

            # verticals
            x_vert, dx = (x_map + 1, 1) if cos_a > 0 else (x_map - 1e-6, -1)

            depth_vert = (x_vert - px) / cos_a
            y_vert = depth_vert * sin_a + py

            delta_depth = dx / cos_a
            dy = delta_depth * sin_a

            for i in range(MAX_DEPTH):
                tile_vert = int(x_vert), int(y_vert)
                texture_vert = self.map[0, 0]
                if tile_vert in self.map:
                    texture_vert = self.map[tile_vert]
                    break
                x_vert += dx
                y_vert += dy
                depth_vert += delta_depth

            if depth_vert < depth_hor:
                x_wall, y_wall = x_vert, y_vert  # Координаты точки попадания луча в стену
                depth = depth_vert
                texture = texture_vert
                y_vert %= 1
                offset = y_vert if cos_a > 0 else (1 - y_vert)
            else:
                x_wall, y_wall = x_hor, y_hor  # Координаты точки попадания луча в стену
                depth = depth_hor
                texture = texture_hor
                x_hor %= 1
                offset = (1 - x_hor) if sin_a > 0 else x_hor

            # delete fish
            depth *= self.player.table_cos[self.player.in_360(self.player.angle - ray_angle)]

            x_p2, y_p2 = self.player.x2, self.player.y2
            dx, dy = x_p2 - px, y_p2 - py

            player_depth = dx * self.player.table_cos[self.player.angle] + dy * self.player.table_sin[self.player.angle] # проекция
            if player_depth > 0.5:
                distance_to_ray = abs(dx * sin_a - dy * cos_a)
                player_radius = 0.3  # Ширина модели игрока
                if distance_to_ray < player_radius:
                    if player_depth < depth:
                        proj_height_player = SCREEN_DIST / (player_depth + 1e-6)
                        pg.draw.rect(self.screen, 'white' if self.player.life2 else "red",
                                     (ray * SCALE, (HEIGHT - proj_height_player) // 2, SCALE, proj_height_player))

            proj_height = SCREEN_DIST / (depth + 1e-6)
            self.ray_casting_result.append((depth, proj_height, texture, offset))

            ray_angle += 1
            ray_angle = self.player.in_360(ray_angle)

    def update(self):
        self.ray_cast()
        self.get_objects_to_render()

import Scenes
import Objects
import pygame
from math import pi
import math
import MapFuncs


class GameScene(Scenes.Scene):
    def __init__(self):
        super().__init__()
        self.wall_list = []
        self.wall_cache = {}
        self.jump_to = False
        self.type = None
        ## wall_cache结构：{距离：[第一个面：[[坐标]，[颜色]]，第二个面：[[坐标]，[颜色]]...]，第二个距离...}

    def join_in(
        self, manager: Scenes.SceneManager, args
    ):  ##第一位为地图，第二位为screen
        manager.render_word("加载中", 100)
        self.wall_list, self.camera, self.map, self.type = MapFuncs.getWall(
            manager.mapdist
        )
        if self.camera is None:
            manager.jump_to(
                manager.scenelists["ErrorLoadingScene"], None, ["MenuScene"]
            )
            return
        self.update(manager)
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        return super().join_in(manager, args)

    def update(self, manager: Scenes.SceneManager):
        if self.jump_to:
            self.jump_to = False
            self.camera.on_move = [False, False, False, False, False, False]
            manager.reserve_jump(manager.scenelists["PauseScene"])
            return
        self.wall_cache = {}
        trans_mat = self.camera.get_trans_mat()
        temp = Objects.hit_1(self.wall_list, trans_mat, self.camera)
        for i in temp:
            if not i is None:
                r, c = i[0].shape
                temp2 = [[], i[2]]
                for j in range(c):
                    temp2[0].append([])
                    temp2[0][j].append(i[0][2, j] * 100 + 640)
                    temp2[0][j].append(-i[0][1, j] * 100 + 360)
                if not i[1] in self.wall_cache.keys():
                    self.wall_cache[i[1]] = []
                self.wall_cache[i[1]].append(temp2)
        while self.camera.vision[0] > pi:
            self.camera.vision[0] -= 2 * pi
        while self.camera.vision[0] < -pi:
            self.camera.vision[0] += 2 * pi
        if self.camera.vision[1] > pi / 2 - 0.03:
            self.camera.vision[1] = pi / 2 - 0.03
        if self.camera.vision[1] < -pi / 2 + 0.03:
            self.camera.vision[1] = -pi / 2 + 0.03
        new_dest = self.camera.dest.copy()
        move = [0.0, 0.0, 0.0]
        if self.camera.on_move[0]:
            move[0] += 1.0
        if self.camera.on_move[1]:
            move[2] -= 1.0
        if self.camera.on_move[2]:
            move[0] -= 1.0
        if self.camera.on_move[3]:
            move[2] += 1.0
        if self.camera.on_move[4]:
            move[1] += 1.0
        if self.camera.on_move[5]:
            move[1] -= 1.0
        d = math.sqrt(move[0] ** 2 + move[2] ** 2)
        if d != 0.0:
            move[0] /= d
            move[2] /= d
            new_dest[0] += move[0] * math.cos(self.camera.vision[0]) + move[
                2
            ] * math.sin(self.camera.vision[0])
            new_dest[2] += -move[0] * math.sin(self.camera.vision[0]) + move[
                2
            ] * math.sin(self.camera.vision[0] + pi / 2)
        new_dest[1] += move[1]
        if self.type == "normal":
            if new_dest[0] < 0:
                new_dest[0] = 0.0
            elif new_dest[0] > (self.map.shape[0] - 2) * 40:
                new_dest[0] = (self.map.shape[0] - 2) * 40.0
            if new_dest[1] > 1000.0:
                new_dest[1] = 1000.0
            elif new_dest[1] < 0.0:
                new_dest[1] = 0.0
            if new_dest[2] < 0:
                new_dest[2] = 0.0
            elif new_dest[2] > (self.map.shape[1] - 2) * 40:
                new_dest[2] = (self.map.shape[1] - 2) * 40.0
        ##MapFuncs.getMovePosition(self.map, self.camera.dest)
        MapFuncs.getMovePosition_test(self.wall_list, new_dest, self.camera.dest)
        self.camera.dest = new_dest.copy()
        return super().update(manager)

    def draw(self, screen: pygame.Surface):
        screen.fill((255, 255, 255))
        for i in sorted(self.wall_cache, reverse=True):
            for j in self.wall_cache[i]:
                pygame.draw.polygon(
                    screen, (50, 50, 50), [[y * 2 for y in x] for x in j[0]], width=10
                )
                pygame.draw.polygon(screen, j[1], [[y * 2 for y in x] for x in j[0]])
        return super().draw(screen)

    def input(self, event: Scenes.Event, scale_x: float, scale_y: float):
        if event.type == pygame.MOUSEMOTION:
            self.camera.vision[0] -= event.rel[0] / 640 * pi
            self.camera.vision[1] -= event.rel[1] / 640 * pi
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.jump_to = True
            elif event.key == pygame.K_w:
                self.camera.on_move[0] = False
            elif event.key == pygame.K_a:
                self.camera.on_move[1] = False
            elif event.key == pygame.K_s:
                self.camera.on_move[2] = False
            elif event.key == pygame.K_d:
                self.camera.on_move[3] = False
            elif event.key == pygame.K_SPACE:
                self.camera.on_move[4] = False
            elif event.key == pygame.K_LSHIFT:
                self.camera.on_move[5] = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.camera.on_move[0] = True
            elif event.key == pygame.K_a:
                self.camera.on_move[1] = True
            elif event.key == pygame.K_s:
                self.camera.on_move[2] = True
            elif event.key == pygame.K_d:
                self.camera.on_move[3] = True
            elif event.key == pygame.K_SPACE:
                self.camera.on_move[4] = True
            elif event.key == pygame.K_LSHIFT:
                self.camera.on_move[5] = True
        return super().input(event, scale_x, scale_y)

    def jump_out(self, manager, args=None):
        self.wall_cache = {}
        self.wall_list = []
        self.camera = None
        self.jump_to = False
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        return super().jump_out(manager, args)

import Scenes
from pygame import Surface
from tkinter import filedialog
import pygame
import Button
import json
import copy


class EditPlane:
    def __init__(self, my_map: list[list]):
        self.map = my_map
        self.statue = None  ##结构：[类型，[行，列]]
        self.row = len(my_map)
        self.col = len(my_map[0])
        self.height, self.width = 620, 620
        if self.row > self.col:
            self.width = int(self.col / self.row * self.width)
        elif self.col > self.row:
            self.height = int(self.row / self.col * self.height)
        self.left = 360 - self.width / 2
        self.top = 360 - self.height / 2
        self.unit_width = self.height / self.row
        if not self.unit_width < 12.5:
            self.spawn_width = self.unit_width * 0.8
        else:
            self.spawn_width = 10.0

    def draw(self, screen: Surface):
        canvas = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, (200, 200, 200), canvas)
        spawning = [-1, -1]

        for i in range(self.row):
            for j in range(self.col):
                if self.map[i][j] == 1:
                    pygame.draw.rect(
                        screen,
                        (255, 99, 71),  ##番茄
                        pygame.Rect(
                            self.left + j * self.unit_width,
                            self.top + i * self.unit_width,
                            self.unit_width + 1,
                            self.unit_width + 1,
                        ),
                    )
                elif self.map[i][j] == 2:
                    spawning = [i, j]
        if not spawning[0] == -1:
            pygame.draw.rect(
                screen,
                (124, 252, 0),  ##草坪色
                pygame.Rect(
                    self.left
                    + (2 * spawning[1] + 1) * self.unit_width / 2
                    - self.spawn_width / 2,
                    self.top
                    + (2 * spawning[0] + 1) * self.unit_width / 2
                    - self.spawn_width / 2,
                    self.spawn_width + 1,
                    self.spawn_width + 1,
                ),
            )
        if not self.statue is None:
            if self.statue[0] == "pen":
                pygame.draw.rect(
                    screen,
                    (255, 160, 122),  ##浅鲑鱼色
                    pygame.Rect(
                        self.left + self.statue[1][1] * self.unit_width,
                        self.top + self.statue[1][0] * self.unit_width,
                        self.unit_width + 1,
                        self.unit_width + 1,
                    ),
                )
            elif self.statue[0] == "eraser":
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    pygame.Rect(
                        self.left + self.statue[1][1] * self.unit_width,
                        self.top + self.statue[1][0] * self.unit_width,
                        self.unit_width + 1,
                        self.unit_width + 1,
                    ),
                )
            elif self.statue[0] == "spawn":
                pygame.draw.rect(
                    screen,
                    (173, 255, 47),  ##黄绿色
                    pygame.Rect(
                        self.left
                        + (2 * self.statue[1][1] + 1) * self.unit_width / 2
                        - self.spawn_width / 2,
                        self.top
                        + (2 * self.statue[1][0] + 1) * self.unit_width / 2
                        - self.spawn_width / 2,
                        self.spawn_width + 1,
                        self.spawn_width + 1,
                    ),
                ),

    def deal(self):
        if self.statue[0] == "pen":
            self.map[self.statue[1][0]][self.statue[1][1]] = 1
        elif self.statue[0] == "spawn":
            for i in range(self.row):
                for j in range(self.col):
                    if self.map[i][j] == 2:
                        self.map[i][j] = 0
            self.map[self.statue[1][0]][self.statue[1][1]] = 2
        elif self.statue[0] == "eraser":
            self.map[self.statue[1][0]][self.statue[1][1]] = 0


class EditScene(Scenes.Scene):
    def __init__(self):
        self.plane = None
        self.back_statue = False
        self.back_button = Button.Button("返回", 70, 25, 100, 40)
        self.pen_button = Button.Button("铅笔", 780, 100, 180, 50)
        self.eraser_button = Button.Button("橡皮", 980, 100, 180, 50)
        self.spawn_button = Button.Button("选择出生点", 1180, 100, 180, 50)
        self.col_unit = Button.SettingUnit(750, 200, 4, 1, 4, 100, "列")
        self.row_unit = Button.SettingUnit(750, 300, 4, 1, 4, 100, "行")
        self.confirm_button = Button.Button("确认", 1180, 265, 180, 50)
        self.new_button = Button.Button("新建地图", 780, 400, 180, 50)
        self.read_button = Button.Button("读取地图", 980, 400, 180, 50)
        self.save_button = Button.Button("保存地图", 1180, 400, 180, 50)
        self.has_saved = True
        self.statue = "pen"  ##为pen，eraser或spawn
        self.lpress = False
        self.confirm_change = False
        self.file_operate = [False, False, False]  ##为new,read与save
        super().__init__()

    def join_in(self, manager: Scenes.SceneManager, args=None):
        try:
            with open(manager.mapdist, mode="r") as mapfile:
                my_map = json.load(mapfile)["map"]
                self.plane = EditPlane(my_map)
                self.col_unit.value = self.plane.col
                self.row_unit.value = self.plane.row
                self.has_saved = True
        except Exception:
            manager.reserve_jump(manager.scenelists["ErrorLoadingScene"], [self])
            self.create_new_map()
        return super().join_in(manager, args)

    def draw(self, screen: Surface):
        screen.fill((255, 255, 255))
        self.plane.draw(screen)
        self.back_button.draw(screen)
        self.pen_button.draw(screen)
        self.eraser_button.draw(screen)
        self.spawn_button.draw(screen)
        self.col_unit.draw(screen)
        self.row_unit.draw(screen)
        if not (
            self.col_unit.value == self.plane.col
            and self.row_unit.value == self.plane.row
        ):
            self.confirm_button.draw(screen)
        self.new_button.draw(screen)
        self.read_button.draw(screen)
        self.save_button.draw(screen)
        return super().draw(screen)

    def input(self, event: Scenes.Event):
        self.col_unit.input(event)
        self.row_unit.input(event)
        self.confirm_change = self.confirm_change or self.confirm_button.deal_mouse(
            event
        )
        self.back_statue = self.back_statue or self.back_button.deal_mouse(event)
        self.file_operate[0] = self.file_operate[0] or self.new_button.deal_mouse(event)
        self.file_operate[1] = self.file_operate[1] or self.read_button.deal_mouse(
            event
        )
        self.file_operate[2] = self.file_operate[2] or self.save_button.deal_mouse(
            event
        )
        if self.eraser_button.deal_mouse(event):
            self.statue = "eraser"
        if self.pen_button.deal_mouse(event):
            self.statue = "pen"
        if self.spawn_button.deal_mouse(event):
            self.statue = "spawn"
        if hasattr(event, "pos"):
            row = (event.pos[1] - self.plane.top) // self.plane.unit_width
            col = (event.pos[0] - self.plane.left) // self.plane.unit_width
            if 0 <= row < self.plane.row and 0 <= col < self.plane.col:
                self.plane.statue = [self.statue, [int(row), int(col)]]
            else:
                self.plane.statue = None
        mouse_presses = pygame.mouse.get_pressed()
        self.lpress = mouse_presses[0] or self.lpress
        return super().input(event)

    def update(self, manager: Scenes.SceneManager):
        self.col_unit.update()
        self.row_unit.update()
        if self.lpress:
            self.lpress = False
            if not self.plane.statue is None:
                self.plane.deal()
                self.has_saved = False
        if self.confirm_change and not (
            self.col_unit.value == self.plane.col
            and self.row_unit.value == self.plane.row
        ):
            self.confirm_change = False
            self.reset_map(self.col_unit.value, self.row_unit.value)
        if self.file_operate[0]:
            self.file_operate = [False, False, False]
            self.create_new_map()
        if self.file_operate[1]:
            self.file_operate = [False, False, False]
            self.read_map(manager)
        if self.file_operate[2]:
            self.file_operate = [False, False, False]
            self.save_map(manager)
        if self.back_statue:
            self.back_statue = False
            self.back_button.reset()
            self.pen_button.reset()
            self.eraser_button.reset()
            self.spawn_button.reset()
            self.row_unit.reset()
            self.col_unit.reset()
            self.confirm_button.reset()
            self.read_button.reset()
            self.save_button.reset()
            self.new_button.reset()
            if self.has_saved:
                manager.jump_to(manager.scenelists["MenuScene"])
            else:
                self.lpress = False
                self.confirm_change = False
                manager.reserve_jump(manager.scenelists["SaveConfirmScene"])
        return super().update(manager)

    def jump_out(self, manager, args=None):
        self.plane = None
        self.back_statue = False
        self.has_saved = True
        self.statue = None
        self.lpress = False
        self.confirm_change = False
        self.file_operate = [False, False, False]
        self.back_button.reset()
        self.pen_button.reset()
        self.eraser_button.reset()
        self.spawn_button.reset()
        self.row_unit.reset()
        self.col_unit.reset()
        self.confirm_button.reset()
        self.read_button.reset()
        self.save_button.reset()
        self.new_button.reset()
        return super().jump_out(manager, args)

    def reset_map(self, new_col, new_row):
        new_map = copy.deepcopy(self.plane.map)
        while new_col > len(new_map[0]):
            for i in new_map:
                i.append(0)
        while new_col < len(new_map[0]):
            for i in new_map:
                i.pop()
        while new_row < len(new_map):
            new_map.pop()
        while new_row > len(new_map):
            new_map.append(copy.deepcopy(new_map[-1]))
            for i in range(len(new_map[-1])):
                new_map[-1][i] = 0
        self.plane = EditPlane(new_map)
        self.has_saved = False

    def create_new_map(self):
        my_map = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 2, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
        self.plane = EditPlane(my_map)
        self.has_saved = False
        self.col_unit.value = self.plane.col
        self.row_unit.value = self.plane.row

    def read_map(self, manager: Scenes.SceneManager):
        mapdist = filedialog.askopenfilename(
            initialdir="/home",
            filetypes=[("地图文件", "*.json")],
            title="选择地图",
        )
        pygame.event.clear()
        old_plane = self.plane
        try:
            with open(mapdist, mode="r") as mapfile:
                my_map = json.load(mapfile)["map"]
                self.plane = EditPlane(my_map)
                self.col_unit.value = self.plane.col
                self.row_unit.value = self.plane.row
                self.has_saved = True
        except Exception:
            manager.reserve_jump(manager.scenelists["ErrorLoadingScene"], [self])
            self.plane = old_plane

    def save_map(self, manager: Scenes.SceneManager):
        has_spawn = False
        for i in range(self.plane.row):
            for j in range(self.plane.col):
                has_spawn = has_spawn or self.plane.map[i][j] == 2
        if not has_spawn:
            manager.reserve_jump(manager.scenelists["ErrorSavingScene"], [self])
            return
        save_dist = filedialog.asksaveasfilename(
            filetypes=[("地图文件", "*.json")], title="选择保存位置", initialdir="/home"
        )
        pygame.event.clear()
        if not save_dist == "":
            with open(save_dist, "w") as file:
                json.dump({"map": self.plane.map, "type": "normal"}, file)
                file.close()
            self.has_saved = True

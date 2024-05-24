from pygame import Surface
import pygame
from tkinter import filedialog
import Button
import Scenes


class MenuScene(Scenes.Scene):
    def __init__(self):
        self.start_button = Button.Button("开始", 1800, 520, 600, 100)
        self.choose_button = Button.Button("选择地图", 1800, 720, 600, 100)
        self.edit_button = Button.Button("地图编辑器", 1800, 920, 600, 100)
        self.jump_statue = ""
        self.choose_statue = False
        super().__init__()

    def update(self, manager: Scenes.SceneManager):
        if self.jump_statue == "start":
            manager.jump_to(
                manager.scenelists["GameScene"], None, [manager.mapdist, manager.screen]
            )
        elif self.jump_statue == "edit":
            manager.jump_to(manager.scenelists["EditScene"])
        if self.choose_statue:
            self.join_in(manager)
            mapdist = filedialog.askopenfilename(
                initialdir="/home",
                filetypes=[("地图文件", "*.json")],
                title="选择地图",
            )
            if not mapdist == "":
                manager.mapdist = mapdist
            pygame.event.clear()
        return super().update(manager)

    def input(self, event: Scenes.Event, scale_x: float, scale_y: float):
        if self.start_button.deal_mouse(event, scale_x, scale_y):
            self.jump_statue = "start"
        if self.edit_button.deal_mouse(event, scale_x, scale_y):
            self.jump_statue = "edit"
        self.choose_statue = self.choose_statue or self.choose_button.deal_mouse(
            event, scale_x, scale_y
        )
        return super().input(event, scale_x, scale_y)

    def draw(self, screen: Surface):
        screen.fill((255, 255, 255))
        pygame.draw.polygon(
            screen,
            (128, 128, 128),
            [[1196, 1028], [1196, 390], [746, 264], [746, 1152]],
        )
        pygame.draw.polygon(
            screen,
            (50, 50, 50),
            [[1196, 1028], [1196, 390], [746, 264], [746, 1152]],
            width=5,
        )
        pygame.draw.polygon(
            screen,
            (150, 150, 150),
            [[746, 1152], [746, 264], [190, 342], [192, 1076]],
        )
        pygame.draw.polygon(
            screen,
            (50, 50, 50),
            [[746, 1152], [746, 264], [190, 342], [192, 1076]],
            width=5,
        )
        self.start_button.draw(screen)
        self.choose_button.draw(screen)
        self.edit_button.draw(screen)
        return super().draw(screen)

    def join_in(self, manager, args=None):
        self.start_button.reset()
        self.choose_button.reset()
        self.jump_statue = ""
        self.choose_statue = False
        return super().join_in(manager, args)

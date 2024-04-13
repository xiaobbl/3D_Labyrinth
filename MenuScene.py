from pygame import Surface
import pygame
from tkinter import filedialog
import Button
import Scenes


class MenuScene(Scenes.Scene):
    def __init__(self):
        self.start_button = Button.Button("开始", 900, 260, 300, 50)
        self.choose_button = Button.Button("选择地图", 900, 360, 300, 50)
        self.edit_button = Button.Button("地图编辑器", 900, 460, 300, 50)
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

    def input(self, event: Scenes.Event):
        if self.start_button.deal_mouse(event):
            self.jump_statue = "start"
        if self.edit_button.deal_mouse(event):
            self.jump_statue = "edit"
        self.choose_statue = self.choose_statue or self.choose_button.deal_mouse(event)
        return super().input(event)

    def draw(self, screen: Surface):
        screen.fill((255, 255, 255))
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

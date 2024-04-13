import sys
import pygame
from pygame.event import Event


class Scene:
    def __init__(self):
        pass

    def update(self, manager):
        pass

    def join_in(self, manager, args=None):
        pass

    def jump_out(self, manager, args=None):
        pass

    def draw(self, screen: pygame.Surface):
        pass

    def input(self, event: pygame.event.Event):
        pass


class SceneManager:
    def __init__(
        self,
        first_scene: Scene,
        SceneLists: dict,
        screen: pygame.Surface,
        first_joinin_args,
    ):
        self.current_scene = first_scene
        self.scenelists = SceneLists
        self.screen = screen
        self.mapdist = "default.json"
        self.reserved_scene = None
        first_scene.join_in(self, first_joinin_args)

    def jump_to(
        self, new_scene: Scene, args_out=None, args_in=None, args_reserved_out=None
    ):
        pygame.event.clear()
        self.current_scene.jump_out(self, args_out)
        if not self.reserved_scene is None:
            self.reserved_scene.jump_out(self, args_reserved_out)
        self.current_scene = new_scene
        new_scene.join_in(self, args_in)

    def update(self):
        self.current_scene.update(self)
        self.current_scene.draw(self.screen)
        pygame.display.update()

    def input(self, list: list):
        for i in list:
            if i.type == pygame.QUIT:
                sys.exit(0)
            else:
                self.current_scene.input(i)

    def reserve_jump(self, new_scene: Scene, args_in=None):
        self.reserved_scene = self.current_scene
        self.current_scene = new_scene
        self.current_scene.join_in(self, args_in)

    def reserve_back(self, args_out=None):
        self.current_scene.jump_out(args_out)
        self.current_scene = self.reserved_scene
        self.reserved_scene = None

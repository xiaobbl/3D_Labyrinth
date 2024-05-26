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

    def input(self, event: pygame.event.Event, scale_x: float, scale_y: float):
        pass


class SceneManager:
    def __init__(
        self,
        first_scene: Scene,
        SceneLists: dict,
        window: pygame.Surface,
        screen: pygame.Surface,
        first_joinin_args,
    ):
        self.current_scene = first_scene
        self.scenelists = SceneLists
        self.screen = screen
        self.mapdist = "default.json"
        self.reserved_scene = None
        self.width = 1280
        self.height = 720
        self.full_window = False
        self.window = window
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
        self.width, self.height = self.window.get_width(), self.window.get_height()
        pygame.transform.scale(self.screen, (self.width, self.height), self.window)
        pygame.display.update()

    def input(self, list: list):
        for i in list:
            if i.type == pygame.QUIT:
                sys.exit(0)
            else:
                if i.type == pygame.KEYUP and i.key == pygame.K_F11:
                    if self.full_window:
                        pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
                    else:
                        info = pygame.display.list_modes()
                        pygame.display.set_mode(info[0], pygame.FULLSCREEN)
                    self.full_window = not self.full_window
                self.width, self.height = (
                    self.window.get_width(),
                    self.window.get_height(),
                )
                self.current_scene.input(i, self.width / 2560, self.height / 1440)

    def reserve_jump(self, new_scene: Scene, args_in=None):
        self.reserved_scene = self.current_scene
        self.current_scene = new_scene
        self.current_scene.join_in(self, args_in)

    def reserve_back(self, args_out=None):
        self.current_scene.jump_out(args_out)
        self.current_scene = self.reserved_scene
        self.reserved_scene = None

    def render_word(self, message: str, size: int):  ##架构不良导致屎山的典型案例
        self.window.fill((255, 255, 255))
        font = pygame.font.Font(pygame.font.match_font("SimSun"), size)
        text = font.render(message, True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = self.window.get_width() / 2
        textRect.centery = self.window.get_height() / 2
        self.window.blit(text, textRect)
        pygame.display.update()
        pass

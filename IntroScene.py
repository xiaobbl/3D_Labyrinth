import Scenes
import Button
import pygame


class ErrorLoadingScene(Scenes.Scene):
    def __init__(self, message):
        self.confirm_button = Button.Button("确认", 1280, 920, 1000, 140)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 120)
        self.text = self.font.render(message, True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 1280
        self.textRect.centery = 600
        self.jump_to = None
        self.jump_statue = False
        super().__init__()

    def join_in(self, manager, args):  ##args第一位存储跳转目标
        self.jump_to = args[0]
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(280, 140, 2000, 1160)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 10, 6)
        screen.blit(self.text, self.textRect)
        self.confirm_button.draw(screen)
        return super().draw(screen)

    def update(self, manager: Scenes.SceneManager):
        if self.jump_statue:
            if type(self.jump_to) == str:
                manager.jump_to(manager.scenelists[self.jump_to])
            else:
                manager.reserve_back()
        return super().update(manager)

    def jump_out(self, manager, args=None):
        self.confirm_button.reset()
        self.jump_statue = False
        self.jump_to = None
        return super().jump_out(manager, args)

    def input(self, event: Scenes.Event, scale_x: float, scale_y: float):
        self.jump_statue = self.confirm_button.deal_mouse(event, scale_x, scale_y)
        return super().input(event, scale_x, scale_y)


class PauseScene(Scenes.Scene):
    def __init__(self):
        self.continue_button = Button.Button("继续", 1280, 800, 1000, 140)
        self.back_button = Button.Button("返回", 1280, 1000, 1000, 140)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun", bold=True), 200)
        self.text = self.font.render("暂停", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 1280
        self.textRect.centery = 500
        self.continue_statue = False
        self.back_statue = False
        super().__init__()

    def join_in(self, manager, args):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.mouse.set_pos([640, 360])
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(280, 140, 2000, 1160)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 10, 6)
        screen.blit(self.text, self.textRect)
        self.continue_button.draw(screen)
        self.back_button.draw(screen)
        return super().draw(screen)

    def update(self, manager: Scenes.SceneManager):
        if self.continue_statue:
            manager.reserve_back()
        if self.back_statue:
            manager.jump_to(manager.scenelists["MenuScene"])
        return super().update(manager)

    def jump_out(self, manager, args=None):
        self.continue_button.reset()
        self.back_button.reset()
        self.continue_statue = False
        self.back_statue = False
        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        return super().jump_out(manager, args)

    def input(self, event: Scenes.Event, scale_x: float, scale_y: float):
        self.continue_statue = (
            self.continue_statue
            or self.continue_button.deal_mouse(event, scale_x, scale_y)
            or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE)
        )
        self.back_statue = self.back_statue or self.back_button.deal_mouse(
            event, scale_x, scale_y
        )
        return super().input(event, scale_x, scale_y)


class SaveConfirmScene(Scenes.Scene):
    def __init__(self):
        self.continue_button = Button.Button("继续", 1280, 800, 1000, 140)
        self.back_button = Button.Button("取消", 1280, 1000, 1000, 140)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun", bold=True), 120)
        self.text = self.font.render("还未保存，是否继续退出？", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 1280
        self.textRect.centery = 500
        self.continue_statue = False
        self.back_statue = False
        super().__init__()

    def join_in(self, manager, args):
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(280, 140, 2000, 1160)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 10, 6)
        screen.blit(self.text, self.textRect)
        self.continue_button.draw(screen)
        self.back_button.draw(screen)
        return super().draw(screen)

    def update(self, manager: Scenes.SceneManager):
        if self.back_statue:
            manager.reserve_back()
        if self.continue_statue:
            manager.jump_to(manager.scenelists["MenuScene"])
        return super().update(manager)

    def jump_out(self, manager, args=None):
        self.continue_button.reset()
        self.back_button.reset()
        self.continue_statue = False
        self.back_statue = False
        return super().jump_out(manager, args)

    def input(self, event: Scenes.Event, scale_x: float, scale_y: float):
        self.back_statue = self.back_statue or self.back_button.deal_mouse(
            event, scale_x, scale_y
        )
        self.continue_statue = self.continue_statue or self.continue_button.deal_mouse(
            event, scale_x, scale_y
        )
        return super().input(event, scale_x, scale_y)

import Scenes
import Button
import pygame


class ErrorLoadingScene(Scenes.Scene):
    def __init__(self, message):
        self.confirm_button = Button.Button("确认", 640, 460, 500, 70)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 60)
        self.text = self.font.render(message, True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 640
        self.textRect.centery = 300
        self.jump_to = None
        self.jump_statue = False
        super().__init__()

    def join_in(self, manager, args):  ##args第一位存储跳转目标
        self.jump_to = args[0]
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(140, 70, 1000, 580)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 5, 3)
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

    def input(self, event: Scenes.Event):
        self.jump_statue = self.confirm_button.deal_mouse(event)
        return super().input(event)


class PauseScene(Scenes.Scene):
    def __init__(self):
        self.continue_button = Button.Button("继续", 640, 400, 500, 70)
        self.back_button = Button.Button("返回", 640, 500, 500, 70)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun", bold=True), 100)
        self.text = self.font.render("暂停", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 640
        self.textRect.centery = 250
        self.continue_statue = False
        self.back_statue = False
        super().__init__()

    def join_in(self, manager, args):
        pygame.mouse.set_visible(True)
        pygame.event.set_grab(False)
        pygame.mouse.set_pos([640, 360])
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(140, 70, 1000, 580)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 5, 3)
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

    def input(self, event: Scenes.Event):
        self.continue_statue = (
            self.continue_statue
            or self.continue_button.deal_mouse(event)
            or (event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE)
        )
        self.back_statue = self.back_statue or self.back_button.deal_mouse(event)
        return super().input(event)


class SaveConfirmScene(Scenes.Scene):
    def __init__(self):
        self.continue_button = Button.Button("继续", 640, 400, 500, 70)
        self.back_button = Button.Button("取消", 640, 500, 500, 70)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun", bold=True), 60)
        self.text = self.font.render("还未保存，是否继续退出？", True, (255, 255, 255))
        self.textRect = self.text.get_rect()
        self.textRect.centerx = 640
        self.textRect.centery = 250
        self.continue_statue = False
        self.back_statue = False
        super().__init__()

    def join_in(self, manager, args):
        return super().join_in(manager, args)

    def draw(self, screen: pygame.Surface):
        fill_rect = pygame.Rect(140, 70, 1000, 580)
        screen.fill((180, 180, 180), fill_rect)
        pygame.draw.rect(screen, (70, 70, 70), fill_rect, 5, 3)
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

    def input(self, event: Scenes.Event):
        self.back_statue = self.back_statue or self.back_button.deal_mouse(event)
        self.continue_statue = self.continue_statue or self.continue_button.deal_mouse(
            event
        )
        return super().input(event)

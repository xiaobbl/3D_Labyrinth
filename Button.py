import pygame


class Button:
    def __init__(self, message: str, centerx, centery, width, height):
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 30)
        self.text = self.font.render(message, True, (255, 255, 255))
        self.mouse_in = False
        self.lbuttondown = False
        self.rect = pygame.Rect(
            centerx - width // 2, centery - height // 2, width, height
        )
        self.centery = centery
        self.centerx = centerx
        self.width = width
        self.height = height

    def deal_mouse(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.lbuttondown = False
            return self.mouse_in
        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            self.mouse_in = (
                abs(x - self.centerx) <= self.width // 2
                and abs(y - self.centery) <= self.height // 2
            )
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.lbuttondown = event.button == 1
        return False

    def draw(self, screen: pygame.Surface):
        width = 12
        color = (211, 211, 211)
        if self.mouse_in:
            if self.lbuttondown:
                color = (128, 128, 128)
            else:
                color = (169, 169, 169)
            width = 14
        pygame.draw.rect(screen, (105, 105, 105), self.rect.inflate(width, width), 0, 6)
        pygame.draw.rect(screen, color, self.rect)
        screen.blit(self.text, self.text.get_rect(center=(self.centerx, self.centery)))

    def reset(self):
        self.lbuttondown, self.mouse_in = False, False


class SettingUnit:
    def __init__(self, x, y, value, vbreak, min, max, message):
        self.value = value
        self.vbreak = vbreak
        self.min = min
        self.max = max
        self.x = x
        self.sub = (x + 100 + 20, y + 25)
        self.add = (self.sub[0] + 150 + 20, y + 25)
        self.add_button = Button("+", self.add[0], self.add[1], 40, 40)
        self.sub_button = Button("-", self.sub[0], self.sub[1], 40, 40)
        self.font = pygame.font.Font(pygame.font.match_font("SimSun"), 30)
        self.change_statue = None
        self.text1 = self.font.render(message, True, (0, 0, 0))
        self.text2 = self.font.render(str(self.value), True, (0, 0, 0))
        self.rect1 = self.text1.get_rect()
        self.rect2 = self.text2.get_rect()

    def draw(self, screen: pygame.Surface):
        screen.blit(self.text1, self.rect1)
        screen.blit(self.text2, self.rect2)
        self.add_button.draw(screen)
        self.sub_button.draw(screen)

    def input(self, event: pygame.event.Event):
        if self.add_button.deal_mouse(event):
            self.change_statue = "+"
        elif self.sub_button.deal_mouse(event):
            self.change_statue = "-"
        else:
            self.change_statue = None

    def update(self):
        self.text2 = self.font.render(str(self.value), True, (0, 0, 0))
        self.rect2 = self.text2.get_rect()
        self.rect1.bottomleft = (self.x, self.rect1.bottom)
        self.rect1.centery = self.sub[1]
        self.rect2.centerx = (self.sub[0] + self.add[0]) // 2
        self.rect2.centery = self.sub[1]
        if not self.change_statue == None:
            new_value = eval(str(self.value) + self.change_statue + str(self.vbreak))
            self.change_statue = None
            if new_value < self.min:
                self.value = self.min
            elif new_value > self.max:
                self.value = self.max
            else:
                self.value = new_value
        return self.value

    def reset(self):
        self.change_statue = None

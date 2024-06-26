import Scenes
import GameScene
import MenuScene
import IntroScene
import EditScene
import pygame
import time

pygame.init()
pygame.display.set_icon(pygame.image.load("icon.ico"))
pygame.display.set_caption("3D_Labyrinth")
screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
screen2 = pygame.Surface((2560, 1440))
scene_lists = {}
scene_lists["GameScene"] = GameScene.GameScene()
scene_lists["MenuScene"] = MenuScene.MenuScene()
scene_lists["ErrorLoadingScene"] = IntroScene.ErrorLoadingScene("加载地图时发生错误")
scene_lists["ErrorSavingScene"] = IntroScene.ErrorLoadingScene("请至少选择一个出生点！")
scene_lists["PauseScene"] = IntroScene.PauseScene()
scene_lists["EditScene"] = EditScene.EditScene()
scene_lists["SaveConfirmScene"] = IntroScene.SaveConfirmScene()
manager = Scenes.SceneManager(
    scene_lists["MenuScene"], scene_lists, screen, screen2, [None, screen]
)
while True:
    start = time.time()
    manager.input(pygame.event.get())
    manager.update()
    end = time.time()
    """ print(end - start) """
    if end - start < 0.007:
        time.sleep(0.007 - end + start)

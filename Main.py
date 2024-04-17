import Scenes
import GameScene
import MenuScene
import IntroScene
import EditScene
import pygame
import time

pygame.init()
screen = pygame.display.set_mode((1280, 720))
scene_lists = {}
scene_lists["GameScene"] = GameScene.GameScene()
scene_lists["MenuScene"] = MenuScene.MenuScene()
scene_lists["ErrorLoadingScene"] = IntroScene.ErrorLoadingScene("加载地图时发生错误")
scene_lists["ErrorSavingScene"] = IntroScene.ErrorLoadingScene("请至少选择一个出生点！")
scene_lists["PauseScene"] = IntroScene.PauseScene()
scene_lists["EditScene"] = EditScene.EditScene()
scene_lists["SaveConfirmScene"] = IntroScene.SaveConfirmScene()
manager = Scenes.SceneManager(
    scene_lists["MenuScene"], scene_lists, screen, [None, screen]
)
while True:
    start = time.time()
    manager.input(pygame.event.get())
    manager.update()
    end = time.time()
    if end - start < 0.007:
        time.sleep(0.007 - end + start)

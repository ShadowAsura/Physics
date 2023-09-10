import pygame


class SceneManager:
    def __init__(self):
        from .MenuScene import MainMenuScene
        self.current_scene = MainMenuScene(self)

    def switch_to_scene(self, new_scene):
        self.current_scene = new_scene

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)

    def handle_event(self, event):
        self.current_scene.handle_event(event, self)
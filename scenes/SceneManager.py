import pygame


class SceneManager:
    def __init__(self):
        from .MenuScene import MainMenuScene  # Check if this import is correct or necessary.
        self.current_scene = MainMenuScene(self)

    def switch_to_scene(self, new_scene):

        self.current_scene = new_scene

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)

    def handle_event(self, event, scene_manager):
        self.current_scene.handle_event(event, self)  # pass self as scene_manager to current_scene
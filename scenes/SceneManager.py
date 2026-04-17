import pygame


class SceneManager:
    def __init__(self):
        from .MenuScene import MainMenuScene  # Check if this import is correct or necessary.
        from .SpringScene import SpringScene
        from .FluidScene import FluidScene
        from .SoftBodyScene import SoftBodyScene
        from .PendulumScene import PendulumScene
        self.scene_registry = {
            "menu": MainMenuScene,
            "spring": SpringScene,
            "fluid": FluidScene,
            "softbody": SoftBodyScene,
            "pendulum": PendulumScene,
        }
        self.current_scene = MainMenuScene(self)

    def switch_to_scene(self, new_scene):

        self.current_scene = new_scene

    def switch_to(self, scene_key):
        scene_cls = self.scene_registry[scene_key]
        if scene_key == "menu":
            self.current_scene = scene_cls(self)
        else:
            self.current_scene = scene_cls()

    def update(self, dt):
        self.current_scene.update(dt)

    def draw(self, screen):
        self.current_scene.draw(screen)

    def handle_event(self, event, scene_manager):
        self.current_scene.handle_event(event, self)  # pass self as scene_manager to current_scene
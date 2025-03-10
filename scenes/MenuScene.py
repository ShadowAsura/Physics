import pygame
from .Scene import Scene
from .SceneManager import SceneManager
from .FluidScene import FluidScene
from .SoftBodyScene import SoftBodyScene
from .SpringScene import SpringScene
from .PendulumScene import PendulumScene

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class MainMenuScene(Scene):
    def __init__(self, scene_manager):
        super().__init__()
        self.scene_manager = scene_manager
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["SoftBody", "Spring", "Fluid", "Pendulum"]
        self.buttons = [self.font.render(option, True, BLACK) for option in self.options]

    def draw(self, screen):
        screen.fill(WHITE)
        for index, button in enumerate(self.buttons):
            screen.blit(button, (SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))

    def handle_event(self, event, scene_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button down event captured in MainMenuScene!")  # Debugging print statement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for index, button in enumerate(self.buttons):
                button_rect = button.get_rect(topleft=(SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    # Switch to the corresponding scene
                    if self.options[index] == "Fluid":
                        self.scene_manager.switch_to_scene(FluidScene())
                    elif self.options[index] == "SoftBody":
                        self.scene_manager.switch_to_scene(SoftBodyScene())
                    elif self.options[index] == "Spring":  # Gotta check the right option
                        self.scene_manager.switch_to_scene(SpringScene())
                    elif self.options[index] == "Pendulum":  # Same deal here
                        self.scene_manager.switch_to_scene(PendulumScene())
                    # Add other scenes as needed




                    
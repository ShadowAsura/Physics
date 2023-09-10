import pygame
from .Scene import Scene

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["SoftBody", "Spring", "Fluid"]
        self.buttons = [self.font.render(option, True, BLACK) for option in self.options]

    def draw(self, screen):
        screen.fill(WHITE)
        for index, button in enumerate(self.buttons):
            screen.blit(button, (SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button down event captured in SoftBodyScene!")  # Debugging print statement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for index, button in enumerate(self.buttons):
                button_rect = button.get_rect(topleft=(SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    # Switch to the corresponding scene
                    if self.options[index] == "Fluid":
                        scene_manager.switch_to_scene(FluidScene())
                    elif self.options[index] == "SoftBody":
                        scene_manager.switch_to_scene(SoftBodyScene())
                    if self.options[index] == "Spring":
                        scene_manager.switch_to_scene(SpringScene())
                    # Add other scenes as needed
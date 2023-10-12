import pygame
import numpy as np
from .Scene import Scene

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GRID_SIZE = (80, 60)  # Reduced for simplicity; Adjust as per requirement

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class FluidScene(Scene):
    def __init__(self):
        super().__init__()
        self.velocity = np.zeros((GRID_SIZE[0], GRID_SIZE[1], 2))
        self.density = np.zeros(GRID_SIZE)
        self.pressure = np.zeros(GRID_SIZE)
        self.right_arrow_rect = pygame.Rect(740, 540, 40, 20)
        self.left_arrow_rect = pygame.Rect(690, 540, 40, 20)
        self.cell_size = (SCREEN_WIDTH//GRID_SIZE[0], SCREEN_HEIGHT//GRID_SIZE[1])

    def update(self):
        dt = 0.016  # Assuming 60 FPS

        # 2. Apply Navier-Stokes Equations (Basic Euler Integration Example)
        # 3. Advection
        # 4. Diffusion
        # 5. Pressure Projection
        # [Implement further physics here; placeholder for computational fluid dynamics]

        # Simple Density Dispersion (Example: spreading a "color" or "density" in the fluid)
        self.density = self.density * 0.99  # Simple decay for demonstration
        # [Implement Advection, Diffusion, and Pressure Projection for accurate fluid simulation]

    def handle_event(self, event, scene_manager):
        # Mouse and Switching Scene Events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.right_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .SoftBodyScene import SoftBodyScene
                scene_manager.switch_to_scene(SoftBodyScene())
            elif self.left_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .SpringScene import SpringScene
                scene_manager.switch_to_scene(SpringScene())
            else:
                # Adding Density on Mouse Click (Example: injecting "color" or "density" into the fluid)
                grid_x, grid_y = mouse_x//self.cell_size[0], mouse_y//self.cell_size[1]
                self.density[grid_x, grid_y] = min(255, self.density[grid_x, grid_y]+50)

    def draw(self, screen):
        screen.fill(WHITE)

        # 7. Rendering
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                pygame.draw.rect(screen,
                                 (min(255, self.density[i, j]),) * 3,
                                 (i*self.cell_size[0], j*self.cell_size[1], self.cell_size[0], self.cell_size[1]))

        # Drawing Right Arrow Button
        pygame.draw.polygon(screen, BLACK, [
            (self.right_arrow_rect.x, self.right_arrow_rect.y),
            (self.right_arrow_rect.x + self.right_arrow_rect.width, self.right_arrow_rect.y + self.right_arrow_rect.height // 2),
            (self.right_arrow_rect.x, self.right_arrow_rect.y + self.right_arrow_rect.height)
        ])
        
        # Drawing Left Arrow Button
        pygame.draw.polygon(screen, BLACK, [
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y),
            (self.left_arrow_rect.x, self.left_arrow_rect.y + self.left_arrow_rect.height // 2),
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y + self.left_arrow_rect.height)
        ])

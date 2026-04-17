import pygame
try:
    import numpy as np
    HAS_NUMPY = True
except Exception:
    np = None
    HAS_NUMPY = False
from engine.config import config

# Setup stuff
GRID_SIZE = (80, 60) 
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

class FluidScene():
    def __init__(self):
        self.numpy_available = HAS_NUMPY
        self.mouse_down = False
        if not self.numpy_available:
            self.unavailable_message = "Fluid scene unavailable: NumPy is missing in this build."
            self.cell_size = (1, 1)
            return

        self.density = np.zeros(GRID_SIZE) 
        self.new_density = np.zeros_like(self.density)
        self.velocity = np.array(np.meshgrid(
            np.linspace(-0.5, 0.5, GRID_SIZE[1]), 
            np.linspace(-0.5, 0.5, GRID_SIZE[0])
        )).transpose(1, 2, 0)
        self.diffusion_rate = 0.1
        self.dt = 0.016
        self.cell_size = (config.width // GRID_SIZE[0], config.height // GRID_SIZE[1])

    def compute_speed(self, i, j):
        """Compute speed based on the velocity vector at a given grid cell."""
        return np.linalg.norm(self.velocity[i, j])
    def map_speed_to_color(self, speed):
        """Map speed to a color gradient: Blue for low speed, Red for high speed."""
        MAX_SPEED = 1.0  # Tweak this if colors look weird
        f = min(1, speed / MAX_SPEED)
        r = int(255 * f)
        b = int(255 * (1 - f))
        return (r, 0, b)
    def update(self, dt):
        if not self.numpy_available:
            return

        self.dt = dt
        self.advection()
        self.diffusion()
        if self.mouse_down:
            mx, my = pygame.mouse.get_pos()
            grid_x, grid_y = mx//self.cell_size[0], my//self.cell_size[1]
            self.density[grid_x, grid_y] += 10
            self.velocity[grid_x, grid_y, 1] += 0.1  # Give it a lil push down
        self.velocity[0, :, 0] = 0
        self.velocity[-1, :, 0] = 0
        self.velocity[:, 0, 1] = 0
        self.velocity[:, -1, 1] = 0
        self.density *= 0.99





    def advection(self):
        if not self.numpy_available:
            return

        # Move the fluid around based on speed
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                x, y = i - self.velocity[i, j, 1] * self.dt * GRID_SIZE[0], j - self.velocity[i, j, 0] * self.dt * GRID_SIZE[1]
                x, y = max(0, min(GRID_SIZE[0]-1, x)), max(0, min(GRID_SIZE[1]-1, y))
                self.new_density[i, j] = self.density[int(x), int(y)]
        self.density[:] = self.new_density[:]

    def diffusion(self):
        if not self.numpy_available:
            return

        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                self.new_density[i, j] = (1 - self.diffusion_rate) * self.density[i, j] + \
                                         (self.diffusion_rate/4) * sum(self.density[x, y] for x, y in neighbors if 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1])
        self.density[:] = self.new_density[:]

    def handle_event(self, event, _=None):
        if not self.numpy_available:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False

    def draw_velocity(self, screen):
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                start_pos = (i*self.cell_size[0] + self.cell_size[0]//2, j*self.cell_size[1] + self.cell_size[1]//2)
                end_pos = (start_pos[0] + self.velocity[i, j, 0]*self.cell_size[0]*2, start_pos[1] + self.velocity[i, j, 1]*self.cell_size[1]*2)
                pygame.draw.line(screen, BLACK, start_pos, end_pos, 1)

    def draw(self, screen):
        if not self.numpy_available:
            screen.fill(WHITE)
            title_font = pygame.font.SysFont(None, 42)
            body_font = pygame.font.SysFont(None, 28)

            title = title_font.render("Fluid Scene Unavailable", True, BLACK)
            line1 = body_font.render("NumPy is required for this simulation.", True, BLACK)
            line2 = body_font.render("Use desktop app for full fluid simulation.", True, BLACK)

            screen.blit(title, (config.width // 2 - title.get_width() // 2, config.height // 2 - 60))
            screen.blit(line1, (config.width // 2 - line1.get_width() // 2, config.height // 2 - 10))
            screen.blit(line2, (config.width // 2 - line2.get_width() // 2, config.height // 2 + 24))
            return

        screen.fill(WHITE)
        # Make it look pretty
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                speed = self.compute_speed(i, j)
                speed_color = self.map_speed_to_color(speed)
                dye_intensity = int(self.density[i, j] * 255)
                combined_color = (min(255, speed_color[0] + dye_intensity), 0, min(255, speed_color[2] + dye_intensity))
                pygame.draw.rect(screen, combined_color, (i * self.cell_size[0], j * self.cell_size[1], self.cell_size[0], self.cell_size[1]))
        self.draw_velocity(screen)

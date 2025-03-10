import pygame
import numpy as np

# Setup stuff
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
GRID_SIZE = (80, 60) 
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

class FluidScene():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Fluid Simulation")
        self.clock = pygame.time.Clock()
        self.running = True

        self.density = np.zeros(GRID_SIZE) 
        self.new_density = np.zeros_like(self.density)
        self.velocity = np.array(np.meshgrid(
            np.linspace(-0.5, 0.5, GRID_SIZE[1]), 
            np.linspace(-0.5, 0.5, GRID_SIZE[0])
        )).transpose(1, 2, 0)
        self.diffusion_rate = 0.1
        self.dt = 0.016
        self.cell_size = (SCREEN_WIDTH//GRID_SIZE[0], SCREEN_HEIGHT//GRID_SIZE[1])
        self.mouse_down = False
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
    def update(self):
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
        # Move the fluid around based on speed
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                x, y = i - self.velocity[i, j, 1] * self.dt * GRID_SIZE[0], j - self.velocity[i, j, 0] * self.dt * GRID_SIZE[1]
                x, y = max(0, min(GRID_SIZE[0]-1, x)), max(0, min(GRID_SIZE[1]-1, y))
                self.new_density[i, j] = self.density[int(x), int(y)]
        self.density[:] = self.new_density[:]

    def diffusion(self):
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                neighbors = [(i-1, j), (i+1, j), (i, j-1), (i, j+1)]
                self.new_density[i, j] = (1 - self.diffusion_rate) * self.density[i, j] + \
                                         (self.diffusion_rate/4) * sum(self.density[x, y] for x, y in neighbors if 0 <= x < GRID_SIZE[0] and 0 <= y < GRID_SIZE[1])
        self.density[:] = self.new_density[:]

    def handle_event(self, event, _=None):
        if event.type == pygame.QUIT:
            self.running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.mouse_down = False

    def draw_velocity(self):
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                start_pos = (i*self.cell_size[0] + self.cell_size[0]//2, j*self.cell_size[1] + self.cell_size[1]//2)
                end_pos = (start_pos[0] + self.velocity[i, j, 0]*self.cell_size[0]*2, start_pos[1] + self.velocity[i, j, 1]*self.cell_size[1]*2)
                pygame.draw.line(self.screen, BLACK, start_pos, end_pos, 1)

    def draw(self, _=None):
        self.screen.fill(WHITE)
        # Make it look pretty
        for i in range(GRID_SIZE[0]):
            for j in range(GRID_SIZE[1]):
                speed = self.compute_speed(i, j)
                speed_color = self.map_speed_to_color(speed)
                dye_intensity = int(self.density[i, j] * 255)
                combined_color = (min(255, speed_color[0] + dye_intensity), 0, min(255, speed_color[2] + dye_intensity))
                pygame.draw.rect(self.screen, combined_color, (i * self.cell_size[0], j * self.cell_size[1], self.cell_size[0], self.cell_size[1]))
        self.draw_velocity()


    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_event(event)
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(60)

if __name__ == "__main__":
    FluidScene().run()
    pygame.quit()

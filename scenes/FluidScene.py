import pygame
import math
from engine.FluidParticle import FluidParticle

from .Scene import Scene

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class FluidScene(Scene):
    def __init__(self):
        super().__init__()
        self.particles = [FluidParticle(x, y) for x in range(50, 400, 20) for y in range(50, 400, 20)]
        self.right_arrow_rect = pygame.Rect(740, 540, 40, 20)
        self.left_arrow_rect = pygame.Rect(690, 540, 40, 20)

    def update(self):
        dt = 0.016  # Assuming 60 FPS
        for particle in self.particles:
            particle.apply_force(pygame.Vector2(0, 0.1))  # Apply gravity
            particle.update(dt)

        for i in range(len(self.particles)):
            self.particles[i].update(dt)
            self.particles[i].check_collision_with_wall(SCREEN_WIDTH, SCREEN_HEIGHT)
            for j in range(i + 1, len(self.particles)):
                self.particles[i].check_collision_with_particle(self.particles[j])

                
    def check_particle_collision(self, p1, p2):
        distance = p1.position.distance_to(p2.position)
        if distance == 0:
            return
        min_distance = p1.radius + p2.radius
        if distance < min_distance:
            # Resolve collision by moving particles away from each other
            # This is a simple and somewhat inaccurate method, but works for demonstration
            overlap = min_distance - distance
            correction = (overlap / distance) * 0.5
            p1.position -= correction * (p1.position - p2.position)
            p2.position += correction * (p1.position - p2.position)
            
            # Reverse velocity to simulate a bounce
            p1.velocity *= -0.5
            p2.velocity *= -0.5

    def handle_event(self, event, scene_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_vec = pygame.Vector2(mouse_x, mouse_y)
            if self.right_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .SoftBodyScene import SoftBodyScene  # Import here instead of at the top of the file
                scene_manager.switch_to_scene(SoftBodyScene())
            elif self.left_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .SpringScene import SpringScene  # Import here instead of at the top of the file
                scene_manager.switch_to_scene(SpringScene())

    def draw(self, screen):
        screen.fill((255, 255, 255))

        # Drawing Right Arrow Button
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.right_arrow_rect.x, self.right_arrow_rect.y),
            (self.right_arrow_rect.x + self.right_arrow_rect.width, self.right_arrow_rect.y + self.right_arrow_rect.height // 2),
            (self.right_arrow_rect.x, self.right_arrow_rect.y + self.right_arrow_rect.height)
        ])
        
        # Drawing Left Arrow Button
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y),
            (self.left_arrow_rect.x, self.left_arrow_rect.y + self.left_arrow_rect.height // 2),
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y + self.left_arrow_rect.height)
        ])

        for particle in self.particles:
            particle.draw(screen)
import pygame
import pygame.gfxdraw
import math

class SoftSpring:
    def __init__(self, particle_a, particle_b, k):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.rest_length = self.particle_a.position.distance_to(self.particle_b.position)
        self.k = k
        self.base_rest_length = self.rest_length

    def update(self):
        displacement = self.rest_length - self.particle_a.position.distance_to(self.particle_b.position)
        force_magnitude = self.k * displacement
        force_direction = (self.particle_b.position - self.particle_a.position).normalize()

        # Apply the force to each particle
        self.particle_a.apply_force(-force_direction * force_magnitude)
        self.particle_b.apply_force(force_direction * force_magnitude)

    def draw(self, screen):
        pygame.draw.aaline(screen, (0, 0, 0), (int(self.particle_a.position[0]), int(self.particle_a.position[1])), (int(self.particle_b.position[0]), int(self.particle_b.position[1])))




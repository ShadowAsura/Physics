import pygame
import math


class Particle:
    def __init__(self, x, y, mass=1.0):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = mass
        self.forces = pygame.Vector2(0, 0)
        self.radius = 30
        self.damping = 0.98

    def apply_force(self, force):
        self.forces += force

    def integrate(self, dt):
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.forces = pygame.Vector2(0, 0)
        self.velocity *= self.damping

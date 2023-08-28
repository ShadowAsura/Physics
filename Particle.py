import pygame

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class Particle:
    def __init__(self, x, y, mass=1.0, screen_width=800, screen_height=600):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.mass = mass
        self.forces = pygame.Vector2(0, 0)
        self.radius = 30
        self.damping = 0.99
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height

    def apply_force(self, force):
        self.forces += force

    def integrate(self, dt):
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.forces = pygame.Vector2(0, 0)
        self.velocity *= self.damping

        # Boundary checks
        if self.position.x < self.radius:
            self.position.x = self.radius
            self.velocity.x *= -1
        elif self.position.x > self.SCREEN_WIDTH - self.radius:
            self.position.x = self.SCREEN_WIDTH - self.radius
            self.velocity.x *= -1

        if self.position.y < self.radius:
            self.position.y = self.radius
            self.velocity.y *= -1
        elif self.position.y > self.SCREEN_HEIGHT - self.radius:
            self.position.y = self.SCREEN_HEIGHT - self.radius
            self.velocity.y *= -1

    def apply_gravity(self):
        GRAVITY = pygame.Vector2(0, 0.5)
        self.forces += GRAVITY * self.mass

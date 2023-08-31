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

    def apply_damping(self, damping_factor=0.01):
        self.velocity *= (1 - damping_factor)

    def check_wall_collision(self, window_width, window_height):
        if self.position.x <= 0 or self.position.x >= window_width:
            self.velocity.x *= -0.9  # Reflect and dampen
        if self.position.y <= 0 or self.position.y >= window_height:
            self.velocity.y *= -0.9  # Reflect and dampen

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

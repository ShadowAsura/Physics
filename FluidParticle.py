import pygame
import random
import math

class FluidParticle:
    def __init__(self, x, y, mass=1.0, radius=5.0):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))  # Wider range
        self.mass = mass
        self.radius = radius
        self.forces = pygame.Vector2(0, 0)
        self.coefficient_of_restitution = 0.9  # Closer to 1 for less energy loss

    def apply_force(self, force):
        self.forces += force

    def apply_gravity(self):
        GRAVITY = pygame.Vector2(0, 9.8)  # Reduced for more 'floaty' behavior
        self.apply_force(GRAVITY * self.mass)

    def update(self, dt):
        self.apply_gravity()
        acceleration = self.forces / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt
        self.forces = pygame.Vector2(0, 0)

    def check_collision_with_wall(self, window_width, window_height):
        if self.position.x - self.radius <= 0 or self.position.x + self.radius >= window_width:
            self.velocity.x *= -self.coefficient_of_restitution
        if self.position.y - self.radius <= 0 or self.position.y + self.radius >= window_height:
            self.velocity.y *= -self.coefficient_of_restitution

    def apply_damping_force(self, other, damping_constant=0.01):
        relative_velocity = self.velocity - other.velocity
        damping_force = -damping_constant * relative_velocity
        self.apply_force(damping_force)
        other.apply_force(-damping_force)



    def check_collision_with_particle(self, other):
        dist_vector = self.position - other.position
        dist = dist_vector.length()
        if dist < self.radius + other.radius:
            overlap = (self.radius + other.radius) - dist
            correction = dist_vector.normalize() * overlap
            self.position += correction * (self.mass / (self.mass + other.mass))
            other.position -= correction * (other.mass / (self.mass + other.mass))

            v1_final = self.velocity - 2 * other.mass / (self.mass + other.mass) * (self.velocity - other.velocity).dot(correction.normalize()) * correction.normalize()
            v2_final = other.velocity - 2 * self.mass / (self.mass + other.mass) * (other.velocity - self.velocity).dot(correction.normalize()) * correction.normalize()
            
            self.velocity = v1_final * self.coefficient_of_restitution
            other.velocity = v2_final * other.coefficient_of_restitution

            self.apply_damping_force(other)

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 0, 255), (int(self.position.x), int(self.position.y)), self.radius)

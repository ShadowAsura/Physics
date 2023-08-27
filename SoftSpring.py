import pygame
import pygame.gfxdraw
import math

class SoftSpring:
    def __init__(self, particle_a, particle_b, stiffness):
        self.particle_a = particle_a
        self.particle_b = particle_b
        self.stiffness = stiffness
        self.rest_length = particle_a.position.distance_to(particle_b.position)

    def draw(self, screen):
        pygame.draw.aaline(screen, (0, 0, 0), (int(self.particle_a.position[0]), int(self.particle_a.position[1])), (int(self.particle_b.position[0]), int(self.particle_b.position[1])))


    def apply_force(self):
        # Calculate the current length of the spring
        current_length = self.particle_a.position.distance_to(self.particle_b.position)
        
        # Calculate the difference from the rest length
        length_difference = current_length - self.rest_length
        
        # Calculate the force magnitude
        force_magnitude = self.stiffness * length_difference
        
        # Calculate the force direction
        force_direction = (self.particle_a.position - self.particle_b.position).normalize()
        
        # Apply the forces to the particles
        self.particle_a.apply_force(-force_direction * force_magnitude)
        self.particle_b.apply_force(force_direction * force_magnitude)
    def update(self, k):
        # Calculate the current distance between the two particles
        distance = self.particle_a.position.distance_to(self.particle_b.position)
        
        # Calculate the difference from the rest length
        difference = distance - self.rest_length
        
        # Calculate the force magnitude using Hooke's law
        force_magnitude = k * difference
        
        # Calculate the force direction
        force_direction = (self.particle_b.position - self.particle_a.position).normalize()
        
        # Apply the force to each particle
        self.particle_a.apply_force(-force_direction * force_magnitude)
        self.particle_b.apply_force(force_direction * force_magnitude)


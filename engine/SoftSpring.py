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
        damping_factor = 0.1  # Tweak this to change bounciness
        stiffness_factor = 0.1  # How stretchy the spring is
        
        force_direction = self.particle_b.position - self.particle_a.position
        if force_direction.length() == 0:
            return
            
        displacement = self.rest_length - self.particle_a.position.distance_to(self.particle_b.position)
        force_magnitude = self.k * displacement * stiffness_factor
        
        force_direction = (self.particle_b.position - self.particle_a.position).normalize()
        damping_force = -damping_factor * (self.particle_a.velocity - self.particle_b.velocity).dot(force_direction) * force_direction
        
        total_force = force_direction * force_magnitude + damping_force
        
        self.particle_a.apply_force(-total_force)
        self.particle_b.apply_force(total_force)


    def draw(self, screen):
        # Grab the two ends of the spring
        p0 = self.particle_a.position  # Where it starts
        p3 = self.particle_b.position  # Where it ends
        
        # Figure out how to make it curvy
        p1 = p0 + (p3 - p0) * 0.3  # Bend point near start
        p2 = p3 - (p3 - p0) * 0.3  # Bend point near end
        
        num_points = 10  # How smooth we want it
        for t in range(num_points):
            t /= num_points
            x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * p1.x + 3 * (1 - t) * t ** 2 * p2.x + t ** 3 * p3.x
            y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * p1.y + 3 * (1 - t) * t ** 2 * p2.y + t ** 3 * p3.y
            
            # You can draw a small circle or point at (x, y) here
            
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1)





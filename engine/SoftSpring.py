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
        damping_factor = 0.1  # Adjust as needed
        stiffness_factor = 0.1  # Adjust as needed
        
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
        # Assuming self.particle_a and self.particle_b are the endpoints of the spring
        p0 = self.particle_a.position  # Start point
        p3 = self.particle_b.position  # End point
        
        # Calculate control points for Bezier curve
        p1 = p0 + (p3 - p0) * 0.3  # Control point near the start
        p2 = p3 - (p3 - p0) * 0.3  # Control point near the end
        
        num_points = 10  # Number of points to interpolate along the curve
        for t in range(num_points):
            t /= num_points
            x = (1 - t) ** 3 * p0.x + 3 * (1 - t) ** 2 * t * p1.x + 3 * (1 - t) * t ** 2 * p2.x + t ** 3 * p3.x
            y = (1 - t) ** 3 * p0.y + 3 * (1 - t) ** 2 * t * p1.y + 3 * (1 - t) * t ** 2 * p2.y + t ** 3 * p3.y
            
            # You can draw a small circle or point at (x, y) here
            
            pygame.draw.circle(screen, (0, 0, 0), (int(x), int(y)), 1)





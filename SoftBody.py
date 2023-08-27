import pygame
import math
from Particle import Particle
from SoftSpring import SoftSpring


class SoftBody:
    def __init__(self, x, y, width, height, particle_mass, spring_stiffness, num_particles):
        self.particles = self.create_particles(x, y, width, height, particle_mass, num_particles)
        self.springs = self.create_springs(spring_stiffness)
        self.dragging = False
        self.dragged_particle = None
        self.spring_stiffness = spring_stiffness

    def create_particles(self, x, y, width, height, particle_mass, num_particles):
        particles = []
        dx = width / (num_particles - 1)
        dy = height / (num_particles - 1)
        for i in range(num_particles):
            for j in range(num_particles):
                particle = Particle(x + i * dx, y + j * dy, particle_mass)
                particles.append(particle)
        return particles

    def create_springs(self, spring_stiffness):
        springs = []
        num_particles = int(len(self.particles) ** 0.5)
        for i in range(num_particles):
            for j in range(num_particles):
                if i < num_particles - 1:
                    springs.append(SoftSpring(self.particles[i * num_particles + j], self.particles[(i + 1) * num_particles + j], spring_stiffness))
                if j < num_particles - 1:
                    springs.append(SoftSpring(self.particles[i * num_particles + j], self.particles[i * num_particles + j + 1], spring_stiffness))
        return springs

    def update(self, dt):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            translation = pygame.Vector2(mouse_x, mouse_y) - self.drag_offset - self.compute_center_of_mass()
            for particle in self.particles:
                particle.position += translation

        for spring in self.springs:
            spring.update(self.spring_stiffness)
        for particle in self.particles:
            particle.integrate(dt)

    def compute_center_of_mass(self):
        center_of_mass = pygame.Vector2(0, 0)
        for particle in self.particles:
            center_of_mass += particle.position
        center_of_mass /= len(self.particles)
        return center_of_mass


    def render(self, screen):
        for spring in self.springs:
            spring.draw(screen)
        for particle in self.particles:
            pygame.draw.circle(screen, (0, 0, 255), (int(particle.position.x), int(particle.position.y)), 5)

        # Draw the center of mass
        com = self.compute_center_of_mass()
        pygame.draw.circle(screen, (255, 0, 0), (int(com.x), int(com.y)), 8)  # Draw a red circle for COM
        pygame.draw.line(screen, (255, 0, 0), (int(com.x) - 10, int(com.y)), (int(com.x) + 10, int(com.y)), 2)  # Horizontal line
        pygame.draw.line(screen, (255, 0, 0), (int(com.x), int(com.y) - 10), (int(com.x), int(com.y) + 10), 2)  # Vertical line



    def handle_mouse_down(self, x, y):
        center_of_mass = self.compute_center_of_mass()
        distance = center_of_mass.distance_to(pygame.Vector2(x, y))
        print(f"Mouse clicked at ({x}, {y}), COM is at {center_of_mass}, distance is {distance}")
        if distance < 20:  # You can adjust this threshold
            print("Starting drag...")
            self.dragging = True
            self.drag_offset = pygame.Vector2(x, y) - center_of_mass



    def handle_mouse_up(self):
        print("Ending drag...")
        self.dragging = False




    def handle_mouse_move(self, mouse_x, mouse_y):
        if self.dragging and self.dragged_particle:
            self.dragged_particle.position.x = mouse_x
            self.dragged_particle.position.y = mouse_y


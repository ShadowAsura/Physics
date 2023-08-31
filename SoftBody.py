import pygame
import math
from Particle import Particle
from SoftSpring import SoftSpring


class SoftBody:
    def __init__(self, x, y, width, height, particle_mass, spring_stiffness, num_particles, screen_width=800, screen_height=600):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.initial_relative_positions = []
        self.particles = self.create_particles(x, y, width, height, particle_mass, num_particles)
        self.springs = self.create_springs(5.0)  # Adjust this value as needed

        self.dragging = False
        self.dragged_particle = None
        self.spring_stiffness = spring_stiffness

        self.drag_force_multiplier = 20.0  # Adjust as needed
        self.restoring_force_multiplier = 0.5  # Adjust as needed
        self.initial_positions = [particle.position.copy() for particle in self.particles]

        self.shake_duration = 0  # Duration for which the shaking effect should last

    def create_particles(self, x, y, width, height, particle_mass, num_particles):
        particles = []
        dx = width / (num_particles - 1)
        dy = height / (num_particles - 1)
        initial_center_of_mass = pygame.Vector2(x + width/2, y + height/2)
        for i in range(num_particles):
            for j in range(num_particles):
                particle = Particle(x + i * dx, y + j * dy, particle_mass, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
                particles.append(particle)
                # Store the initial relative position of each particle
                self.initial_relative_positions.append(particle.position - initial_center_of_mass)
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
        for particle in self.particles:
            particle.check_wall_collision(self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
        for _ in range(5):
            for spring in self.springs:
                spring.update()

        for particle in self.particles:
            particle.apply_damping()
            particle.apply_gravity()
            particle.integrate(dt)

        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            current_center_of_mass = self.compute_center_of_mass()
            translation = pygame.Vector2(mouse_x, mouse_y) - current_center_of_mass

            # Constants
            SPRING_CONSTANT = 0.5  # Adjust this value to change the strength of the wobble

            for particle in self.particles:
                # Apply the translation to move the particle
                particle.position += translation

                # Calculate the displacement of the particle from the center of mass
                displacement = particle.position - current_center_of_mass

                # Calculate the spring force based on the displacement
                spring_force = -SPRING_CONSTANT * displacement

                # Apply the spring force to the particle
                particle.forces += spring_force



        # Constants
        RESTORATIVE_CONSTANT = 1  # Adjust this value to change the strength of the restoration

        current_center_of_mass = self.compute_center_of_mass()
        for i, particle in enumerate(self.particles):
            # Calculate the desired position of the particle relative to the current center of mass
            desired_position = current_center_of_mass + self.initial_relative_positions[i]
            
            # Calculate the displacement from the desired position
            displacement = particle.position - desired_position

            # Calculate the restorative force
            restorative_force = -RESTORATIVE_CONSTANT * displacement

            # Apply the restorative force to the particle
            particle.forces += restorative_force

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
        # If dragging, visualize the drag offset and translation



    def handle_mouse_down(self, x, y):
        center_of_mass = self.compute_center_of_mass()
        distance_to_com = center_of_mass.distance_to(pygame.Vector2(x, y))
        
        if distance_to_com < 20:  # Adjust this threshold as needed
            self.dragging = True
            self.drag_offset = pygame.Vector2(x, y) - center_of_mass






    def handle_mouse_move(self, mouse_x, mouse_y):
        if self.dragging and self.dragged_particle:
            self.dragged_particle.position.x = mouse_x
            self.dragged_particle.position.y = mouse_y


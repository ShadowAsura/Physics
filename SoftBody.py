import pygame
import math
from Particle import Particle
from SoftSpring import SoftSpring


class SoftBody:
    def __init__(self, x, y, width, height, particle_mass, spring_stiffness, num_particles, screen_width=800, screen_height=600):
        self.SCREEN_WIDTH = screen_width
        self.SCREEN_HEIGHT = screen_height
        self.particles = self.create_particles(x, y, width, height, particle_mass, num_particles)
        self.springs = self.create_springs(5.0)  # Adjust this value as needed

        self.dragging = False
        self.dragged_particle = None
        self.spring_stiffness = spring_stiffness


        self.shake_duration = 0  # Duration for which the shaking effect should last

    def create_particles(self, x, y, width, height, particle_mass, num_particles):
        particles = []
        dx = width / (num_particles - 1)
        dy = height / (num_particles - 1)
        for i in range(num_particles):
            for j in range(num_particles):
                particle = Particle(x + i * dx, y + j * dy, particle_mass, self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
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
        for spring in self.springs:
            spring.update()

        for particle in self.particles:
            particle.apply_gravity()
            particle.integrate(dt)

        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            translation = pygame.Vector2(mouse_x, mouse_y) - self.drag_offset - self.compute_center_of_mass()
            for particle in self.particles:
                print("Particle position before:", self.particles[0].position)
                particle.position += translation
                print("Particle position after:", self.particles[0].position)

        for particle in self.particles:
            # Bottom boundary
            if particle.position.y > self.SCREEN_HEIGHT - particle.radius:
                particle.position.y = self.SCREEN_HEIGHT - particle.radius
                particle.velocity.y = -abs(particle.velocity.y)

            # Top boundary
            if particle.position.y < particle.radius:
                particle.position.y = particle.radius
                particle.velocity.y = abs(particle.velocity.y)

            # Right boundary
            if particle.position.x > self.SCREEN_WIDTH - particle.radius:
                particle.position.x = self.SCREEN_WIDTH - particle.radius
                particle.velocity.x = -abs(particle.velocity.x)

            # Left boundary
            if particle.position.x < particle.radius:
                particle.position.x = particle.radius
                particle.velocity.x = abs(particle.velocity.x)

        # If shake_duration is greater than zero, apply a random force to each particle
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            translation = pygame.Vector2(mouse_x, mouse_y) - self.drag_offset - self.compute_center_of_mass()
            print("Translation:", translation)
            for particle in self.particles:
                particle.position += translation

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
        if self.dragging:
            pygame.draw.line(screen, (0, 255, 0), (int(self.drag_offset.x), int(self.drag_offset.y)), (int(self.compute_center_of_mass().x), int(self.compute_center_of_mass().y)), 2)
            pygame.draw.line(screen, (255, 0, 255), (int(self.compute_center_of_mass().x), int(self.compute_center_of_mass().y)), (int(self.compute_center_of_mass().x + self.drag_offset.x), int(self.compute_center_of_mass().y + self.drag_offset.y)), 2)


    def handle_mouse_down(self, x, y):
        center_of_mass = self.compute_center_of_mass()
        distance_to_com = center_of_mass.distance_to(pygame.Vector2(x, y))
        
        if distance_to_com < 20:  # Adjust this threshold as needed
            self.dragging = True
            self.drag_offset = pygame.Vector2(x, y) - center_of_mass
            print("Initial Center of Mass:", center_of_mass)
            print("Drag Offset:", self.drag_offset)
        print(f"Drag Offset: {self.soft_body.drag_offset.x}, {self.soft_body.drag_offset.y}")




    def handle_mouse_move(self, mouse_x, mouse_y):
        print("Mouse Position:", mouse_x, mouse_y)
        if self.dragging:
            translation = pygame.Vector2(mouse_x, mouse_y) - self.drag_offset - self.compute_center_of_mass()
            print("Mouse Position:", (mouse_x, mouse_y))
            print("Translation:", translation)
            for particle in self.particles:
                particle.position += translation
            print("New Center of Mass:", self.compute_center_of_mass())




    def handle_mouse_move(self, mouse_x, mouse_y):
        print("Handling mouse move in SoftBody!")  # Debugging print statement
        if self.dragging and self.dragged_particle:
            self.dragged_particle.position.x = mouse_x
            self.dragged_particle.position.y = mouse_y


import pygame
from SpringChain import SpringChain
from Spring import Spring
from SoftBody import SoftBody
import math
from SpringUI import SpringUI
from PolygonObject import PolygonObject
from FluidParticle import FluidParticle

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Scene:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def handle_event(self, event):
        pass

class MainMenuScene(Scene):
    def __init__(self):
        super().__init__()
        self.font = pygame.font.SysFont(None, 55)
        self.options = ["SoftBody", "Spring", "Fluid"]
        self.buttons = [self.font.render(option, True, BLACK) for option in self.options]

    def draw(self, screen):
        screen.fill(WHITE)
        for index, button in enumerate(self.buttons):
            screen.blit(button, (SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("Mouse button down event captured in SoftBodyScene!")  # Debugging print statement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for index, button in enumerate(self.buttons):
                button_rect = button.get_rect(topleft=(SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    # Switch to the corresponding scene
                    if self.options[index] == "Fluid":
                        scene_manager.switch_to_scene(FluidScene())
                    elif self.options[index] == "SoftBody":
                        scene_manager.switch_to_scene(SoftBodyScene())
                    if self.options[index] == "Spring":
                        scene_manager.switch_to_scene(SpringScene())
                    # Add other scenes as needed
class FluidScene(Scene):
    def __init__(self):
        super().__init__()
        self.particles = [FluidParticle(x, y) for x in range(50, 400, 20) for y in range(50, 400, 20)]

    def update(self):
        dt = 0.016  # Assuming 60 FPS
        for particle in self.particles:
            particle.apply_force(pygame.Vector2(0, 0.1))  # Apply gravity
            particle.update(dt)

        for i in range(len(self.particles)):
            self.particles[i].update(dt)
            self.particles[i].check_collision_with_wall(SCREEN_WIDTH, SCREEN_HEIGHT)
            for j in range(i + 1, len(self.particles)):
                self.particles[i].check_collision_with_particle(self.particles[j])

                
    def check_particle_collision(self, p1, p2):
        distance = p1.position.distance_to(p2.position)
        if distance == 0:
            return
        min_distance = p1.radius + p2.radius
        if distance < min_distance:
            # Resolve collision by moving particles away from each other
            # This is a simple and somewhat inaccurate method, but works for demonstration
            overlap = min_distance - distance
            correction = (overlap / distance) * 0.5
            p1.position -= correction * (p1.position - p2.position)
            p2.position += correction * (p1.position - p2.position)
            
            # Reverse velocity to simulate a bounce
            p1.velocity *= -0.5
            p2.velocity *= -0.5

    def draw(self, screen):
        screen.fill((255, 255, 255))
        for particle in self.particles:
            particle.draw(screen)



class SoftBodyScene(Scene):
    def __init__(self):
        super().__init__()
        # Create a soft body at the center of the screen
        self.soft_body = SoftBody(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200, 1.0, 0.05, 5, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.user_polygons = []  # List to store user-created polygons
        self.dragged_particle = None
        self.dragged_polygon = None  # Keep track of dragged user polygon
        # UI Elements
        self.button_rects = {'Add Square': pygame.Rect(10, 10, 100, 50),
                             'Add Triangle': pygame.Rect(120, 10, 100, 50)}
        self.slider_rect = pygame.Rect(10, 70, 200, 10)
        self.slider_thumb_rect = pygame.Rect(10, 65, 10, 20)
        self.slider_value = 0.5  # Initial value of the slider, range [0, 1]
        self.mass_value = 1.0  # Initial mass value

    def draw(self, screen):
        screen.fill(WHITE)
        self.soft_body.render(screen)
        for poly in self.user_polygons:
            poly.draw(screen)

        # Draw UI Elements
        for button, rect in self.button_rects.items():
            pygame.draw.rect(screen, (0, 128, 255), rect)
            font = pygame.font.Font(None, 36)
            text_surf = font.render(button, True, (0, 0, 0))
            screen.blit(text_surf, rect.move(10, 10))
        
        # Draw Slider
        pygame.draw.rect(screen, (0, 128, 255), self.slider_rect)
        pygame.draw.rect(screen, (255, 0, 0), self.slider_thumb_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_vec = pygame.Vector2(mouse_x, mouse_y)
            # Check if mouse is near the center of mass
            center_of_mass = self.soft_body.compute_center_of_mass()
            distance_to_com = center_of_mass.distance_to(pygame.Vector2(mouse_x, mouse_y))
            for poly in self.user_polygons:
                if poly.is_point_inside(mouse_vec):
                    self.dragged_polygon = poly
                    break
            # Check if a UI button was clicked
            for button, rect in self.button_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    if button == 'Add Square':
                        self.add_square(mouse_x, mouse_y)
                    elif button == 'Add Triangle':
                        self.add_triangle(mouse_x, mouse_y)
            # Check if the slider thumb was clicked
            if self.slider_thumb_rect.collidepoint(mouse_x, mouse_y):
                self.dragging_slider = True

            if distance_to_com < 20:  # Adjust this threshold as needed
                self.soft_body.dragging = True
                self.soft_body.drag_offset = pygame.Vector2(mouse_x, mouse_y) - center_of_mass
            else:
                # Check if mouse is near any particle
                for particle in self.soft_body.particles:
                    distance_to_particle = particle.position.distance_to(pygame.Vector2(mouse_x, mouse_y))
                    if distance_to_particle < particle.radius:
                        self.dragged_particle = particle
                        break

        elif event.type == pygame.MOUSEBUTTONUP:
            self.soft_body.dragging = False
            self.dragged_particle = None
            self.dragging_slider = False
            self.dragged_polygon = None
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Dragging the slider thumb
            if self.dragging_slider:
                self.slider_value = (mouse_x - self.slider_rect.left) / self.slider_rect.width
                self.slider_value = max(0, min(1, self.slider_value))  # Clamp between 0 and 1
                self.slider_thumb_rect.x = self.slider_rect.x + self.slider_value * self.slider_rect.width - self.slider_thumb_rect.width // 2
                
                # Update particle mass based on slider value
                self.mass_value = self.slider_value * 10  # Assume max mass is 10
                for particle in self.soft_body.particles:
                    particle.mass = self.mass_value
            if self.dragged_polygon:
                # Drag the entire polygon by translating all its vertices
                translation_vector = pygame.Vector2(mouse_x, mouse_y) - self.dragged_polygon.vertices[0]
                for vertex in self.dragged_polygon.vertices:
                    vertex += translation_vector
            if self.soft_body.dragging:
                self.soft_body.handle_mouse_move(mouse_x, mouse_y)
            elif self.dragged_particle:
                self.dragged_particle.position = pygame.Vector2(mouse_x, mouse_y)



    def update(self):
        if self.dragged_particle:
            print("Dragging a particle!")  # Debugging print statement
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragged_particle.position = pygame.Vector2(mouse_x, mouse_y)
        elif self.soft_body.dragging:
            print("Dragging the center of mass!")  # Debugging print statement
        self.soft_body.update(0.016)  # Assuming 60 FPS, so dt is approximately 0.016
        for particle in self.soft_body.particles:
            particle.apply_gravity()
            particle.integrate(0.01667)

    def add_square(self, x, y):
        # Add a square polygon centered at (x, y)
        square = PolygonObject([pygame.Vector2(x-20, y-20),
                                pygame.Vector2(x+20, y-20),
                                pygame.Vector2(x+20, y+20),
                                pygame.Vector2(x-20, y+20)])
        self.user_polygons.append(square)

    def add_triangle(self, x, y):
        # Add a triangle polygon centered at (x, y)
        triangle = PolygonObject([pygame.Vector2(x-20, y+20),
                                  pygame.Vector2(x+20, y+20),
                                  pygame.Vector2(x, y-20)])
        self.user_polygons.append(triangle)
class SpringScene(Scene):
    def __init__(self):
        super().__init__()
        self.spring_chain = SpringChain(SCREEN_WIDTH // 2, 100, 1, 100, 0.05, SCREEN_HEIGHT)
        self.spring_ui = SpringUI(10, 10)
        self.dragged_spring = None
        self.oscillation_data = []
        self.time_elapsed = 0  # Add this line to keep track of time
        self.amplitude = 50  # Amplitude of oscillation
        self.mass = 1  # Mass attached to the spring
        self.min_displacement = float('inf')
        self.max_displacement = float('-inf')
        self.simple_harmonic_mode = False
        self.shm_button = pygame.Rect(10, 200, 100, 40)  # x, y, width, height
        self.velocity = 0.0
        self.graph_width = 200
        self.omega = 0
        self.pulled = False
        self.released = False


    def draw(self, screen):
        screen.fill(WHITE)
        self.spring_chain.draw(screen)
        self.spring_ui.draw(screen)

        pygame.draw.rect(screen, (0, 128, 255), self.shm_button)
        font = pygame.font.SysFont(None, 24)
        button_text = font.render("Toggle SHM", True, (255, 255, 255))
        
        
        # Calculate the position to center the text
        text_rect = button_text.get_rect(center=self.shm_button.center)
        
        screen.blit(button_text, text_rect)

        graph_x, graph_y = SCREEN_WIDTH - self.graph_width, 50
        graph_height = 100

        pygame.draw.rect(screen, (0, 0, 0), (graph_x, graph_y, self.graph_width, graph_height), 1)
        pygame.draw.line(screen, (0, 0, 0), (graph_x, graph_y + graph_height // 2), (graph_x + self.graph_width, graph_y + graph_height // 2))

        if self.min_displacement != self.max_displacement:
            for i in range(1, len(self.oscillation_data)):
                x1, y1 = self.oscillation_data[i-1]
                x2, y2 = self.oscillation_data[i]

                y1_scaled = ((y1 - self.min_displacement) / (self.max_displacement - self.min_displacement)) * graph_height
                y2_scaled = ((y2 - self.min_displacement) / (self.max_displacement - self.min_displacement)) * graph_height

                pygame.draw.line(screen, (255, 0, 0), (graph_x + x1, graph_y + y1_scaled), (graph_x + x2, graph_y + y2_scaled))

    def handle_event(self, event):
        self.spring_ui.handle_event(event, self.spring_chain)
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if self.shm_button.collidepoint(mouse_x, mouse_y):
                self.simple_harmonic_mode = not self.simple_harmonic_mode

            else:
                for spring in self.spring_chain.springs:
                    if math.sqrt((mouse_x - spring.end[0]) ** 2 + (mouse_y - spring.end[1]) ** 2) < 20:
                        spring.dragging = True
                        self.dragged_spring = spring
                        break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragged_spring:
                self.dragged_spring.dragging = False
                self.dragged_spring = None
                self.released = True  # Now the spring is released and will oscillate
                self.pulled = False  # Spring is no longer being pulled


    def update(self):
        self.time_elapsed += 0.016  # Assuming 60 FPS, so dt is approximately 0.016

        last_spring = self.spring_chain.springs[-1]
        k = last_spring.k
        m = self.mass  # mass attached to the spring
        omega = math.sqrt(k / m)

        if self.simple_harmonic_mode:
            if self.released:
                # Calculate displacement from equilibrium
                displacement = last_spring.end[1] - last_spring.anchor[1]

                # Calculate acceleration due to Hooke's Law (a = -omega^2 * x)
                acceleration = -omega * omega * displacement

                # Update velocity
                self.velocity += acceleration * 0.016  # dt is 0.016

                # Update position based on velocity
                last_spring.end[1] += self.velocity * 0.016  # dt is 0.016

            elif self.pulled and not self.released:
                self.released = True  # The spring has been released, SHM starts
                self.velocity = 0  # Reset velocity for a new pull

        else:
            # Reset these flags and values when not in SHM mode
            self.released = False
            self.pulled = False
            self.velocity = 0

            # Normal update logic for the spring chain
            self.spring_chain.update()




        first_spring = self.spring_chain.springs[0]
        current_length = math.dist(first_spring.anchor, first_spring.end)
        displacement = current_length - first_spring.rest_length

        self.min_displacement = min(self.min_displacement, displacement)
        self.max_displacement = max(self.max_displacement, displacement)

        self.oscillation_data.append((self.graph_width, displacement))
        self.oscillation_data = [(x - 1, y) for x, y in self.oscillation_data]
        self.oscillation_data = [(x, y) for x, y in self.oscillation_data if x >= 0]

            







class SceneManager:
    def __init__(self):
        self.current_scene = MainMenuScene()

    def switch_to_scene(self, new_scene):
        self.current_scene = new_scene

    def update(self):
        self.current_scene.update()

    def draw(self, screen):
        self.current_scene.draw(screen)

    def handle_event(self, event):
        self.current_scene.handle_event(event)

# Main loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Physics Engine UI")
scene_manager = SceneManager()
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            # Check if the current scene is SoftBodyScene
            if isinstance(scene_manager.current_scene, SoftBodyScene):
                if scene_manager.current_scene.soft_body.dragging:
                    scene_manager.current_scene.soft_body.handle_mouse_move(mouse_x, mouse_y)
                elif scene_manager.current_scene.soft_body.dragged_particle:
                    scene_manager.current_scene.soft_body.dragged_particle.position = pygame.Vector2(mouse_x, mouse_y)
            # Check if the current scene is SpringScene
            elif isinstance(scene_manager.current_scene, SpringScene):
                    scene_manager.current_scene.handle_event(event)
                    scene_manager.current_scene.update()

        else:
            scene_manager.handle_event(event)


    scene_manager.update()
    scene_manager.draw(screen)
    pygame.display.flip()
    clock.tick(75)  # This will cap the loop to run at 60 FPS


pygame.quit()

'''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if the mouse is near the end of any spring in the chain
            for spring in spring_chain.springs:
                if math.sqrt((mouse_x - spring.end[0])**2 + (mouse_y - spring.end[1])**2) < 20:
                    spring.dragging = True
                    break  # Break out of the loop once a spring is being dragged
        elif event.type == pygame.MOUSEBUTTONUP:
            # Set dragging to False for all springs in the chain
            for spring in spring_chain.springs:
                spring.dragging = False

    screen.fill((255, 255, 255))  # Fill the screen with white

    

    # In the main loop:
    spring_chain.update()
    spring_chain.draw(screen)



    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
'''


import pygame
from SpringChain import SpringChain
from Spring import Spring
from SoftBody import SoftBody
import math
from SpringUI import SpringUI


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
                    if self.options[index] == "Spring":
                        scene_manager.switch_to_scene(SpringScene())
                    elif self.options[index] == "SoftBody":
                        scene_manager.switch_to_scene(SoftBodyScene())
                    if self.options[index] == "Spring":
                        scene_manager.switch_to_scene(SpringScene())
                    # Add other scenes as needed

class SoftBodyScene(Scene):
    def __init__(self):
        super().__init__()
        # Create a soft body at the center of the screen
        self.soft_body = SoftBody(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200, 1.0, 0.05, 5, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.dragged_particle = None
    def draw(self, screen):
        screen.fill(WHITE)
        self.soft_body.render(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            
            # Check if mouse is near the center of mass
            center_of_mass = self.soft_body.compute_center_of_mass()
            distance_to_com = center_of_mass.distance_to(pygame.Vector2(mouse_x, mouse_y))
            
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

        elif event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()
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

class SpringScene(Scene):
    def __init__(self):
        super().__init__()
        self.spring_chain = SpringChain(SCREEN_WIDTH // 2, 100, 1, 100, 0.05, SCREEN_HEIGHT)
        self.spring_ui = SpringUI(10, 10)  # Position the UI at (10, 10)
        self.dragged_spring = None  # Add this line to keep track of the dragged spring
        self.oscillation_data = []
        self.time_elapsed = 0

        

    def draw(self, screen):
        screen.fill(WHITE)
        self.spring_chain.draw(screen)
        self.spring_ui.draw(screen)  # Draw the UI
        # Draw the oscillation graph
        graph_x, graph_y = SCREEN_WIDTH - 200, 50  # Top-right corner
        pygame.draw.rect(screen, (0, 0, 0), (graph_x, graph_y, 200, 100), 1)  # Graph boundary
        pygame.draw.line(screen, (0, 0, 0), (graph_x, graph_y + 50), (graph_x + 200, graph_y + 50))  # X-axis
        pygame.draw.line(screen, (0, 0, 0), (graph_x, graph_y), (graph_x, graph_y + 100))  # Y-axis
        
        # Draw tick marks (example: every 50 units on X-axis and every 20 units on Y-axis)
        for i in range(5):
            pygame.draw.line(screen, (0, 0, 0), (graph_x + i * 50, graph_y + 48), (graph_x + i * 50, graph_y + 52))
        for i in range(6):
            pygame.draw.line(screen, (0, 0, 0), (graph_x - 2, graph_y + i * 20), (graph_x + 2, graph_y + i * 20))
        
        # Plot the data line
        for i in range(1, len(self.oscillation_data)):
            x1, y1 = self.oscillation_data[i-1]
            x2, y2 = self.oscillation_data[i]
            pygame.draw.line(screen, (255, 0, 0), (graph_x + x1, graph_y + 50 - y1), (graph_x + x2, graph_y + 50 - y2))

    def handle_event(self, event):
        self.spring_ui.handle_event(event, self.spring_chain)  # Handle UI events
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for spring in self.spring_chain.springs:
                if math.sqrt((mouse_x - spring.end[0])**2 + (mouse_y - spring.end[1])**2) < 20:
                    spring.dragging = True
                    self.dragged_spring = spring
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragged_spring:
                self.dragged_spring.dragging = False
                self.dragged_spring = None

    def update(self):
        if self.dragged_spring and self.dragged_spring.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragged_spring.end[0] = mouse_x
            self.dragged_spring.end[1] = mouse_y
        self.spring_chain.update()

        # Oscillation Graph
        self.time_elapsed += 0.016  # Assuming 60 FPS
        # Update the oscillation data

        first_spring = self.spring_chain.springs[0]
        current_length = math.dist(first_spring.anchor, first_spring.end)
        displacement = current_length - first_spring.rest_length  # Displacement from rest length
        
        self.oscillation_data.append((self.time_elapsed, displacement))
        
        # Remove old data to keep the graph within bounds (optional)
        if len(self.oscillation_data) > 200:
            self.oscillation_data.pop(0)







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


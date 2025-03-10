import pygame
import math
from .Scene import Scene
from engine.SoftBody import SoftBody
from engine.PolygonObject import PolygonObject


# Screen size stuff
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Basic colors we need
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class SoftBodyScene(Scene):
    def __init__(self):
        super().__init__()
        # Throw a soft body in the middle of the screen
        self.user_polygons = []  # Keeping track of shapes the user makes
        self.soft_body = SoftBody(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 100, 200, 200, 1.0, 0.05, 5, self.user_polygons, SCREEN_WIDTH, SCREEN_HEIGHT)
        self.dragged_particle = None
        self.dragged_polygon = None  # For when user grabs a polygon
        self.right_arrow_rect = pygame.Rect(740, 540, 40, 20)
        self.left_arrow_rect = pygame.Rect(690, 540, 40, 20)
        # Buttons and stuff
        self.button_rects = {'Add Square': pygame.Rect(10, 10, 100, 50),
                             'Add Triangle': pygame.Rect(120, 10, 100, 50)}
        self.slider_rect = pygame.Rect(10, 70, 200, 10)
        self.slider_thumb_rect = pygame.Rect(10, 65, 10, 20)
        self.slider_value = 0.5  # Starts halfway
        self.mass_value = 1.0  # Default weight

    def draw(self, screen):
        screen.fill((255, 255, 255))
        self.soft_body.render(screen)

        # Right arrow for next scene
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.right_arrow_rect.x, self.right_arrow_rect.y),
            (self.right_arrow_rect.x + self.right_arrow_rect.width, self.right_arrow_rect.y + self.right_arrow_rect.height // 2),
            (self.right_arrow_rect.x, self.right_arrow_rect.y + self.right_arrow_rect.height)
        ])
        
        # Left arrow for prev scene
        pygame.draw.polygon(screen, (0, 0, 0), [
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y),
            (self.left_arrow_rect.x, self.left_arrow_rect.y + self.left_arrow_rect.height // 2),
            (self.left_arrow_rect.x + self.left_arrow_rect.width, self.left_arrow_rect.y + self.left_arrow_rect.height)
        ])
        
        for poly in self.user_polygons:
            poly.draw(screen)
        
        font = pygame.font.Font(None, 24)  # Changed font size to 24
        for button, rect in self.button_rects.items():
            pygame.draw.rect(screen, (0, 128, 255), rect)
            text_surf = font.render(button, True, (0, 0, 0))
            
            # Center the text nice and pretty
            text_x = rect.x + (rect.width - text_surf.get_width()) // 2
            text_y = rect.y + (rect.height - text_surf.get_height()) // 2
            screen.blit(text_surf, (text_x, text_y))

    def handle_event(self, event, scene_manager):

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_vec = pygame.Vector2(mouse_x, mouse_y)
            # See if user clicked the center bit
            center_of_mass = self.soft_body.compute_center_of_mass()
            distance_to_com = center_of_mass.distance_to(pygame.Vector2(mouse_x, mouse_y))
            if self.right_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .SpringScene import SpringScene  # Import here instead of at the top of the file
                scene_manager.switch_to_scene(SpringScene())
            elif self.left_arrow_rect.collidepoint(mouse_x, mouse_y):
                from .FluidScene import FluidScene  # Import here instead of at the top of the file
                scene_manager.switch_to_scene(FluidScene())
            for poly in self.user_polygons:
                if poly.is_point_inside(mouse_vec):
                    self.dragged_polygon = poly
                    break
            # Check if a UI button was clicked
            for button, rect in self.button_rects.items():
                if rect.collidepoint(mouse_x, mouse_y):
                    center_x = SCREEN_WIDTH // 2
                    center_y = SCREEN_HEIGHT // 2

                    if button == 'Add Square':
                        self.add_square(center_x, center_y)
                    elif button == 'Add Triangle':
                        self.add_triangle(center_x, center_y)


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
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragged_particle.position = pygame.Vector2(mouse_x, mouse_y)
        elif self.soft_body.dragging:
            pass
        self.soft_body.update(0.016)  # Assuming 60 FPS, so dt is approximately 0.016
        for particle in self.soft_body.particles:
            particle.apply_gravity()
            particle.integrate(0.01667)
        for poly in self.user_polygons:
            for particle in self.soft_body.particles:
                if poly.is_point_inside(particle.position):
                    # Apply a simple repulsion force by reversing the velocity
                    particle.velocity *= -1 
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
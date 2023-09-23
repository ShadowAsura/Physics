import pygame
from engine.Pendulum import Pendulum
import math

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

class PendulumScene:
    def __init__(self):
        self.pendulums = []  # List to store all pendulum objects
        self.dragging_pendulum = None 
        self.original_position = None
        self.screen = None
        self.initialize_pendulums()

    
    def initialize_pendulums(self):
        x, y = SCREEN_WIDTH // 2, 50
        pivot_point = (x, y)
        pendulum1 = Pendulum(200, 20, math.pi / 4, origin = pivot_point)
        self.pendulums.append(pendulum1)
        x += pendulum1.length * math.sin(pendulum1.angle)
        y += pendulum1.length * math.cos(pendulum1.angle)
        
        pivot_point = (x, y)
        pendulum2 = Pendulum(160, 20, math.pi / 6, origin = pivot_point, parent=pendulum1)
        self.pendulums.append(pendulum2)
        x += pendulum2.length * math.sin(pendulum2.angle)
        y += pendulum2.length * math.cos(pendulum2.angle)

        pivot_point = (x, y)
        pendulum3 = Pendulum(120, 20, math.pi / 8, origin = pivot_point, parent=pendulum2)
        self.pendulums.append(pendulum3)
    
    def handle_event(self, event, scene_manager):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for pendulum in self.pendulums:
                if pendulum.is_mouse_over(event.pos):
                    self.dragging_pendulum = pendulum
                    self.original_position = pendulum.get_position()  # store the position at the moment of mouse down
                    break
        
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging_pendulum:
                mouse_position = pygame.math.Vector2(event.pos)
                displacement = mouse_position - self.original_position
                # You may want to set a new angle based on the mouse_position here.
                # For example:
                delta_x, delta_y = displacement.x, displacement.y
                new_angle = math.atan2(delta_x, delta_y)
                self.dragging_pendulum.angle = new_angle
        
        elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging_pendulum:
                    displacement = pygame.math.Vector2(event.pos) - self.original_position
                    self.dragging_pendulum.apply_force(displacement)
                    self.dragging_pendulum = None  # Reset after mouse release

    def update(self):
        if not self.dragging_pendulum:
            dt = 1/60.0
            for pendulum in self.pendulums:
                pendulum.update(dt)
            
            # Update the origins and positions list for each pendulum
            x, y = SCREEN_WIDTH // 2, 50
            for pendulum in self.pendulums:
                pendulum.origin = (x, y)  # Update the origin to be the pivot point of each pendulum
                x += pendulum.length * math.sin(pendulum.angle)
                y += pendulum.length * math.cos(pendulum.angle)
                pendulum.positions.append((int(x), int(y)))
                
                # Optional: Limit the number of positions stored to prevent the list from becoming too long
                if len(pendulum.positions) > 50:  # Adjust as needed
                    pendulum.positions.pop(0)
                pendulum.trace_points.append((x, y))
        if self.dragging_pendulum:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, (255,0,0), self.original_position, mouse_pos, 2)


    def draw(self, screen):
        self.screen = screen
        screen.fill((255, 255, 255))
        x, y = screen.get_width() // 2, 50
        for pendulum in self.pendulums:
            pendulum.draw(screen, x, y)
            x += pendulum.length * math.sin(pendulum.angle)
            y += pendulum.length * math.cos(pendulum.angle)
            



import pygame
import math
from .Scene import Scene

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


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
import pygame
from SpringChain import SpringChain
from Spring import Spring
import math

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
        self.options = ["Pendulum", "Spring", "Fluid"]
        self.buttons = [self.font.render(option, True, BLACK) for option in self.options]

    def draw(self, screen):
        screen.fill(WHITE)
        for index, button in enumerate(self.buttons):
            screen.blit(button, (SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for index, button in enumerate(self.buttons):
                button_rect = button.get_rect(topleft=(SCREEN_WIDTH // 2 - button.get_width() // 2, 150 + index * 60))
                if button_rect.collidepoint(mouse_x, mouse_y):
                    # Switch to the corresponding scene
                    if self.options[index] == "Spring":
                        scene_manager.switch_to_scene(SpringScene())
                    # Add other scenes as needed

class SpringScene(Scene):
    def __init__(self):
        super().__init__()
        self.spring_chain = SpringChain(SCREEN_WIDTH // 2, 100, 3, 100, 0.05, SCREEN_HEIGHT)


    def draw(self, screen):
        screen.fill(WHITE)
        self.spring_chain.draw(screen)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            for spring in self.spring_chain.springs:
                if math.sqrt((mouse_x - spring.end[0])**2 + (mouse_y - spring.end[1])**2) < 20:
                    self.spring_chain.dragging = True
                    self.dragged_spring = spring  # Store the spring being dragged
                    break
        elif event.type == pygame.MOUSEBUTTONUP:
            self.spring_chain.dragging = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.spring_chain.add_spring()

    def update(self):
        if self.spring_chain.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.dragged_spring.end = [mouse_x, mouse_y]  # Update the position of the dragged spring
        self.spring_chain.update()


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

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        scene_manager.handle_event(event)

    scene_manager.update()
    scene_manager.draw(screen)
    pygame.display.flip()
    pygame.time.wait(10)

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


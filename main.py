import pygame

from engine import SpringChain
from engine import Spring

from engine import SoftBody
import math


from ui import SpringUI

from engine import PolygonObject
from engine import FluidParticle

from scenes.SceneManager import SceneManager
from scenes.MenuScene import MainMenuScene
from scenes.SoftBodyScene import SoftBodyScene
from scenes.SpringScene import SpringScene
from scenes.FluidScene import FluidScene

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Main loop
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Physics Engine")
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
                events = pygame.event.get()
                for event in events:
                    if event.type == pygame.QUIT:
                        running = False
                for poly in scene_manager.current_scene.user_polygons:  # replace 'user_polygons' with your actual list of PolygonObject instances
                    poly.handle_interaction(events)
                if scene_manager.current_scene.soft_body.dragging:
                    scene_manager.current_scene.soft_body.handle_mouse_move(mouse_x, mouse_y)
                elif scene_manager.current_scene.soft_body.dragged_particle:
                    scene_manager.current_scene.soft_body.dragged_particle.position = pygame.Vector2(mouse_x, mouse_y)
            # Check if the current scene is SpringScene
            elif isinstance(scene_manager.current_scene, SpringScene):
                    scene_manager.current_scene.handle_event(event)
                    scene_manager.current_scene.update()

        else:
            scene_manager.handle_event(event, scene_manager)


    scene_manager.update()
    scene_manager.draw(screen)
    pygame.display.flip()
    clock.tick(75)  # This will cap the loop to run at 60 FPS


pygame.quit()


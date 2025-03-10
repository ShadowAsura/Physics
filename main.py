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
from scenes.PendulumScene import PendulumScene

# Fire up pygame
pygame.init()

# Screen size stuff
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Basic colors we need
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Let's get this party started
screen = pygame.display.set_mode((800, 600), pygame.SRCALPHA)
pygame.display.set_caption("Physics Engine")
pygame.display.set_icon(pygame.image.load("physics.png"))
scene_manager = SceneManager()
clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()  # Grab all the stuff that happened
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        else:
            scene_manager.handle_event(event, scene_manager)




    scene_manager.update()
    scene_manager.draw(screen)
    pygame.display.flip()
    clock.tick(75)  # Keep things smooth at 60fps


pygame.quit()
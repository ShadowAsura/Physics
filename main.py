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
from engine.config import config

# Fire up pygame
pygame.init()

# Basic colors we need
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Let's get this party started
screen = pygame.display.set_mode((config.width, config.height), pygame.SRCALPHA)
pygame.display.set_caption("Physics Engine")
pygame.display.set_icon(pygame.image.load("physics.png"))
scene_manager = SceneManager()
clock = pygame.time.Clock()
running = True
while running:
    dt = clock.tick(60) / 1000.0
    events = pygame.event.get()  # Grab all the stuff that happened
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        else:
            scene_manager.handle_event(event, scene_manager)

    scene_manager.update(dt)
    scene_manager.draw(screen)
    pygame.display.flip()


pygame.quit()
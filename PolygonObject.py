import random
import pygame

class PolygonObject:
    def __init__(self, vertices):
        self.vertices = vertices  # A list of pygame.Vector2 objects that define the polygon's vertices
        self.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # Random color


    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [(int(v.x), int(v.y)) for v in self.vertices])
        pygame.draw.polygon(screen, (0, 0, 0), [(int(v.x), int(v.y)) for v in self.vertices], 1)  # Black border

    def is_point_inside(self, point):
        # Ray casting algorithm to check point inside polygon
        x, y = point
        odd_nodes = False
        j = len(self.vertices) - 1
        for i in range(len(self.vertices)):
            xi, yi = self.vertices[i]
            xj, yj = self.vertices[j]
            if yi < y and yj >= y or yj < y and yi >= y:
                if xi + (y - yi) / (yj - yi) * (xj - xi) < x:
                    odd_nodes = not odd_nodes
            j = i
        return odd_nodes

    def handle_interaction(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.Vector2(event.pos)
                if self.is_point_inside(mouse_pos):
                    self.move(5, 5)  # Move the polygon by (5, 5) for demonstration.
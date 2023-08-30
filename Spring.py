import math
import pygame
import pygame.gfxdraw

class Spring:
    def __init__(self, anchor_x, anchor_y, length, k, screen_height, num_coils=12):
        self.anchor = [anchor_x, anchor_y]
        self.screen_height = screen_height
        self.rest_length = length
        self.k = k
        self.end = [anchor_x, anchor_y + length]
        self.velocity = [0, 0]
        self.num_coils = num_coils
        self.dragging = False
        self.GRAVITY = 0.5

    def update(self):
        if self.dragging:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.end[0] = mouse_x
            self.end[1] = mouse_y
            self.velocity = [0, 0]
        else:
            displacement = self.rest_length - math.dist(self.anchor, self.end)
            force = self.k * displacement
            angle = math.atan2(self.end[1] - self.anchor[1], self.end[0] - self.anchor[0])
            self.velocity[0] += force * math.cos(angle)
            self.velocity[1] += force * math.sin(angle) + self.GRAVITY
            self.velocity[0] *= 0.9
            self.velocity[1] *= 0.9
            self.end[0] += self.velocity[0]
            self.end[1] += self.velocity[1]

            # Ensure the ball doesn't pass through the anchor point
            min_distance = 10
            if math.dist(self.anchor, self.end) < min_distance:
                self.end = [self.anchor[0] + min_distance * math.cos(angle), self.anchor[1] + min_distance * math.sin(angle)]

    def draw(self, screen):
        angle = math.atan2(self.end[1] - self.anchor[1], self.end[0] - self.anchor[0])
        current_length = math.dist(self.anchor, self.end)
        coil_length = current_length / self.num_coils

        for i in range(self.num_coils):
            start_x = self.anchor[0] + i * (self.end[0] - self.anchor[0]) / self.num_coils 
            start_y = self.anchor[1] + i * (self.end[1] - self.anchor[1]) / self.num_coils
            end_x = self.anchor[0] + (i + 1) * (self.end[0] - self.anchor[0]) / self.num_coils
            end_y = self.anchor[1] + (i + 1) * (self.end[1] - self.anchor[1]) / self.num_coils

            mid_x = (start_x + end_x) / 2
            mid_y = (start_y + end_y) / 2

            pygame.draw.arc(screen, (0, 0, 0), (mid_x - 10, mid_y - coil_length / 2, 20, coil_length), angle, angle + math.pi, 2)
            pygame.draw.arc(screen, (0, 0, 0), (mid_x - 10, mid_y, 20, coil_length), angle + math.pi, angle + 2*math.pi, 2)
        
        # Draw the mass at the end
        pygame.draw.circle(screen, (0, 0, 255), (int(self.end[0]), int(self.end[1])), 10)

import math
import pygame
from collections import deque

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


class Pendulum:
    def __init__(self, length, mass, angle, origin, parent=None):
        self.length = length  # Length of the pendulum arm
        self.angle = angle  # Angle from the vertical, in radians
        self.mass = mass
        self.origin = origin
        self.angular_velocity = 0.0
        self.angular_acceleration = 0.0
        self.gravity = 9.81  # Gravity constant
        self.time_scale = 4.0 
        self.parent = parent  # Parent pendulum, if any
        self.positions = []
        self.trace_points = deque(maxlen=200)
        self.color = (22, 77, 105)
        self.bob_radius = 10

    def update(self, dt):
        dt = dt * self.time_scale
        # Define the system of ODEs
        def f(t, y):
            angle, angular_velocity = y
            dydt = [angular_velocity, -self.gravity / self.length * math.sin(angle)]
            return dydt

        # 4th Order Runge-Kutta Method
        y = [self.angle, self.angular_velocity]
        k1 = [dt * yi for yi in f(0, y)]
        k2 = [dt * yi for yi in f(0, [yj + 0.5 * k1j for yj, k1j in zip(y, k1)])]
        k3 = [dt * yi for yi in f(0, [yj + 0.5 * k2j for yj, k2j in zip(y, k2)])]
        k4 = [dt * yi for yi in f(0, [yj + k3j for yj, k3j in zip(y, k3)])]

        # Update angle and angular velocity
        self.angle += (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0]) / 6
        self.angular_velocity += (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1]) / 6


    def draw(self, screen, x, y):

        end_x = x + self.length * math.sin(self.angle)
        end_y = y + self.length * math.cos(self.angle)
        
        pygame.draw.aaline(screen, (0, 0, 0), (x, y), (end_x, end_y), 2)
        pygame.draw.circle(screen, (0, 0, 255), (int(end_x), int(end_y)), 10)

        for i, (x, y) in enumerate(self.trace_points):
            alpha = int((i / len(self.trace_points)) * 255)  # Fade out older points
            color = (*self.color, alpha)  # Assuming self.pendulum.color is an RGB tuple
            pygame.draw.circle(screen, color, (int(x), int(y)), 2)

    def is_mouse_over(self, mouse_pos):
        if len(self.positions) == 0:
            return False
        
        current_position = self.positions[-1]
        x1, y1 = current_position  # Unpack current_position tuple into x1 and y1
        x2, y2 = mouse_pos  # Unpack mouse_pos tuple into x2 and y2
        
        distance_to_mouse = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        return distance_to_mouse < self.bob_radius

    def get_position(self):
        # Assuming self.arm_length is the length of the pendulum's arm
        # and self.angle is the current angle of the pendulum.
        x = self.length * math.sin(self.angle) + self.origin[0] # assuming self.origin is the pivot point
        y = self.length * math.cos(self.angle) + self.origin[1]
        return pygame.math.Vector2(x, y)

    def apply_force(self, force):
        # Convert the linear force to a change in angular velocity or however it should affect your pendulum.
        # The exact physics might be more complex, depending on the precision and realism you are aiming for.
        # Assuming the force is a vector applied at the bob position, you can calculate the torque as follows:
        
        r = pygame.math.Vector2(self.get_position() - self.origin)  # radius vector from pivot to bob
        torque = r.cross(force)  # cross product gives the torque
        
        # Assuming you have some way of managing angular velocity, perhaps as self.angular_velocity
        # And assuming you have the moment of inertia I, for a point mass at the end of a rod, it’s m * L^2.
        # Where m is the mass of the bob and L is the length of the rod.
        
        I = self.mass * (self.length ** 2)  # moment of inertia
        angular_acceleration = torque / I  # α = τ/I
        self.angular_velocity += angular_acceleration  # Update angular velocity based on angular acceleration

        # Calculate the new position after applying the force
        new_x = self.origin[0] + self.length * math.sin(self.angle)
        new_y = self.origin[1] + self.length * math.cos(self.angle)
        self.positions.append((int(new_x), int(new_y)))

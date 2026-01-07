from constants import ASTEROID_MIN_RADIUS, ASTEROID_TURN_SPEED, LINE_WIDTH
import pygame
from circleshape import CircleShape
from logger import log_event
import random
import math

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.rotation = 0
        self.rect = pygame.Rect(x - radius, y - radius, radius * 4, radius * 2)
        
        # Generate irregular asteroid shape
        self.shape_points = []
        num_sides = random.randint(8, 12)
        for i in range(num_sides):
            angle = (i / num_sides) * 2 * math.pi
            variation = random.uniform(0.7, 1.3)
            r = self.radius * variation
            x_point = r * math.cos(angle)
            y_point = r * math.sin(angle)
            self.shape_points.append(pygame.Vector2(x_point, y_point))

    def draw(self, screen):
        # Rotate and translate shape points
        angle_rad = math.radians(self.rotation)
        rotated_corners = []
        for point in self.shape_points:
            # Rotate around origin
            rotated_x = point.x * math.cos(angle_rad) - point.y * math.sin(angle_rad)
            rotated_y = point.x * math.sin(angle_rad) + point.y * math.cos(angle_rad)
            # Translate to position
            rotated_corners.append((self.position.x + rotated_x, self.position.y + rotated_y))
        
        pygame.draw.polygon(screen, "white", rotated_corners, LINE_WIDTH)



    def update(self, dt):
        self.position = self.position + self.velocity * dt
        self.rotation = self.rotation + ASTEROID_TURN_SPEED * dt

    def split(self):
        self.kill()

        if self.radius <= ASTEROID_MIN_RADIUS:
            points = 25
            return (None, points)

        log_event("asteroid_split")

        random_angle = random.uniform(20, 50)
        rotated_velocity1 = self.velocity.rotate(random_angle)
        rotated_velocity2 = self.velocity.rotate(-random_angle)

        new_radius = self.radius - ASTEROID_MIN_RADIUS

        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)

        asteroid1.velocity = rotated_velocity1 * 1.2
        asteroid2.velocity = rotated_velocity2 * 1.2

        if self.radius == 60:
            points = 100
        elif self.radius == 40:
            points = 50
        else:
            points = 0

        return ((asteroid1, asteroid2), points)
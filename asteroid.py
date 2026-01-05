from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
import pygame
from circleshape import CircleShape
from logger import log_event
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position = self.position + self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return (asteroid1, asteroid2)
        
        else:
            log_event("asteroid_split")
            random_angle = random.uniform(20, 50)
            negative_random_angle = -random_angle
            rotated_velocity1 = self.velocity.rotate(random_angle)
            rotated_velocity2 = self.velocity.rotate(negative_random_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid1.velocity = rotated_velocity1 * 1.2
            asteroid2.velocity = rotated_velocity2 * 1.2
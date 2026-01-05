from asteroid import Asteroid
import player
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state
from player import Player
from asteroidfield import AsteroidField
from logger import log_event
import sys
from shot import Shot

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()
    print("Starting Asteroids with pygame version: 2.6.1")
    print("Screen width: 1280")
    print("Screen height: 720")
    
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    AsteroidField.containers = (updatable,)
    asteroid_field = AsteroidField(asteroids)
    Asteroid.containers = (updatable, drawable, asteroids)

    Shot.containers = (updatable, drawable, shots)

    Player.containers = (updatable, drawable)

    player = Player(x=SCREEN_WIDTH / 2, y=SCREEN_HEIGHT / 2)

    dt = 0

    while True:
        log_state()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            
        updatable.update(dt)
        for asteroid in asteroids:
            if player.collides_with(asteroid):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot):
                    log_event("asteroid_shot")
                    shot.kill()

                    new_asteroids = asteroid.split()
                    if new_asteroids:
                        asteroid1, asteroid2 = new_asteroids
                        asteroids.add(asteroid1)
                        asteroids.add(asteroid2)
    
        screen.fill("black")
        for sprite in drawable:
            sprite.draw(screen)
        pygame.display.flip()

        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()

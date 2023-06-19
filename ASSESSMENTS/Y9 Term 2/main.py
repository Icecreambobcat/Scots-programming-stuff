import pygame
import physics
from physics import collisions

pygame.init()
display_width = 800
display_height = 600

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Rex's platformer game")
clock = pygame.time.Clock()

crashed = False

while not crashed:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            crashed = True

        print(event)
    
    pygame.display.update()
    clock.tick(60)
    
pygame.quit()
quit()
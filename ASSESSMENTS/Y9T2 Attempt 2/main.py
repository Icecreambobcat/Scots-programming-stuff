# Init
import pygame
from pygame.locals import *
pygame.init()
import mapdata

# Disp def
screen_width = 800
screen_height = 800

# Def game meta
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rex\'s Platformer game')
tile_size = 80

# Img load
bg_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/BG.jpg')
moon_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/moon.png')

# Init world class
class World():
    def __init__(self, data) -> None:
        self.tile_list = []
        # Tile images
        ground = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stone.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(ground, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# Instancing
world = World(mapdata.world_data)

# Game loop
run = True
while run: 
    screen.blit(bg_img, (0, 0))
    screen.blit(moon_img, (100, 100))
    
    world.draw()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
# Quit
pygame.quit()
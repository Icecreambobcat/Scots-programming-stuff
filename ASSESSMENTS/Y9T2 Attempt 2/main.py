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
tile_size = 50

# Img load
bg_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/BG.jpg')
moon_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/moon.png')

# Init player class
class Player():
    def __init__(self, x, y) -> None:
        img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/spriteforward.png')
        self.image = pygame.transform.scale(img, (40, 80))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False
        
    def update(self):
        dx = 0
        dy = 0
        
        key = pygame.key.get_pressed()
        # Up
        # Up
        if (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]) and self.jumping == False:
            self.vel_y = -12
            self.jumping = True
        if not key[pygame.K_SPACE] and not key[pygame.K_UP] and not key[pygame.K_w]:
            self.jumping = False
        # Left
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 5
        # Right
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 5
            
        self.vel_y += 0.3
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y
        
        # Check collision - YET TO BE IMPLEMENTED
        
        self.rect.x += dx
        self.rect.y += dy
        
        # Temp check DELETE LATER
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0
        
        screen.blit(self.image, self.rect)


# Init world class
class World():
    def __init__(self, data) -> None:
        self.tile_list = []
        wall = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneCenter.png')
        grass = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneMid.png')
        
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(wall, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass, (tile_size, tile_size))
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
player = Player(100, screen_height - 130)

# Game loop
run = True
while run: 
    screen.blit(bg_img, (0, 0))
    screen.blit(moon_img, (100, 100))
    
    world.draw()
    player.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
# Quit
pygame.quit()
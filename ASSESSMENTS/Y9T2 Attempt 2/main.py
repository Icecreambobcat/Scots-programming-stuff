# Init
import pygame
from pygame.locals import *
import mapdata

pygame.init()
clock = pygame.time.Clock()
fps = 60

# Disp def
screen_width = 800
screen_height = 800

# Def game meta
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Rex\'s Platformer game')
tile_size = 40

# Img load
bg_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/BG.jpg')
moon_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/moon.png')

# Init player class
class Player():
    def __init__(self, x, y) -> None:
        self.images_left = []
        self.images_fwd = []
        self.images_right = []
        self.images_back = []
        self.index = 0
        self.counter = 0
        
        # Left
        for num in range(4, 8):
            img_left = pygame.image.load(f'ASSESSMENTS/Y9T2 Attempt 2/Assets/sprite/{num}.png')
            img_left = pygame.transform.scale(img_left, (30, 70))
            self.images_left.append(img_left)
        
        # Fwd
        for num in range(0, 4):
            img_fwd = pygame.image.load(f'ASSESSMENTS/Y9T2 Attempt 2/Assets/sprite/{num}.png')
            img_fwd = pygame.transform.scale(img_fwd, (30, 70))
            self.images_fwd.append(img_fwd)
        
        # Right
        for num in range(8, 12):
            img_right = pygame.image.load(f'ASSESSMENTS/Y9T2 Attempt 2/Assets/sprite/{num}.png')
            img_right = pygame.transform.scale(img_right, (30, 70))
            self.images_right.append(img_right)
       
        # Back
        for num in range(12, 16):
            img_back = pygame.image.load(f'ASSESSMENTS/Y9T2 Attempt 2/Assets/sprite/{num}.png')
            img_back = pygame.transform.scale(img_back, (30, 70))
            self.images_back.append(img_back)
        
        self.image = self.images_left[self.index]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.jumping = False
        self.direction = 0
        
    def update(self): 
        dx = 0
        dy = 0
        walk_cooldown = 7
        
        key = pygame.key.get_pressed()
        
        # Up
        if (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]) and self.jumping == False:
            self.vel_y = -9
            self.jumping = True
        
        # Left
        if key[pygame.K_LEFT] or key[pygame.K_a]:
            dx -= 4
            self.counter += 1
            self.direction = -1
        
        # Right
        if key[pygame.K_RIGHT] or key[pygame.K_d]:
            dx += 3.5
            self.counter += 1
            self.direction = 1
        
        # Reset func    
        if not (key[pygame.K_LEFT] or key[pygame.K_a]) and not (key[pygame.K_RIGHT] or key[pygame.K_d]):
            self.counter = 0
            self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
            
        # Gravity
        self.vel_y += 0.3
        if self.vel_y > 10:
            self.vel_y = 10
        dy += self.vel_y 
        
        # Animations
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_left):
                self.index = 0
            if self.direction == 1:
                self.image = self.images_right[self.index]
            if self.direction == -1:
                self.image = self.images_left[self.index]
        
        # Check collision
        for tile in world.tile_list:
            # Horizontal
            if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            
            # Vert
            if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                
                if self.vel_y < 0:
                    dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                
                elif self.vel_y >= 0:
                    dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.jumping = False
                    
        self.rect.x += dx
        self.rect.y += dy
        
        screen.blit(self.image, self.rect)


# Init world class
class World():
    def __init__(self, data) -> None:
        self.tile_list = []
        wall = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneCenter.png')
        grass = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneMid.png')
        grass_single = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stone.png')
        grass_left = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneLeft.png')
        grass_right = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/stoneRight.png')
        
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
                    
                if tile == 3:
                    img = pygame.transform.scale(grass_single, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 4:
                    img = pygame.transform.scale(grass_left, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                
                if tile == 5:
                    img = pygame.transform.scale(grass_right, (tile_size, tile_size))
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
    
    clock.tick(fps)
    
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
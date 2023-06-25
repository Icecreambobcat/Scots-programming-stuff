# Init
import pygame
# Yes i know wildcard imports are bad but I don't have a fix right now, so if its broken poke me and I'll try fix
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
game_over = 0
main_menu = True

# Img load
bg_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/BG.jpg')
moon_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/moon.png')
restart_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/retrybtn.png')
start_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/startbtn.png')
exit_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/exitbtn.png')

# Button class
class Button():
    def __init__(self,x , y, image) -> None:
        self.image = pygame.transform.scale(image, (200, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False
        
    def draw (self):
        action = False
        
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True
                
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, self.rect)
        
        return action

# Init player class
class Player():
    def __init__(self, x, y) -> None:
        self.reset(x, y)
        
    def update(self, game_over): 
        dx = 0
        dy = 0
        walk_cooldown = 7
        
        if game_over == 0:
            key = pygame.key.get_pressed()
            
            # Up
            if (key[pygame.K_SPACE] or key[pygame.K_UP] or key[pygame.K_w]) and self.airborne == False:
                self.vel_y = -10
            
            # Left
            if key[pygame.K_LEFT] or key[pygame.K_a]:
                dx -= 3.5
                self.counter += 1
                self.direction = -1
            
            # Right
            if key[pygame.K_RIGHT] or key[pygame.K_d]:
                dx += 3.0
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
            self.vel_y += 0.4
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
            self.airborne = True
            
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
                        self.airborne = False
                        
            # Collision with kill obj
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = 1
            
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = 1
                        
            self.rect.x += dx
            self.rect.y += dy
            
        elif game_over == 1:
            self.image = self.dead_image
            self.rect.x - 10
            if self.rect.y > 200:
                self.rect.y -= 2
            
        screen.blit(self.image, self.rect)
        return game_over 
    
    def reset (self, x, y):
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
        
        dead_image = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/ghost.png') 
        self.dead_image = pygame.transform.scale(dead_image, (50, 70))
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect.x = x
        self.rect.y = y
        self.vel_y = 0
        self.direction = 0
        self.airborne = True


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
                    
                if tile == 6:
                    blob = Enemy(col_count * tile_size, row_count * tile_size)
                    blob_group.add(blob)
                    
                if tile == 7:
                    lava = Lava(col_count * tile_size, row_count * tile_size)
                    lava_group.add(lava)
                    
                col_count += 1
            row_count += 1
            
    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        enemy_image = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Enemies/blockerMad.png')
        self.image = pygame.transform.scale(enemy_image, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0
        
    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if self.move_counter > 25:
            self.move_direction *= -1
            self.move_counter *= -1
            
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y) -> None:
        pygame.sprite.Sprite.__init__(self)
        lava_img = pygame.image.load('ASSESSMENTS/Y9T2 Attempt 2/Assets/platformerGraphicsDeluxe_Updated/Tiles/liquidLavaTop_mid.png')
        self.image = pygame.transform.scale(lava_img, (tile_size, tile_size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Instancing
blob_group = pygame.sprite.Group() 
lava_group = pygame.sprite.Group()
world = World(mapdata.world_data)
player = Player(80, screen_height - 130)

# Button instancing
restart_button = Button(screen_width // 2 - 100, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 250, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 50, screen_height // 2, exit_img)

# Game loop
run = True
while run:
    
    # Fixing the fps
    clock.tick(fps) 
    
    # Blitting the background
    screen.blit(bg_img, (0, 0))
    screen.blit(moon_img, (100, 100))
    
    if main_menu == True:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        # Drawing what the player sees
        world.draw()
        
        if game_over == 0:
            blob_group.update()
            
        blob_group.draw(screen)
        lava_group.draw(screen)
        
        game_over = player.update(game_over)
        
        # If player death
        if game_over == 1:
            if restart_button.draw():
                player.reset(80, screen_height - 130)
                game_over = 0
        
    # Quitting
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
    
# Quit
pygame.quit()
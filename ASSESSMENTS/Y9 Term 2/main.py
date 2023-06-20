import sys
import pygame

class Player:
    # Declares all the metadata on the player
    def __init__(self, image: pygame.Surface): # 
        self.x = 0
        self.y = 0
        self.gravity = 9.8
        self.image = image
        self.width = image.get_width()
        self.height = image.get_height()

        # Jump fields
        self.airbone = False
        self.jumping= False
        self.cache_y = self.y
    
    def draw(self, screen: pygame.Surface): # self refers to the current state of the "self" and sets its own metadata
        screen.blit(self.image, (self.x, self.y)) # draws itself to its current location as defined
    
    def update(self):
        # Move up - jumping
        if self.jumping:
            up_translate = 6
            max_jump_height = 120

            actual_y = self.y + self.height
            new_y = actual_y - up_translate

            if new_y < self.cache_y - max_jump_height:
                # maxheight function exit
                new_y = self.cache_y - max_jump_height
                self.jumping = False
            
            self.y = new_y - self.height
        
        # Move down - falling
        if not self.jumping:
            down_translate = 6

            actual_y = self.y + self.height

            new_y = actual_y + down_translate
    
            # checks for ground contact
            if new_y > 800 - 100:
                new_y = 800 - 100
                self.airbone = False
            
            self.y = new_y - self.height
    
    def jump(self):
        if not self.jumping and not self.airbone:
            self.cache_y = self.y
            self.airbone = True
            self.jumping = True
            

pygame.init()

spriteImg1 = pygame.image.load('Assets/spritewalk1.png')
spriteImg2 = pygame.image.load('Assets/spritewalk2.png')
spriteForward = pygame.image.load('Assets/spriteforward.png')

fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rex's platformer game")
 
player = Player(spriteImg1)
 
# Game loop.
while True:
  screen.fill((0, 0, 0))
  HEIGHT = screen.get_height()
  WIDTH = screen.get_width()
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

  keys = pygame.key.get_pressed()
  
  if keys[pygame.K_LEFT]:
      player.x -= 10
  if keys[pygame.K_RIGHT]:
      player.x += 10
  if keys[pygame.K_UP]:
    player.jump()

  player.update()

  pygame.draw.rect(screen, (255, 255, 255), (0, HEIGHT - 100, WIDTH, 100))
  player.draw(screen)
  
  pygame.display.flip()
  fpsClock.tick(fps)

pygame.quit()
quit()
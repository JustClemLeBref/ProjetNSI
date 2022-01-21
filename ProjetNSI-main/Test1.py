#importation des modules nécessaires
import pygame
import keyboard
import random

#création de la fenetre
pygame.init()

#dimension de la fenetre
screen_width = 1440
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))

#titre, background et icon
pygame.display.set_caption("BLOOBEY")
background = pygame.image.load('.\\GRAPHISME\\background1.png')
icon = pygame.image.load('.\\GRAPHISME\\bloobey-logo.png')
pygame.display.set_icon(icon)

GameOver=pygame.image.load('.\\GRAPHISME\\GAMEOVER.jpg')
GameOver = pygame.transform.scale(GameOver, (1000, 1000))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#ajoute en plus
pygame.display.flip()
clock = pygame.time.Clock()



class game_character(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.description = "default"
        self.image = pygame.image.load(image)
        self.size = (150,150)
        self.transform = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.x = 300
        self.y = 640
        self.rect = self.image.get_rect()
        self.rect.height = self.size[0]
        self.isJump = False
        self.jumpCount = 10
        self.vel = 100
        self.speed = 20
    
    def update(self):
        self.calc_grav()
        
        self.rect.topleft = self.x, self.y

    def calc_grav(self):
        
        if self.y == 0:
            self.y = 1
        else:
            self.y += .35
 
        # See if we are on the ground.
        if self.rect.y >= screen_height - 150 and self.y >= 0:
            self.y= 0
            self.rect.y = screen_height - self.rect.height
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -10

class Ennemie(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.description = "default"
        self.image = pygame.image.load(image)
        self.size = (150,150)
        self.transform = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.x = 300
        self.y = 640
        self.rect = self.image.get_rect()
        self.isJump = False
        self.jumpCount = 10
        self.vel = 100
        self.speed = 20
    
    def update(self):

        self.rect.topleft = self.x, self.y

class Platform(pygame.sprite.Sprite):
    """ Platform Bloobey jump on """
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.load('.\\GRAPHISME\\Grass_Block.jpg')
 
        self.rect = self.image.get_rect()
 
class Level(pygame.sprite.Sprite):
 
    def __init__(self, width, height):
        super().__init__()
 
        self.image = pygame.Surface([width, height])
        self.image.load('.\\GRAPHISME\\Grass_Block.jpg')
 
        self.rect = self.image.get_rect()
 
class BUTTON(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.description = "default"
        self.image = pygame.image.load(image)
        self.size = (150,150)
        self.transform = pygame.transform.scale(self.image, (self.size[0], self.size[1]))
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 640
        self.clicked = False
        self.endresult = 0

    def click(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
    def update(self):
        self.rect.topleft = self.x, self.y
        
SLIME_obj_image = '.\\GRAPHISME\\bloobey-logo.png'
SLIME_obj = game_character(SLIME_obj_image)
SLIME_obj.description = "Slimey"
SLIME_obj.size = (200,200)
SLIME_obj.image = SLIME_obj.transform
coordone_SLIME_obj=(400,750)
SLIME_obj.x = coordone_SLIME_obj[0]
SLIME_obj.y = coordone_SLIME_obj[1]

Ennemie_obj_image = '.\\GRAPHISME\\monstre_test.png'
Ennemie_obj = Ennemie(Ennemie_obj_image)
Ennemie_obj.description = "Enemy"
Ennemie_obj.size = (150,150)
Ennemie_obj.image = SLIME_obj.transform
coordone_Ennemie_obj=(300,500)
Ennemie_obj.x = coordone_Ennemie_obj[0]
Ennemie_obj.y = coordone_Ennemie_obj[1]


all_sprites = pygame.sprite.Group(Ennemie_obj, SLIME_obj)
SLIMES = pygame.sprite.Group(SLIME_obj)

image_YES = '.\\GRAPHISME\\YES.png'
image_NO = '.\\GRAPHISME\\NO.png'

YES = BUTTON(image_YES)
YES.image = YES.transform
coordone_YES=(400,650)
YES.x = coordone_YES[0]
YES.y = coordone_YES[1]
YES.endresult = 0

NO = BUTTON(image_NO)
NO.image = NO.transform
NO.x = YES.x + 450
NO.y = YES.y
NO.endresult = 2

BUTTONS = pygame.sprite.Group(YES, NO)

SLIME_copy = SLIME_obj.image
SLIME_with_flip = pygame.transform.flip(SLIME_copy, True, False)

Ennemie_copy = pygame.image.load('.\\GRAPHISME\\monstre_test(1).png')
Ennemie_with_flip = pygame.transform.flip(Ennemie_copy, True, False)


def restart():
    color = 0
    SLIME_obj.x = 420
    SLIME_obj.y = 640
    Ennemie_obj.x = 900
    Ennemie_obj.y = coordone_Ennemie_obj[1]
    isJump = False
    jumpCount = -11
    vel = 650
    y = 50
    
isJump = False
jumpCount = 10
vel = 100
y = 50
Position=0
color=0
touched = 0
ancien=SLIME_obj.x
hearts=1

active = True



while active:
    if SLIME_obj.x != ancien:
        print(SLIME_obj.x)
        print(SLIME_obj.y)
        ancien=SLIME_obj.x

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            active = False
            

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'): # si la touche 'z' est pressé
            print('You Pressed ECHAP Key!')
            active = False
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete
    
    #recherche de collision

    all_sprites.update()

    collided_bananas = pygame.sprite.spritecollide(Ennemie_obj, SLIMES, False)
    for collided_banana in collided_bananas:
        if hearts == 3:
            pygame.time.delay(10)
            color=1
        else:
            restart()
            hearts+=1
        #chargement des personage
    
    try:
        #si la touche 'q' est appuier
        if keyboard.is_pressed('d'):
            if SLIME_obj.x != 1000:
                SLIME_obj.x=SLIME_obj.x+10
            SLIME_obj.image=SLIME_with_flip
        # si la touche 'q' est appuier
        if keyboard.is_pressed('q'):
            if SLIME_obj.x!=-10:
                SLIME_obj.x=SLIME_obj.x-10
            SLIME_obj.image=SLIME_copy
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete

    if not(isJump):
        if keyboard.is_pressed('z'):  # si la touche 'z' est pressé
            if SLIME_obj.y > vel:
                SLIME_obj.y -= vel
            isJump = True
    else:
        if jumpCount >= -10:
            SLIME_obj.y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            SLIME_obj.y += 2*y
            jumpCount = 10
            isJump = False

    #boucle des mouvements du monstre

    if Position==0:
        if Ennemie_obj.x != 1000:
            Ennemie_obj.x += 10
            Ennemie_obj.image=Ennemie_copy
        else:
            Position = 1
    if Position == 1:
        if Ennemie_obj.x!=-10:
            Ennemie_obj.x -= 10
            Ennemie_obj.image = Ennemie_with_flip
        else:
            Position = 0
    display_surface = pygame.display.set_mode((screen_width, screen_height))

    #changement de scene

    if color == 1:
        display_surface.blit(GameOver,(200,100))
        BUTTONS.update()
        BUTTONS.draw(display_surface)
        YES.click(event_list)
        if YES.click(event_list):
            hearts = 1
            color=0
            restart()
            
        if NO.click(event_list):
            active = False
    if color == 2:
        active = False
        
    if color == 0:
        display_surface.blit(background,(0,0))
        all_sprites.draw(screen)
    pygame.display.update()
    clock.tick(30)
    
pygame.quit()

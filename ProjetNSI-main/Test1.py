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

#Image du GameOver
GameOver=pygame.image.load('.\\GRAPHISME\\GAMEOVER.jpg')
GameOver = pygame.transform.scale(GameOver, (1000, 1000))

white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#on ajoute en plus
pygame.display.flip()
clock = pygame.time.Clock()


#classe du joueur, ses stats
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
        self.isJump = False
        self.jumpCount = 10
        self.vel = 100
        self.speed = 20

    #création de la gravité
    def update(self):
        self.calc_grav()
        
        self.rect.topleft = self.x, self.y

    def calc_grav(self):
        
        if self.y == 0:
            self.y = 1
        else:
            self.y += .90
 
        # on rregarde si le joueur est au sol
        if self.rect.y >= screen_height - 150 and self.y >= 0:
            self.y= 0
            self.y = screen_height - self.rect.heightww
            
    #variable pour le saut du joueur
    def jump(self):
        # appelé quand le joueur veut sauter
 
        # On bouge un peu vers le bas et on regarde si il y a une plateforme en dessous
        self.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.y -= 2
 
        # si on peut sauter, on définit la vitesse du saut
        if len(platform_hit_list) > 0 or self.rect.bottom >= screen_height:
            self.y = -10
            
#classe pour les ennemies, ses stats
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
    #La Platforme où Bloobey saute 
 
    def __init__(self, width, height):
        super().__init__()
        
        #image du block principale
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('.\\GRAPHISME\\Spikes.png')
 
        self.rect = self.image.get_rect()

#classe du Bouton clickable 
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
     
    #variable du clickage de bouton
    def click(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    return True
    def update(self):
        self.rect.topleft = self.x, self.y
        
# Create platforms for the level
class Level():
    """ Definition for level 1. """
 
    def __init__(self):
        """ Create level 1. """
 
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 [210, 70, 200, 200],
                 ]
 
        # Go through the array above and add platforms
        for platform in level:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            self.platform_list.add(block)
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
    def draw(self, screen):
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
#variable qui reset le personnage et le replace au début 
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

#Bloobey, apparition sur l'écran      
SLIME_obj_image = '.\\GRAPHISME\\bloobey-logo.png'
SLIME_obj = game_character(SLIME_obj_image)
SLIME_obj.description = "Slimey"
SLIME_obj.size = (200,200)
SLIME_obj.image = SLIME_obj.transform
coordone_SLIME_obj=(400,750)
SLIME_obj.x = coordone_SLIME_obj[0]
SLIME_obj.y = coordone_SLIME_obj[1]

#apparition de l'ennemi sur l'écran
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

#boutons Yes et No et leurs valeurs
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
    # Create all the levels
    level_list = []
    level_list.append( Level() )
 
    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]
 
    if SLIME_obj.x != ancien:
        print(SLIME_obj.x)
        print(SLIME_obj.y)
        ancien=SLIME_obj.x

    event_list = pygame.event.get()

    for event in event_list:
        if event.type == pygame.QUIT:
            active = False
            

    try:  # try préviens le code si une autre touche que celle donné est appuyé par l'utilisateur
        if keyboard.is_pressed('ESC'): # si la touche 'échappe' est pressé
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
        #chargement des personages
    
    try:
        #si la touche 'd' est appuyer
        if keyboard.is_pressed('d'):
            if SLIME_obj.x != 1000:
                SLIME_obj.x=SLIME_obj.x+10
            SLIME_obj.image=SLIME_with_flip
        # si la touche 'd' est appuyer
        if keyboard.is_pressed('q'):
            if SLIME_obj.x!=-10:
                SLIME_obj.x=SLIME_obj.x-10
            SLIME_obj.image=SLIME_copy
        if keyboard.is_pressed('z'):
            SLIME_obj.jump()
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete

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
    
    #changement de scene
    display_surface = pygame.display.set_mode((screen_width, screen_height))

    if color == 1:
        display_surface.blit(GameOver,(200,100))
        BUTTONS.update()
        BUTTONS.draw(display_surface)
        YES.click(event_list)
        if YES.click(event_list):
            hearts = 1
            color=0
            restart()
        #si on appuie sur 'No', on quitte le jeu    
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
#fin du code et sortie de la fenêtre

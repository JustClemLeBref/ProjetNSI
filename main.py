
#importation des modules nécessaires
import pygame
import keyboard
import random

#dimension de la fenetre
screen_width = 1440
screen_height = 1000

#on ajoute en plus
pygame.display.flip()
clock = pygame.time.Clock()


white = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)



#classe du joueur, ses stats
class game_character(pygame.sprite.Sprite):
    def __init__(self,image,size):
        super().__init__()
        self.description = "default"
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.x = 300
        self.y = 640
        self.rect = self.image.get_rect()
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0 
        # List of sprites we can bump against
        self.level = None

    #création de la gravité
    def update(self):
        self.calc_grav()
        self.rect.topleft = self.x, self.y
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
 
        # See if we are on the ground.
        if self.rect.y >= screen_height - self.rect.height and self.change_y >= 0:
            self.change_y = 0
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
 
    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -6
 
    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 6
 
    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0
 
            
            
#classe pour les ennemies, ses stats
class Ennemie(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.description = "default"
        self.size = (150,150)
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size[0], self.size[1]))
        self.x = 300
        self.y = 640
        self.rect = self.image.get_rect()
    
    def update(self):
        self.rect.topleft = self.x, self.y
    def deplacement(self):
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
class Platform(pygame.sprite.Sprite):
    #La Platforme où Bloobey saute 
 
    def __init__(self, width, height):
        super().__init__()
        
        #image du block principale
        self.image = pygame.Surface([width, height])
        self.image = pygame.image.load('GRAPHISME/Spikes.png')
 
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
        
class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """
 
    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
         
        # Background image
        self.background = None
 
    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
 
    def draw(self):
        """ Draw everything on this level. """
 
 
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
 
# Create platforms for the level
class Level_1(Level):
    """ Definition for level 1. """
 
    def __init__(self,game_character):
        """ Create level 1. """
 
        self.platform_list = pygame.sprite.Group()
        # Array with width, height, x, and y of platform
        level = [[210, 70, 500, 500],
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 [210, 70, 200, 200],
                 [400, 500, 200, 200],
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
    def draw(self, screen):
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
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

def GameOver_Scene():
    #Image du GameOver
    GameOver=pygame.image.load('GRAPHISME/GAMEOVER.jpg')
    GameOver = pygame.transform.scale(GameOver, (1000, 1000))
    
    #boutons Yes et No et leurs valeurs
    image_YES = 'GRAPHISME/YES.png'
    image_NO = 'GRAPHISME/NO.png'
    
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
    
    display_surface.blit(GameOver,(200,100))
    
    BUTTONS.update()
    
    BUTTONS.draw(display_surface)
    
    if YES.click(event_list):
        hearts = 1
        color=0
        restart()
    #si on appuie sur 'No', on quitte le jeu    
    if NO.click(event_list):
        active = False


def main():
    """ Main Program """
    pygame.init()
    
    screen = pygame.display.set_mode((screen_width, screen_height))
    
    #titre, background et icon
    pygame.display.set_caption("BLOOBEY")
    background = pygame.image.load('GRAPHISME/Background_Sized.png')
    icon = pygame.image.load('GRAPHISME/bloobey-logo.png')
    pygame.display.set_icon(icon)
    
    #Bloobey, apparition sur l'écran      
    SLIME_obj_image = pygame.image.load('GRAPHISME/bloobey-logo.png')
    SLIME_obj_size = (200,200)
    SLIME_obj = game_character(SLIME_obj_image,SLIME_obj_size)
    coordone_SLIME_obj=(400,750)
    SLIME_obj.x = coordone_SLIME_obj[0]
    SLIME_obj.y = coordone_SLIME_obj[1]
    
    #apparition de l'ennemi sur l'écran
    Ennemie_obj_image = 'GRAPHISME/monstre_test.png'
    Ennemie_obj = Ennemie(Ennemie_obj_image)
    Ennemie_obj.description = "Enemy"
    Ennemie_obj.size = (150,150)
    coordone_Ennemie_obj=(300,500)
    Ennemie_obj.x = coordone_Ennemie_obj[0]
    Ennemie_obj.y = coordone_Ennemie_obj[1]
    
    SLIME_copy = SLIME_obj.image
    SLIME_with_flip = pygame.transform.flip(SLIME_copy, True, False)
    
    Ennemie_copy = pygame.image.load('GRAPHISME/monstre_test(1).png')
    Ennemie_with_flip = pygame.transform.flip(Ennemie_copy, True, False)

    # Create all the levels
    level_list = []
    level_list.append( Level_1(SLIME_obj) )
    
    isJump = False
    jumpCount = 10
    vel = 100
    y = 50
    ancien=SLIME_obj.x
    hearts=1 
    
    active = True
    
    all_sprites = pygame.sprite.Group(Ennemie_obj, SLIME_obj)
    SLIMES = pygame.sprite.Group(SLIME_obj)

    
    while active:

        
        # Set the current level
        current_level_no = 0
        current_level = level_list[current_level_no]
        
        if SLIME_obj.x != ancien:
            print(SLIME_obj.x)
            print(SLIME_obj.y)
        ancien=SLIME_obj.x
    
        event_list = pygame.event.get()
            
        keys = pygame.key.get_pressed() 
          
        for event in event_list:
            if event_list == pygame.QUIT:
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('You Pressed ECHAP Key!')
                    active = False
                if event.key == pygame.K_RIGHT:
                    if SLIME_obj.x != 1000:
                        SLIME_obj.x=SLIME_obj.x+10
                    SLIME_obj.image=SLIME_with_flip
                if event.key == pygame.K_LEFT:
                    if SLIME_obj.x!=-10:
                        SLIME_obj.x=SLIME_obj.x-10
                    SLIME_obj.image=SLIME_copy
                if event.key == pygame.K_UP:
                    SLIME_obj.jump()
                if event.type == pygame.QUIT:
                    active = False

        
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
    
        
        #changement de scene
        display_surface = pygame.display.set_mode((screen_width, screen_height))
        display_surface.blit(background,(0,0))
        all_sprites.draw(screen)
        current_level.draw(screen)
        pygame.display.update()
        clock.tick(30)
    #fin du code et sortie de la fenêtre
    pygame.quit()


main()


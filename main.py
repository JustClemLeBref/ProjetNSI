
#importation des modules nécessaires
import pygame
import teste1

#dimension de la fenetre
screen_width = 1440
screen_height = 1000

#on ajoute en plus
clock = pygame.time.Clock()

GREEN = (255, 255, 255)
red = (255, 0, 0)
black = (0, 0, 0)

#classe du joueur, ses stats
class Player(pygame.sprite.Sprite):
    def __init__(self,image,size):
        super().__init__()
        self.description = "default"
        self.image = pygame.transform.scale(image, (size[0], size[1]))
        self.original = self.image
        self.original_flip = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        
        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0 
        
        # List of sprites we can bump against
        self.level = None


    def update(self):
        self.calc_grav()
        self.rect.topleft = self.rect.x, self.rect.y
        # Move left/right
        self.rect.x += self.change_x
        
 
        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right
 
        # Move up/down
        self.rect.y += self.change_y
        
        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            # Stop our vertical movement
            self.change_y = 0
        
        
        
    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .25
 
        # See if we are on the ground.
        if self.rect.y >= screen_height - self.rect.height-100  and self.change_y >= 0: 
            self.change_y = 0
            self.rect.y = screen_height - self.rect.height-100
 
    def jump(self):
        """ Called when user hits 'jump' button. """
 
        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down
        # 1 when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= screen_height:
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
        self.original = self.image
        self.original_flip = pygame.transform.flip(self.image, True, False)
        self.x = 300
        self.y = 640
        self.rect = self.image.get_rect()
        self.state = 0
    
    def update(self):
        self.rect.topleft = self.x, self.y
        #self.deplacement()
    def deplacement(self):
        if self.state==0:
            if self.x != 1000:
                self.x += 10
                self.image=self.original
            else:
                self.state = 1
        if self.state == 1:
            if self.x!=-10:
                self.x -= 10
                self.image = self.original_flip
            else:
                self.state = 0


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
        
class Platform(pygame.sprite.Sprite):
    #La Platforme où Bloobey saute 
 
    def __init__(self, width, height,image):
        super().__init__()
        
        #image du block principale
        
        
        self.image = pygame.Surface([width, height])
        #self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        #self.image.fill(GREEN)
 
        self.rect = self.image.get_rect()
        

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
        self.platform_list.draw(Level.screen)
        self.enemy_list.draw(Level.screen)
 
# Create platforms for the level
class Level_1(Level):
    """ Definition for level 1. """
 
    def __init__(self,player):
        """ Create level 1. """
        
        # Call the parent constructor
        Level.__init__(self, player)
        
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\Cubes\SCubeShortD4.png'
        cube2 = 'GRAPHISME\Cubes\SCubeLongD1.png'
        # Array with width, height, x, and y of platform
        level = [[100, 100, 100, 810,cube1],
                 [100, 100, 0, 810,cube2],
                 [100, 100, 500, 810,cube2],
                 [100, 100, 600, 810,cube1],
                 [100, 100, 900, 710,cube2],
                 [100, 100, 1000, 710,cube1],
                 [100, 100, 400, 510,cube2],
                 [100, 100, 500, 510,cube1],]
                
                 
        Monsters = [['GRAPHISME/monstre_test.png', (150,150), (0,500)]]
        
        # Go through the array above and add platforms
        
        for platform in level:
            block = Platform(platform[0], platform[1],platform[4])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)
        
        # Go through the array above and add platforms
        for ennemie in Monsters:
            monstre = Ennemie(ennemie[0])
            monstre.size = ennemie[1]
            coordone_monstre = ennemie[2]
            monstre.x = coordone_monstre[0]
            monstre.y = coordone_monstre[1]
            self.enemy_list.add(monstre)
            
            
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()
        
    def draw(self, screen):
        # Draw all the sprite lists that we have
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
#variable qui reset le personnage et le replace au début 



def main():
    
    """ Main Program """
    pygame.init()
    
    screen = pygame.display.set_mode((screen_width, screen_height))

    keys = pygame.key.get_pressed() 
    
    #titre, background et icon
    pygame.display.set_caption("BLOOBEY")
    background = pygame.image.load('GRAPHISME/Background_Sized.png')
    icon = pygame.image.load('GRAPHISME/bloobey-logo.png')
    pygame.display.set_icon(icon)
    
    #Bloobey, apparition sur l'écran      
    SLIME_obj_image = pygame.image.load('GRAPHISME/bloobey-logo.png')
    SLIME_obj_size = (133,100)
    SLIME_obj = Player(SLIME_obj_image,SLIME_obj_size)
    

    
    # Create all the levels
    level_list = []
    level_list.append( Level_1(SLIME_obj) )
    
    # Set the current level
    current_level_now = 0
    current_level = level_list[current_level_now]
    
    active_sprite_list = pygame.sprite.Group()
    SLIME_obj.level = current_level
    active_sprite_list.add(SLIME_obj)
    
    coordone_SLIME_obj=(100,screen_height - 250)
    SLIME_obj.rect.x = coordone_SLIME_obj[0]
    SLIME_obj.rect.y = coordone_SLIME_obj[1]
    
    

    
    ancien=SLIME_obj.rect.x
    hearts=1 
    
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    active = True
    

    
    while active:
        event_list = pygame.event.get()
        
        
        
        if SLIME_obj.rect.x != ancien:
            print(SLIME_obj.rect.x)
            print(SLIME_obj.rect.y)
        ancien=SLIME_obj.rect.x
        
        for event in event_list:
            
            if event.type == pygame.QUIT:
                print("A")
                active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print('You Pressed ECHAP Key!')
                    active = False
            
            if event.type == pygame.KEYDOWN:
                 
                if event.key == pygame.K_RIGHT:
                    
                    SLIME_obj.go_right()
                        
                    SLIME_obj.image=SLIME_obj.original_flip
                    
                if event.key == pygame.K_LEFT:
                    
                    SLIME_obj.go_left()
                        
                    SLIME_obj.image=SLIME_obj.original
                    
                if event.key == pygame.K_UP:
                    
                    SLIME_obj.jump()
                       
            if event.type == pygame.KEYUP:
                
                if event.key == pygame.K_LEFT and SLIME_obj.change_x < 0:
                    
                    SLIME_obj.stop()
                    
                if event.key == pygame.K_RIGHT and SLIME_obj.change_x > 0:
                    
                    SLIME_obj.stop()
            """
        """
        # Update items in the level
        current_level.update()
        active_sprite_list.update()
    
    
                    
        # If the player gets near the right side, shift the world left (-x)
        if SLIME_obj.rect.right > screen_width:
            SLIME_obj.rect.right = screen_width
 
        # If the player gets near the left side, shift the world right (+x)
        if SLIME_obj.rect.left < 0:
            SLIME_obj.rect.left = 0
        

        #recherche de collision
        collision_sprite = pygame.sprite.spritecollide(SLIME_obj, current_level.enemy_list, False)
        
        for Collision in collision_sprite:
            
            GameOver_Scene(event_list)
        if SLIME_obj.rect.y == 800:
            GameOver_Scene(event_list)
        
        
        screen.blit(background,(0,0))
        active_sprite_list.draw(screen)
        current_level.draw(screen)
        

        # Limit to 60 frames per second
        clock.tick(60)
        
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        
    #fin du code et sortie de la fenêtre
    pygame.quit()



def GameOver_Scene():
    pygame.init()
    display_surface = pygame.display.set_mode((screen_width, screen_height))
    
    pygame.display.set_caption('Image')   

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
    
    active = True
    while active:
        pygame.display.update() 
        Event = pygame.event.get()
        display_surface.blit(GameOver,(200,100))
        BUTTONS.update()
        BUTTONS.draw(display_surface)
        
        if YES.click(Event):
            active = False
            pygame.quit()
            restart()
        #si on appuie sur 'No', on quitte le jeu    
        if NO.click(Event):
            active=False
            pygame.quit()

def restart():
    main()
    GameOver_Scene()

teste1.mainmenu()
restart()


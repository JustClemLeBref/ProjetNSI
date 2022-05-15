#importation des modules nécessaires et des autres fichiers contenant le reste du code
import pygame
from pygame import mixer
import random
from mainmenu import *
from levels import *
from end_screen import *

#dimension de la fenetre
screen_width = 1425
screen_height = 1000


clock = pygame.time.Clock()

Vert = (255, 255, 255)
rouge = (255, 0, 0)
noir = (0, 0, 0)

def main():
    
    #fonction principale du jeu 
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
    SLIME_obj_size = (100,66)
    SLIME_obj = Player(SLIME_obj_image,SLIME_obj_size)


    #def de la musique
    pygame.mixer.init()
    pygame.mixer.music.load('.\\main_screen_images\\musique_fort_boyard.ogg')
    pygame.mixer.music.play()

    
    # On crée tout les niveaux
    level_list = []
    level_list.append(Level_1(SLIME_obj))
    level_list.append(Level_2(SLIME_obj))
    level_list.append(Level_3(SLIME_obj))
    level_list.append(Level_4(SLIME_obj))
    level_list.append(Level_5(SLIME_obj))

    
    #On place le premier niveau en premier
    current_level_now = 0

    #coordonnée du joueur au début
    coordone_SLIME_obj=(100,screen_height - 300)
    SLIME_obj.rect.x = coordone_SLIME_obj[0]
    SLIME_obj.rect.y = coordone_SLIME_obj[1]
    
    
    ancien=SLIME_obj.rect.x

    
    #barre de vie de Bloobey, pour quan il a toute sa vie ou moins
    full_hearts = '.\\GRAPHISME\\LifeBarFULL.png'
    two_hearts ='.\\GRAPHISME\\LifeBar2.png'
    one_hearts = '.\\GRAPHISME\\LifeBar1.png'
    hearts_full = BUTTON(full_hearts)
    hearts_full.image = pygame.transform.scale(pygame.image.load(full_hearts), (300,300))
    hearts_full.x = 0
    hearts_full.y = 0
    BUTTON_full=pygame.sprite.Group(hearts_full)
    
    hearts_2 = BUTTON(two_hearts)
    hearts_2.image = pygame.transform.scale(pygame.image.load(two_hearts), (300,300))
    hearts_2.x = 0
    hearts_2.y = 0
    
    BUTTON_2_hearts = pygame.sprite.Group(hearts_2)
    
    hearts_1 = BUTTON(one_hearts)
    hearts_1.image = pygame.transform.scale(pygame.image.load(one_hearts), (300,300))
    hearts_1.x = 0
    hearts_1.y = 0
    
    BUTTON_1_hearts = pygame.sprite.Group(hearts_1)
        
    #Variables pour gérer la vitesse de msie à jour de l'écran
    clock = pygame.time.Clock()
    Quit = True
    End= False
    active = True
    hearts = 2
    total=0
    
    while active:
        
        current_level = level_list[current_level_now]
        
        active_sprite_list = pygame.sprite.Group()
        SLIME_obj.level = current_level
        active_sprite_list.add(SLIME_obj)
        event_list = pygame.event.get()
        
        #inutilisé mais pas supprimé au cas où d'un éventuel bug
        """
        if SLIME_obj.rect.x != ancien:
            print(SLIME_obj.rect.x)
            print(SLIME_obj.rect.y)
        ancien=SLIME_obj.rect.x
        """
        
        for event in event_list:
            
            if event.type == pygame.QUIT:
                active = False
                Quit = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    active = False
                    Quit = False
            #variables pour les touches du clavier qui interagissent avec le jeu, et leurs effets
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
                    
        SLIME_obj.animate()
        

        #On met à jour les objets du niveau
        
        current_level.update()
        active_sprite_list.update()
        
        #On cherche des collisions avec pygame

        #affichage de la barre de vie
        screen.blit(background,(0,0))
        active_sprite_list.draw(screen)
        current_level.draw(screen)
        
        if hearts == 2:
            BUTTON_full.draw(screen)
        if hearts == 1:
            BUTTON_2_hearts.draw(screen)
        if hearts == 0:
            BUTTON_1_hearts.draw(screen)
        
        
        #On met à jour l'écran après chaque actions du jeu
        pygame.display.flip()
        
        collision_sprite = pygame.sprite.spritecollide(SLIME_obj, current_level.enemy_list, False)
        
        #reset du personnage et du niveau pour quand il perd une vie
        current_level.scroll()
        for Collision in collision_sprite:
            if hearts > 0:
                hearts -=1
                current_level.startover()
                SLIME_obj.rect.x = 100
                SLIME_obj.rect.y = screen_height - 300
            else:
                active = False
        
        if SLIME_obj.rect.y >= screen_height:
            if hearts > 0:
                hearts -=1
                current_level.startover()
                SLIME_obj.rect.x = 100
                SLIME_obj.rect.y = screen_height - 300
            else:
                active = False
        #60 imgaes par seconde maximum
        current_level.update()
        current_level.x_worldshift = 0
        clock.tick(60)
        

        
        collision_sprite = pygame.sprite.spritecollide(SLIME_obj, current_level.Door, False)
        
        for Collision in collision_sprite:
            if current_level_now < len(level_list)-1:
                print(current_level_now)
                current_level_now += 1
                SLIME_obj.rect.x = coordone_SLIME_obj[0]
                SLIME_obj.rect.y = coordone_SLIME_obj[1]
            else:
                active=False
                Quit=False
                End = True
                
        clock.tick(60)
    #fin du code et sortie de la fenêtre
    if Quit:
        Pub()
        GameOver_Scene()
        pygame.quit()
    else:
        if End:
            endmenu()
        pygame.quit()
        
 #fonction des pubs, qui s'affiche avant l'écran de game over, pour payer les développeurs
def Pub():
    display_surface =  pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Pub')
    
    Pub1 = 'GRAPHISME/pub.png'
    Pub2 = 'GRAPHISME/pub_BWM.png'
    Pub3 = 'GRAPHISME/Pub_Yphone.png'
    skip_image = 'GRAPHISME/Skip_Ad.png'
    
    coordone_skip = (1300, 800)
    
    random_int = random.randint(1,3)
    if random_int == 1:
        pub= pygame.image.load(Pub1)
        pub= pygame.transform.scale(pub, (1500,1000))
        
        skip = BUTTON(skip_image,)
        
        skip.x = coordone_skip[0]
        skip.y = coordone_skip[1]
    
    elif random_int == 2:
        pub= pygame.image.load(Pub2)
        pub= pygame.transform.scale(pub, (1500,1000))
        
        skip = BUTTON(skip_image,)
        
        skip.x = coordone_skip[0]
        skip.y = coordone_skip[1]
       
    elif random_int == 3:
        pub= pygame.image.load(Pub3)
        pub= pygame.transform.scale(pub, (1500,1000))
        
        skip = BUTTON(skip_image,)
        
        skip.x = coordone_skip[0]
        skip.y = coordone_skip[1]
    
    BUTTONS = pygame.sprite.GroupSingle(skip)
    
    
    active = True
    while active:
        pygame.display.update()
        Event = pygame.event.get()
        display_surface.blit(pub,(0,0))
        BUTTONS.draw(display_surface)
        
        for event in Event : 
            if event.type == pygame.QUIT :
                active=False 
                
        if skip.click(Event):
            active = False
        BUTTONS.update()
    


#fonction game over, demande si oui ou non on souhaite rejouer
def GameOver_Scene():
    
    display_surface = pygame.display.set_mode((screen_width, screen_height))
    white = (0, 0, 0) 
    pygame.display.set_caption('GameOver_Scene')   

    #Image du GameOver
    GameOver=pygame.image.load('GRAPHISME/GAMEOVER.jpg')
    GameOver = pygame.transform.scale(GameOver, (1000, 1000))
    
    #boutons Yes et No et leurs valeurs
    image_YES = 'GRAPHISME/YES.png'
    image_NO = 'GRAPHISME/NO.png'
    
    YES = BUTTON(image_YES)
    coordone_YES=(400,650)
    YES.x = coordone_YES[0]
    YES.y = coordone_YES[1]

    
    NO = BUTTON(image_NO)
    NO.x = YES.x + 450
    NO.y = YES.y
    
    BUTTONS = pygame.sprite.Group(YES,NO)
   

#boucle priincipal du jeu qui fait tourner la fenêtre et le jeu
    active = True
    while active:
        pygame.display.update() 
        Event = pygame.event.get()
        display_surface.fill(white) 
        display_surface.blit(GameOver,(200,100))
        BUTTONS.draw(display_surface)
        
        for event in Event : 
            if event.type == pygame.QUIT :
                active=False 
                
        if YES.click(Event):
            active = False
            main()
          
        #si on appuie sur 'No', on quitte le jeu    
        if NO.click(Event):
            active=False
         
        
        BUTTONS.update()
        
    pygame.quit()
   

return1 = mainmenu()
if return1:
    main()

#importation des modules nécessaires
import pygame
from pygame import mixer
import random
import teste1
from levels import *

#dimension de la fenetre
screen_width = 1440
screen_height = 1000

#on ajoute en plus
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
    
    #On place le premier niveau en premier
    current_level_now = 0

    
    coordone_SLIME_obj=(100,screen_height - 300)
    SLIME_obj.rect.x = coordone_SLIME_obj[0]
    SLIME_obj.rect.y = coordone_SLIME_obj[1]
    
    

    
    ancien=SLIME_obj.rect.x
    hearts=1 
    
    #Variables pour gérer la vitesse de msie à jour de l'écran
    clock = pygame.time.Clock()
    Quit = True
    active = True
    moved = 0

    
    while active:
        print(current_level_now)
        current_level = level_list[current_level_now]
        
        active_sprite_list = pygame.sprite.Group()
        SLIME_obj.level = current_level
        active_sprite_list.add(SLIME_obj)
        event_list = pygame.event.get()
        
        
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
                    print('You Pressed ECHAP Key!')
                    active = False
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

        
        if SLIME_obj.rect.x >= 2*screen_width/4:
            if SLIME_obj.rect.x != ancien:
                for plat in current_level.platform_list:
                    if SLIME_obj.change_x > 0:
                        plat.rect.x -= SLIME_obj.change_x
                for door in current_level.Door:
                    if SLIME_obj.change_x > 0:
                        door.x -= SLIME_obj.change_x
                for ennemie in current_level.enemy_list:
                    if SLIME_obj.change_x > 0:
                        ennemie.rect.x -= SLIME_obj.change_x
        if moved==1:
            if SLIME_obj.rect.x <= 2*screen_width/4:
                if SLIME_obj.rect.x != ancien:
                    for plat in current_level.platform_list:
                        if SLIME_obj.change_x < 0:
                            plat.rect.x -= SLIME_obj.change_x
                    for door in current_level.Door:
                        if SLIME_obj.change_x < 0:
                            door.x -= SLIME_obj.change_x
                    for ennemie in current_level.enemy_list:
                        if SLIME_obj.change_x < 0:
                            ennemie.rect.x -= SLIME_obj.change_x               
        if SLIME_obj.rect.x >= 2*screen_width/4:
            moved = 1

        ancien=SLIME_obj.rect.x

        #On met à jour les objets du niveau
        current_level.update()
        active_sprite_list.update()
    
        #Si le joueur va trop à droite,
        #il ne peut plus avancer plus à droite mais l'écran bouge à la même vitesse
        #pour simuler une caméra qui suit le joueur
        if SLIME_obj.rect.right > screen_width:
            SLIME_obj.rect.right = screen_width
 
        #Pareil mais pour la gauche
        if SLIME_obj.rect.left < 0:
            SLIME_obj.rect.left = 0
        

        #On cherche des collisions avec pygame
        collision_sprite = pygame.sprite.spritecollide(SLIME_obj, current_level.enemy_list, False)
        
        for Collision in collision_sprite:
            active = False
        
            
        screen.blit(background,(0,0))
        active_sprite_list.draw(screen)
        current_level.draw(screen)
        

        #60 imgaes par seconde maximum
        
        clock.tick(60)
        
        #On met à jour l'écran après chaque actions du jeu
        pygame.display.flip()
        
        if SLIME_obj.rect.y >= screen_height:
            print("dead")
            active = False
        collision_sprite = pygame.sprite.spritecollide(SLIME_obj, current_level.Door, False)
        
        for Collision in collision_sprite:
            if current_level_now < len(level_list)-1:
                print(level_list)
                current_level_now += 1
                SLIME_obj.rect.x = coordone_SLIME_obj[0]
                SLIME_obj.rect.y = coordone_SLIME_obj[1]
            else:
                if current_level_now == len(level_list):
                    active=False
        clock.tick(60)
    #fin du code et sortie de la fenêtre
    if Quit:
        print("quit")
        Pub()
        GameOver_Scene()
    else:
        pygame.quit()
    
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
        
        if skip.click(Event):
            active = False
            GameOver_Scene()
        BUTTONS.update()
        



def GameOver_Scene():
    
    display_surface = pygame.display.set_mode((screen_width, screen_height))
    
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
    
    active = True
    while active:
        pygame.display.update() 
        Event = pygame.event.get()
        display_surface.blit(GameOver,(200,100))
        BUTTONS.draw(display_surface)
        BUTTONS.update()
        for event in Event : 
            if event.type == pygame.QUIT :
                active=False 
                
        if YES.click(Event):
            active = False
            main()
          
        #si on appuie sur 'No', on quitte le jeu    
        if NO.click(Event):
            active=False
            print("Quit")
        
        BUTTONS.update()
        
    pygame.quit()
   

return1 = teste1.mainmenu()
if return1==1:
    main()

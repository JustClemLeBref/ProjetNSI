#importation des modules nécessaires
import pygame 
import keyboard  
import sys
import time


#création de la fenetre 
pygame.init() 

#dimension de la fenetre
screen_width = 1440
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height)) 

#ajoute en plus
pygame.display.flip() 
clock = pygame.time.Clock()


#titre, background et icon
pygame.display.set_caption("BLOOBEY") 
background = pygame.image.load('.\\GRAPHISME\\background1.png')
icon = pygame.image.load('.\\GRAPHISME\\bloobey-logo.png')
pygame.display.set_icon(icon)


#csréation du personnage
SLIME_ACTIVE = icon
character_size = (112,95)
character_width = character_size[0]
character_height = character_size[1]
character = pygame.transform.scale(SLIME_ACTIVE, (character_width, character_height))
character_x_pos = 0
character_y_pos = 600
plaform=(character_y_pos,200)

#création des monstres
Monstre = pygame.image.load('GRAPHISME\\monstre_test.png')
Monstre_size = (112,95)
Monstre_width = Monstre_size[0]
Monstre_height = Monstre_size[1]
Monstre = pygame.transform.scale(Monstre, (Monstre_width, Monstre_height))
Monstre_x_pos = 900
Monstre_y_pos = 500

#Variables du saut(personnage)
isJump = False
jumpCount = 10
vel = 100
x = 50
y = 50
width = 40
height = 60
actif = True 
SLIME_ACTIVE = character
y2=y
Position=0
extra=10

#la boucle:
while actif:  
    print("--------")
    print("character_x_pos1:"+str(character_x_pos)+":Monstre_x_pos:"+str(Monstre_x_pos))
    print("character_y_pos1:"+str(character_y_pos)+":Monstre_y_pos:"+str(Monstre_y_pos))
    print("--------")
    
    
    SLIME_copy = character.copy()
    SLIME_with_flip = pygame.transform.flip(SLIME_copy, True, False)
    
    Monstre_copy = Monstre.copy()
    MONSTRE_with_flip = pygame.transform.flip(Monstre_copy, True, False)
    
    
    if not(isJump): 
        if keyboard.is_pressed('z'):  # si la touche 'z' est pressé
            if y > vel:  
                y -= vel
            isJump = True
    else:
        if jumpCount >= -10:
            y -= (jumpCount * abs(jumpCount)) * 0.5
            jumpCount -= 1
        else:
            #colision(Monstre,character)
            jumpCount = 10
            isJump = False



    screen.blit(background,(0,0))
    screen.blit(SLIME_ACTIVE, (character_x_pos, character_y_pos + y))
    
    
#boucle des mouvements du monstre 
    if Position==0: 
        if Monstre_x_pos != 1000:
            Monstre_x_pos += 10
            Monstre=MONSTRE_with_flip
        else:
            Position = 1
    if Position == 1:
        if Monstre_x_pos!=-10:
            Monstre_x_pos -= 10
            Monstre=Monstre_copy
        else:
            Position = 0
    screen.blit(Monstre, (Monstre_x_pos, Monstre_y_pos))
    
    
    
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'): # si la touche 'z' est pressé 
            print('You Pressed ECHAP Key!') 
            pygame.quit()
            actif = False
            
        #si la touche 'q' est appuier 
        if keyboard.is_pressed('d'):  
            if character_x_pos != Monstre_x_pos:
                character_x_pos=character_x_pos+10
            print(character_x_pos)
            SLIME_ACTIVE = SLIME_with_flip
        # si la touche 'q' est appuier 
        if keyboard.is_pressed('q'):
            if character_x_pos!=-10:
                character_x_pos=character_x_pos-10
                SLIME_ACTIVE = character
            
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete
    
 
    
    if (character_x_pos+character_width) <= (Monstre_x_pos+Monstre_width) and character_y_pos+character_width <= (Monstre_y_pos+Monstre_height):
        pygame.quit()
        actif = False 
    for event in pygame.event.get():  #prend chaque evenement de pygame 
        if event.type == pygame.QUIT: #je compare l'evenement pris
            actif = False            
            pygame.quit()
            
            
    pygame.display.update()
    


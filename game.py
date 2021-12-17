#importation des modules nécessaires
import pygame 
import keyboard  
import sys
import time

#création de la fenetre 
pygame.init() 

#dimension de la fenetre
screen_width = 2000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height)) 

#ajoute en plus
pygame.display.flip() 
clock = pygame.time.Clock()


#titre, background et icon
pygame.display.set_caption("Kirby") 
background = pygame.image.load('GRAPHISME\Background.png')
icon = pygame.image.load('GRAPHISME\BLOOBEY-logo.png')
pygame.display.set_icon(icon)


#création du personnage
character = pygame.image.load('GRAPHISME\BLOOBEY-logo.png')
character_size = (225,190)
character_width = character_size[0]
character_height = character_size[1]
character = pygame.transform.scale(character, (character_width, character_height))
character_x_pos = 0
character_y_pos = 600
plaform=(character_y_pos,0)


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

#la boucle:
while actif:  

    SLIME_copy = character.copy()
    SLIME_with_flip = pygame.transform.flip(SLIME_copy, True, False)
    
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
            jumpCount = 10
            isJump = False
            

    screen.blit(background,(0,0))
    screen.blit(SLIME_ACTIVE, (character_x_pos, character_y_pos + y))
    
    for event in pygame.event.get():  #prend chaque evenement de pygame 
        if event.type == pygame.QUIT: #je compare l'evenement pris
            actif = False
            pygame.quit()
            
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'): # si la touche 'z' est pressé 
            print('You Pressed ECHAP Key!') 
            pygame.quit()
            actif = False
            
        if keyboard.is_pressed('d'):  # si la touche 'q' est appuier 
            if character_x_pos!=10000:
                character_x_pos=character_x_pos+10
            SLIME_ACTIVE = SLIME_with_flip
            print(character_x_pos)
            
            
        if keyboard.is_pressed('q'):  # si la touche 'q' est appuier 
            if character_x_pos!=-10:
                character_x_pos=character_x_pos-10
            SLIME_ACTIVE = character
            print(character_x_pos)
            
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete
         
    
    pygame.display.update()
    


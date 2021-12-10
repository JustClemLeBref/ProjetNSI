#module import
import pygame 
import keyboard  
import sys

#creer une fenetre 
pygame.init() 

#dimension de la fenetre
screen_width = 1660
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height)) 

#ajoute en plus
pygame.display.flip() 
clock = pygame.time.Clock()

#titre et background et icon
pygame.display.set_caption("Kirby") 
icon = pygame.image.load(r'assert\icon.jpg')
pygame.display.set_icon(icon)
background = pygame.image.load(r"assert\bg.png")

#load personnage
character = pygame.image.load(r'assert\icon.jpg')
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = 0
character_y_pos = 0
#variable
actif = True 

#la loop
while actif:  # creer _une loop
    screen.blit(background,(0,0))
    screen.blit(character, (character_x_pos, character_y_pos))
    pygame.display.update()
    for event in pygame.event.get(): #prends chaque evenement de pygame 
        if event.type == pygame.QUIT: #je compars levenement pris
            pygame.quit()
            actif = False
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'):  # si la touche 'q' est appuier 
            print('You Pressed ECHAP Key!') 
            pygame.quit()
            actif = False
        if keyboard.is_pressed('d'):  # si la touche 'q' est appuier 
            if character_x_pos!=760:
                character_x_pos=character_x_pos+10
            print(character_x_pos)
        if keyboard.is_pressed('q'):  # si la touche 'q' est appuier 
            if character_x_pos!=-10:
                character_x_pos=character_x_pos-10
            print(character_x_pos)
        if keyboard.is_pressed('s'):  # si la touche 'q' est appuier 
            if character_y_pos!=60:
                character_y_pos=character_y_pos+10
            print(character_y_pos)
        if keyboard.is_pressed('z'):  # si la touche 'q' est appuier 
            if character_y_pos!=120:
                character_y_pos=character_y_pos-10
            print(character_y_pos)
    except:
        break  # if user pressed a key other than the given key the loop will break
    

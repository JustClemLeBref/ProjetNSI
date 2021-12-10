#module import
import pygame 
import keyboard  
import sys

#creer une fenetre 
pygame.init() 

#dimension de la fenetre
screen_width = 1440
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height)) 

#ajoute en plus
pygame.display.flip() 
clock = pygame.time.Clock()

#titre et background et icon
pygame.display.set_caption("Kirby") 
icon = pygame.image.load(r'U:\1ere\NSI\projet\icon.jpg')
pygame.display.set_icon(icon)
background = pygame.image.load(r"U:\1ere\NSI\projet\bg.png")

#variable
actif = True 

#la loop
while actif:  # creer _une loop
    screen.blit(background,(0,0))
    pygame.display.update()
    for event in pygame.event.get(): #prends chaque evenement de pygame 
        if event.type == pygame.QUIT: #je compars levenement pris
            pygame.quit()
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'):  # si la touche 'q' est appuier 
            print('You Pressed ECHAP Key!') 
            pygame.quit()
    except:
        break  # if user pressed a key other than the given key the loop will break
    

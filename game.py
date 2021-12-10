import pygame # utilise le module pygame
import keyboard  # utilise le module keyboard

pygame.init() #creer une fenetre 
screen = pygame.display.set_mode((720,500)) #dimension de la fentre
pygame.display.flip() #je flip la fenectre
pygame.display.set_caption("Kirby") #donne un nom en haut de la fenectre
actif = True #donne la valeur "true" a actif
while actif:  # creer _une loop
    for event in pygame.event.get(): #prends chaque evenement de pygame 
        if event.type == pygame.QUIT: #je compars levenement pris
            actif = False #donne la valeur "false" a actif
    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('q'):  # si la touche 'q' est appuier 
            print('You Pressed A Key!') 
            break  # termine la loop
 

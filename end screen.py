import pygame

import random
from pygame import mixer

class BUTTON(pygame.sprite.Sprite):
    def __init__(self,image,size):
        super().__init__()
        self.description = "default"
        self.image = pygame.transform.scale(pygame.image.load(image), (size[0], size[1]))
        self.rect = self.image.get_rect()
        self.x = 515
        self.y = 550
        
        self.clicked = False
        self.endresult = 0
    
    #variable du clickage de bouton
    def click(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos,self.rect)
                if self.rect.collidepoint(event.pos):
                    return True
    def update(self):
        self.rect.topleft = self.x, self.y


def endmenu():
    pygame.init() 
    
    
    white = (255, 255, 255) 
    
    X = 1400
    Y = 2500
    
    display_surface = pygame.display.set_mode((X, Y )) 
    
    pygame.display.set_caption('Image')   
    image =  pygame.image.load('.\\main_screen_images\\Background_Sized.png') 
    
    #def de la musique
    pygame.mixer.init()
    pygame.mixer.music.load('.\\end_screen_images\\end_song.ogg')
    pygame.mixer.music.play()
    
    
    #def position et importation bouton end
    image_end = '.\\end_screen_images\\the_end.png'
    end = BUTTON(image_end,(350,250))
    coordone_end=(515,575)
    end.x = coordone_end[0]
    end.y = coordone_end[1]
    end.endresult = 0
    
    
    #def position et importation star
    image_star = '.\\end_screen_images\\star.png'
    star = BUTTON(image_star,(10,10))
    coordone_star=(150,125)
    star.x = coordone_star[0]
    star.y = coordone_star[1]
    star.endresult = 0
    
    #def position et importation star2
    image_star2 = '.\\end_screen_images\\star2.png'
    star2 = BUTTON(image_star2,(10,10))
    coordone_star2=(1150,105)
    star2.x = coordone_star2[0]
    star2.y = coordone_star2[1]
    star2.endresult = 0
    
    
    #def position et importation  titre end
    image_Tend = '.\\end_screen_images\\Thanks_for_Playing-removebg-preview.png'
    Tend = BUTTON(image_Tend,(500,500))
    coordone_Tend=(440,50)
    Tend.x = coordone_Tend[0]
    Tend.y = coordone_Tend[1]
    Tend.endresult = 0
    
    
    BUTTONS = pygame.sprite.Group(end,star,Tend,star2)
    heart= False
    scary= False
    continuer = True
    while continuer :
        pygame.display.update() 
        event_list=pygame.event.get()
        display_surface.fill(white) 
        display_surface.blit(image, (0, 0))
        
        BUTTONS.update()
        BUTTONS.draw(display_surface)
        
        #paramètre du clickage star
        if star.click(event_list):
            heart=not(heart)
        if heart:
            heart_image = pygame.image.load('.\\end_screen_images\\heart1.png')
            display_surface.blit(heart_image, (825, 250))

        #paramètre du clickage star2
        if star2.click(event_list):
            scary=not(scary)
        if scary:
            scary_image = pygame.image.load('.\\end_screen_images\\scary.jpg')
            scary_image=pygame.transform.scale(scary_image, (500,500))
            display_surface.blit(scary_image, (500, 500))

            
        
        #paramètre du clickage end       
        if end.click(event_list):
            continuer=False
            pygame.quit() 
    
        for event in event_list : 
    
            if event.type == pygame.QUIT :
                continuer=False 
    
                pygame.quit() 
endmenu()
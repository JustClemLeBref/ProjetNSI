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


def mainmenu():
    pygame.init() 
    
    
    white = (255, 255, 255) 
    
    X = 1400
    Y = 1000
    
    display_surface = pygame.display.set_mode((X, Y )) 
    
    pygame.display.set_caption('Image')   
    image =  pygame.image.load('.\\main_screen_images\\Background_Sized.png') 
    
    #def de la musique
    pygame.mixer.init()
    pygame.mixer.music.load('.\\main_screen_images\\musique_fort_boyard.ogg')
    pygame.mixer.music.play()
    
    #def position et importation bouton play
    image_play = '.\\main_screen_images\\Play_button.png'
    play = BUTTON(image_play,(350,250))
    coordone_play=(515,575)
    play.x = coordone_play[0]
    play.y = coordone_play[1]
    play.endresult = 0
    
    #def position et importation monstre 
    image_monster = '.\\main_screen_images\\Monster.png'
    monster = BUTTON(image_monster,(250,400))
    coordone_monster=(150,470)
    monster.x = coordone_monster[0]
    monster.y = coordone_monster[1]
    monster.endresult = 0
    
    
    #def position et importation BLOOBEY
    image_bloobey = '.\\main_screen_images\\bloobey.png'
    bloobey = BUTTON(image_bloobey,(400,400))
    coordone_bloobey=(950,525)
    bloobey.x = coordone_bloobey[0]
    bloobey.y = coordone_bloobey[1]
    bloobey.endresult = 0
    
    
    #def position et importation  titre BLOOBEY
    image_Tbloobey = '.\\main_screen_images\\titre_Bloobey-removebg-preview(2).png'
    Tbloobey = BUTTON(image_Tbloobey,(1500,1500))
    coordone_Tbloobey=(-60,-600)
    Tbloobey.x = coordone_Tbloobey[0]
    Tbloobey.y = coordone_Tbloobey[1]
    Tbloobey.endresult = 0
    
    #def position et importation  icone settings
    image_icone_setting = '.\\main_screen_images\\setting_icon.png'
    Isetting = BUTTON(image_icone_setting,(100,100))
    coordone_Isetting=(0,0)
    Isetting.x = coordone_Isetting[0]
    Isetting.y = coordone_Isetting[1]
    Isetting.endresult = 0
    
    #def position et importation  icone info
    image_icone_info = '.\\main_screen_images\\icone_info.png'
    Iinfo = BUTTON(image_icone_info,(100,100))
    coordone_Iinfo=(1290,0)
    Iinfo.x = coordone_Iinfo[0]
    Iinfo.y = coordone_Iinfo[1]
    Iinfo.endresult = 0
    
    
    
    
    
    BUTTONS = pygame.sprite.Group(play,monster,bloobey,Tbloobey,Isetting,Iinfo)
    Imenu=False
    menu= False
    continuer = True
    while continuer :
        pygame.display.update() 
        event_list=pygame.event.get()
        display_surface.fill(white) 
        display_surface.blit(image, (0, 0))
        
        BUTTONS.update()
        BUTTONS.draw(display_surface)
        #paramètre du clickage settings
        if Isetting.click(event_list):
            menu=not(menu)
        if menu:
            menu_image = pygame.image.load('.\\main_screen_images\\setting2.png')
            display_surface.blit(menu_image, (525, 250))
        
        #paramètre du clickage info
        if Iinfo.click(event_list):
            Imenu=not(Imenu)
        if Imenu:
            Imenu_image = pygame.image.load('.\\main_screen_images\\image_info.png')
            display_surface.blit(Imenu_image, (175, 250))
    
        
        
        
         #paramètre du clickage play       
        if play.click(event_list):
            continuer=False
            pygame.quit() 
    
        for event in event_list : 
    
            if event.type == pygame.QUIT :
                continuer=False 
    
                pygame.quit() 
mainmenu()

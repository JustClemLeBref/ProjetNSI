
#importation des modules nécessaires
import pygame
from pygame import mixer
import random
import teste1

#dimension de la fenetre
screen_width = 1440
screen_height = 1000

#on ajoute en plus
clock = pygame.time.Clock()

Vert = (255, 255, 255)
rouge = (255, 0, 0)
noir = (0, 0, 0)

#classe du joueur, ses stats
class Player(pygame.sprite.Sprite):
    def __init__(self,image,size):
        super().__init__()
        self.description = "default"
        self.sprites = []
        self.sprites_flip = []
        self.is_animating = False
        for i in range(1,9):
            image="GRAPHISME\\Bloobey-anim\\idle\\BLOOBEY-logo(idle){}.png".format(i)
            image=pygame.image.load(image)
            self.image = pygame.transform.scale(image, (size[0], size[1]))
            self.original = self.image
            self.original_flip = pygame.transform.flip(self.image, True, False)
            self.sprites.append(self.original)
            self.sprites_flip.append(self.original_flip)
        
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        
        self.rect = self.image.get_rect()
        
        # On définit le vecteur vitesse du joueur
        self.change_x = 0
        self.change_y = 0 
        
        # Liste des sprites dans lesquels on peut rentrer dedans 
        self.level = None

        #Fonction pour mettre le joueur a jour apres chaque action
    def update(self):
        self.calc_grav()
        self.rect.topleft = self.rect.x, self.rect.y
        self.rect.x += self.change_x  # Pour bouger de droite à gauche 
        

        #Variable pour repérer les collisions avec pygame
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        
        for block in block_hit_list:
            #Si le joueur va à droite, on place sa droite à gauche de l'objet qu'il touche
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Si le joueur va à gauche, on fait l'inverse
                self.rect.left = block.rect.right
 
        #Variable pour bouger de haut en bas
        self.rect.y += self.change_y
        
       
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
 
            # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom
 
            #Si il y a une collision, on arrete le mouvement vers le haut ou le bas
            self.change_y = 0
        
        if self.is_animating == True:
            self.current_sprite += 0.2
            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                
            
            self.image = self.sprites[int(self.current_sprite)]
    
    def animate(self):
        self.is_animating = True
    
    #Fonction pour calculer la gravité appliqué au joueur ou au monstre  
    def calc_grav(self):
       
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .5
 
        #Condition pour voir si le joueur se situe au sol ou non
        if self.rect.y >= screen_height +300 and self.change_y >= 0: 
            self.change_y = 0
            self.rect.y = screen_height +300
 
#Fonction pour le saut du joueur
    def jump(self):
       
 
        #On vérifie les collions aux alentours du joueur
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2
 
        # Si le saut est possible, le joueur saute
        if len(platform_hit_list) > 0 or self.rect.bottom >= screen_height:
            self.change_y = -10
 
    # Controles du saut:
     #Flèche gauche
    def go_left(self):
        #Flèche gauche
        self.change_x = -6
 
    #Flèche droite
    def go_right(self):
       
        self.change_x = 6
 
    #si le joueur arrête d'appuyer sur une touche
    def stop(self):
        
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
        self.nombre_de_boucle = 0
    
    def update(self):
        self.rect.topleft = self.x, self.y

#Classe du bouton clickable (valable pour plusieurs boutons)
class BUTTON(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.description = "default"
        self.size = (100,100)
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size[0], self.size[1]))
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 640
        
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
        
        
 #Class de La Platforme où Bloobey saute       
class Platform(pygame.sprite.Sprite):
    
 
    def __init__(self, width, height,image):
        super().__init__()
        
        #image du block principale
        
        
        self.image = pygame.Surface([width, height])
        #self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        #self.image.fill(Vert)
 
        self.rect = self.image.get_rect()
        
#classe pour les Portes de fin de niveau
class Door(pygame.sprite.Sprite):
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

#Classe du Niveau 
class Level(object):
    
 
    def __init__(self, player):
        #Les collisions avec le joueur sont indispensables
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.Door = pygame.sprite.Group()
        self.player = player
        
        #Background
        self.background = None
 
    # On met à jour le niveau 
    def update(self):
       
        self.platform_list.update()
        self.enemy_list.update()
        self.Door.update()
    #Fonction pour ajouter le niveau à l'écran 
    def draw(self):
        
 
        
        # On ajoute tout à l'écran 
        self.platform_list.draw(Level.screen)
        self.enemy_list.draw(Level.screen)
        self.Door.draw(Level.screen)
 
#On crée les plateformes du niveau
class Level_1(Level):
    #Niveau 1
 
    def __init__(self,player):
        #Niveau 1 
        
        
        Level.__init__(self, player)
        
        # Call the parent constructor
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\SCubeShortD4.png'
        Spikes = 'GRAPHISME\\Cubes2\\SCubeShortD4.png'
        cube2 = 'GRAPHISME\\Cubes2\\SCubeLongD1.png'
        # Array with width, height, x, and y of platform
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        size=75
        height=0
        
        for line in level:
            height+=size
            print(height)
            length=0
            for object in line:
                print(object)
                if object == 1:
                    print(length)
                    block = Platform(size, size,cube1)
                    block.rect.x = length
                    block.rect.y = height
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door)
                    Door_obj.x = length
                    Door_obj.y = height
                    self.Door.add(Door_obj)
                if object == 2:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door)
                    Door_obj.x = length
                    Door_obj.y = height
                    self.Door.add(Door_obj)
                    
                length+=size
                
        Monsters = [['GRAPHISME/monstre_test.png', (150,150), (0,400)],]
        
        
        #On place les ennemis
        for ennemie in Monsters:
            monstre = Ennemie(ennemie[0])
            monstre.size = ennemie[1]
            coordone_monstre = ennemie[2]
            monstre.x = coordone_monstre[0]
            monstre.y = coordone_monstre[1]
            self.enemy_list.add(monstre)

            
    def update(self):
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update()
        self.enemy_list.update()
        self.Door.update()
        
    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)
 

class Level_2(Level):
    #On définit le niveau 2
 
    def __init__(self,player):
   
        Level.__init__(self, player)
        
        # Call the parent constructor
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\SCubeShortD4.png'
        cube2 = 'GRAPHISME\\Cubes2\\SCubeLongD1.png'
        # Array with width, height, x, and y of platform
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,1,1,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,0,0,0,0,0,1,1,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0],
        [1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        size=75
        height=0
        
        for line in level:
            height+=size
            print(height)
            length=0
            for object in line:
                print(object)
                if object == 1:
                    print(length)
                    block = Platform(size, size,cube1)
                    block.rect.x = length
                    block.rect.y = height
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door)
                    Door_obj.x = length
                    Door_obj.y = height
                    self.Door.add(Door_obj)
                    
                length+=size
                
        Monsters = [['GRAPHISME/monstre_test.png', (150,150), (0,400)],]
        
        
        #On place les ennemis
        for ennemie in Monsters:
            monstre = Ennemie(ennemie[0])
            monstre.size = ennemie[1]
            coordone_monstre = ennemie[2]
            monstre.x = coordone_monstre[0]
            monstre.y = coordone_monstre[1]
            self.enemy_list.add(monstre)
            
    def update(self):
        #On met à jour tout les objets, niveaux et entités créées
        self.platform_list.update()
        self.enemy_list.update()
        self.Door.update()
        
    def draw(self, screen):
        # cette fonction 'dessine' ou place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

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
    level_list.append( Level_1(SLIME_obj))
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
            if current_level_now <= len(level_list)-1:
                print(level_list)
                current_level_now += 1
                SLIME_obj.rect.x = coordone_SLIME_obj[0]
                SLIME_obj.rect.y = coordone_SLIME_obj[1]
            else:
                
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
   

teste1.mainmenu()
if teste1.mainmenu()==1:
    main()



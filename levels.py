#importation de la bibliiothèque pygame
import pygame
#code important du jeu qui définit tout ce qui est en rapport avec les niveaux
#comme le joueur, les ennemis, les plateformes, les collisions, les entités, et les niveaux

#dimension de la fenetre
screen_width = 1425
screen_height = 1000

#classe du joueur, ses stats
class Player(pygame.sprite.Sprite):
    def __init__(self,image,size):
        super().__init__()
        self.description = "default"
        self.sprites = []
        self.sprites_flip = []
        self.is_animating = False

        #boucle pour les animations, on cherche toutes les images de bloobey
        for i in range(1,9):
            image="GRAPHISME\\Bloobey-anim\\idle\\BLOOBEY-logo(idle){}.png".format(i)
            image=pygame.image.load(image)
            self.image = pygame.transform.scale(image, (size[0], size[1]))
            self.original = self.image
            self.original_flip = pygame.transform.flip(self.image, True, False)
            self.sprites.append(self.original)
            self.sprites_flip.append(self.original_flip)
        
        #on commence avec la première image
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.in_movement_screen = screen_width

        self.rect = self.image.get_rect()

        # On définit le vecteur vitesse du joueur
        self.change_x = 0
        self.change_y = 0
        self.speed = 6

        limit = 400
        # Liste des sprites dans lesquels on peut rentrer dedans
        self.level = None

        #Fonction pour mettre le joueur a jour apres chaque action
    def update(self):
        self.calc_grav()
        self.rect.topleft = self.rect.x, self.rect.y

        self.rect.x += self.change_x * self.speed  # Pour bouger de droite à gauche


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

            # reset la position du joueur après une collision (pour ne pas rentrer dans le bloc)
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
            if self.change_x <= 0:
                self.image = self.sprites[int(self.current_sprite)]
            if self.change_x >= 0:
                self.image = self.sprites_flip[int(self.current_sprite)]
    def animate(self):
        self.is_animating = True

    #Fonction pour calculer la gravité appliqué au joueur
    def calc_grav(self):

        #dimension de la fenetre
        screen_width = 1440
        screen_height = 1000

        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += 1

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
            self.change_y = -15

    # Controles du saut:
     #Flèche gauche
    def go_left(self):
        #Flèche gauche
        self.change_x = -1

    #Flèche droite
    def go_right(self):

        self.change_x = 1

    #si le joueur arrête d'appuyer sur une touche
    def stop(self):
        self.change_x = 0


#classe pour les ennemies, les pics
class Ennemie(pygame.sprite.Sprite):
    def __init__(self,image,x,y,size):
        super().__init__()
        self.description = "default"
        self.size = size
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size[0], self.size[1]))
        self.original = self.image
        self.original_flip = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    
    #on update les pics après chaque action
    def update(self,x_shift):
        self.rect.topleft = self.rect.x, self.rect.y
        self.rect.x += x_shift

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
                if self.rect.collidepoint(event.pos):
                    return True
    def update(self):
        self.rect.topleft = self.x, self.y


 #Class de La Platforme où Bloobey saute
class Platform(pygame.sprite.Sprite):


    def __init__(self, width, height,image,x,y):
        super().__init__()

        #image du block principale


        self.image = pygame.Surface([width, height])
        self.image = pygame.transform.scale(pygame.image.load(image), (width, height))
        #coordonnées de la plateforme
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self,x_shift):
        self.rect.topleft = self.rect.x, self.rect.y
        self.rect.x += x_shift

#classe pour les fruits portails de fin de niveau
class Door(pygame.sprite.Sprite):
    def __init__(self,image,x,y):
        super().__init__()
        self.description = "default"
        self.size = (75,75)
        self.image = pygame.transform.scale(pygame.image.load(image), (self.size[0], self.size[1]))
        self.original = self.image
        self.original_flip = pygame.transform.flip(self.image, True, False)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0

    def update(self,x_shift):
        self.rect.topleft = self.rect.x, self.rect.y
        self.rect.x += x_shift


#classe des niveaux en général
class Level(object):


    def __init__(self, player):
        #Les collisions avec le joueur sont indispensables
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.Door = pygame.sprite.Group()
        self.player = player
        self.x_shift = 0
        #Background
        self.background = None
    # On met à jour le niveau
    def update(self):

        self.platform_list.update(self.x_shift)
        self.enemy_list.update(self.x_shift)
        self.Door.update(self.x_shift)
    #Fonction pour ajouter le niveau à l'écran
    def draw(self):

        # On ajoute tout à l'écran
        self.platform_list.draw(Level.screen)
        self.enemy_list.draw(Level.screen)
        self.Door.draw(Level.screen)


#On crée les plateformes du niveau
#classe pour le premier niveau, et tout de même pour ceux qui suivent
class Level_1(Level):
   

    def __init__(self,player):
        #Niveau 1


        Level.__init__(self, player)

        # on définit tout les blocs dont on aura besoin
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube2 = 'GRAPHISME\\Cubes2\\invisible.png'
        cube3 = 'GRAPHISME\\Cubes2\\Cubes12.png'
        cube4 = 'GRAPHISME\\Cubes2\\Cubes13.png'
        cube5 = 'GRAPHISME\\Cubes2\\Cubes14.png'
        cube6 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube7 = 'GRAPHISME\\Cubes2\\Cubes8.png'
        cube8 = 'GRAPHISME\\Cubes2\\Cubes9.png'
        cube9 = 'GRAPHISME\\Cubes2\\Cubes10.png'
        cube10 = 'GRAPHISME\\Cubes2\\Cubes11.png'
        # liste de liste représentant les coordonnées des blocs, des fruits et des pics
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,3,4,4,4,4,4,5,0,0,3,4,4,4,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        size=75
        y=0
        #pour chaque numéro on ajoute le bloc en question dans le niveau avec ses coordonnées
        for line in level:
            y+=size
            x=0
            for object in line:
                if object == 1:
                    block = Platform(size,size,cube1,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    block = Platform(size,size,cube2,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 3:
                    block = Platform(size,size,cube3,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 4:
                    block = Platform(size,size,cube4,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 5:
                    block = Platform(size,size,cube5,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 6:
                    block = Platform(size,size,cube6,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 7:
                    block = Platform(size,size,cube7,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 8:
                    block = Platform(size,size,cube8,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 9:
                    block = Platform(size,size,cube9,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 10:
                    block = Platform(size,size,cube10,x,y)
                    block.player = self.player
                    self.platform_list.add(block)

                if object == 15:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door,x,y)
                    self.Door.add(Door_obj)

                if object == 16:
                    spikes='GRAPHISME\\Spikes.png'
                    monstre = Ennemie(spikes,x,y,(size,size))
                    self.enemy_list.add(monstre)

                x+=size

        self.x_worldshift = 0
        self.total = 0

    def update(self):
        self.total -= self.x_worldshift
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update(self.x_worldshift)
        self.enemy_list.update(self.x_worldshift)
        self.Door.update(self.x_worldshift)

    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

    def startover(self):
        self.x_worldshift = self.total
    
    #fonction du scolling, c'est-à-dire l'effet caméra centrer sur le joueur.
    #si le joueur atteint une certaine abcisse x, sa vitesse vaut 0 et les plateformes bougent avec la même vitesse dans le côté opposé, qui donne un effet caméra.
    def scroll(self):
        player_x = self.player.rect.centerx
        if player_x < screen_width / 4 and self.player.change_x < 0:
            self.x_worldshift = 6
            self.player.speed = 0

        elif player_x >  screen_width - screen_width / 4 and self.player.change_x > 0:
            self.x_worldshift = -6
            self.player.speed = 0
        else:
            self.x_worldshift = 0
            self.player.speed=6

# pareille que la classe Level_1
class Level_2(Level):
    #On définit le niveau 2

    def __init__(self,player):
        #Niveau 2


        Level.__init__(self, player)

        # 
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube2 = 'GRAPHISME\\Cubes2\\invisible.png'
        cube3 = 'GRAPHISME\\Cubes2\\Cubes12.png'
        cube4 = 'GRAPHISME\\Cubes2\\Cubes13.png'
        cube5 = 'GRAPHISME\\Cubes2\\Cubes14.png'
        cube6 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube7 = 'GRAPHISME\\Cubes2\\Cubes8.png'
        cube8 = 'GRAPHISME\\Cubes2\\Cubes9.png'
        cube9 = 'GRAPHISME\\Cubes2\\Cubes10.png'
        cube10 = 'GRAPHISME\\Cubes2\\Cubes11.png'
        #liste de liste représentant les coordonnées des blocs, des fruits et des pics
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,15,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,5,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,3,4,4,4,4,4,4,4,5,0,0,3,4,5,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        size=75
        y=0

        for line in level:
            y+=size
            x=0
            for object in line:
                if object == 1:
                    block = Platform(size,size,cube1,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    block = Platform(size,size,cube2,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 3:
                    block = Platform(size,size,cube3,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 4:
                    block = Platform(size,size,cube4,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 5:
                    block = Platform(size,size,cube5,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 6:
                    block = Platform(size,size,cube6,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 7:
                    block = Platform(size,size,cube7,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 8:
                    block = Platform(size,size,cube8,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 9:
                    block = Platform(size,size,cube9,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 10:
                    block = Platform(size,size,cube10,x,y)
                    block.player = self.player
                    self.platform_list.add(block)

                if object == 15:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door,x,y)
                    self.Door.add(Door_obj)

                if object == 16:
                    spikes='GRAPHISME\\Spikes.png'
                    monstre = Ennemie(spikes,x,y,(size,size))
                    self.enemy_list.add(monstre)


                x+=size
        self.x_worldshift = 0
        self.total = 0

    def update(self):
        self.total -= self.x_worldshift
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update(self.x_worldshift)
        self.enemy_list.update(self.x_worldshift)
        self.Door.update(self.x_worldshift)

    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

    def startover(self):
        self.x_worldshift = self.total

    def scroll(self):
        player_x = self.player.rect.centerx

        if player_x < screen_width / 4 and self.player.change_x < 0:
            self.x_worldshift = 6
            self.player.speed = 0

        elif player_x >  screen_width - screen_width / 4 and self.player.change_x > 0:
            self.x_worldshift = -6
            self.player.speed = 0

        else:
            self.x_worldshift = 0
            self.player.speed=6
            
            
# pareille que la classe Level_1
class Level_3(Level):
    #On définit le niveau 3

    def __init__(self,player):
        #Niveau 3


        Level.__init__(self, player)

        
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube2 = 'GRAPHISME\\Cubes2\\invisible.png'
        cube3 = 'GRAPHISME\\Cubes2\\Cubes12.png'
        cube4 = 'GRAPHISME\\Cubes2\\Cubes13.png'
        cube5 = 'GRAPHISME\\Cubes2\\Cubes14.png'
        cube6 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube7 = 'GRAPHISME\\Cubes2\\Cubes8.png'
        cube8 = 'GRAPHISME\\Cubes2\\Cubes9.png'
        cube9 = 'GRAPHISME\\Cubes2\\Cubes10.png'
        cube10 = 'GRAPHISME\\Cubes2\\Cubes11.png'
        # liste de liste représentant les coordonnées des blocs, des fruits et des pics
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,5,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,0,0,0,0,0,15,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,8,0,0,9,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,8,0,0,9,0,0,9,0,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,3,4,4,5,0,0,10,0,0,10,0,0,10,0,0,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        ]
        size=75
        y=0

        for line in level:
            y+=size
            x=0
            for object in line:
                if object == 1:
                    block = Platform(size,size,cube1,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    block = Platform(size,size,cube2,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 3:
                    block = Platform(size,size,cube3,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 4:
                    block = Platform(size,size,cube4,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 5:
                    block = Platform(size,size,cube5,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 6:
                    block = Platform(size,size,cube6,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 7:
                    block = Platform(size,size,cube7,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 8:
                    block = Platform(size,size,cube8,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 9:
                    block = Platform(size,size,cube9,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 10:
                    block = Platform(size,size,cube10,x,y)
                    block.player = self.player
                    self.platform_list.add(block)

                if object == 15:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door,x,y)
                    self.Door.add(Door_obj)

                if object == 16:
                    spikes='GRAPHISME\\Spikes.png'
                    monstre = Ennemie(spikes,x,y,(size,size))
                    self.enemy_list.add(monstre)

                x+=size


        self.x_worldshift = 0
        self.total = 0



    def update(self):
        self.total -= self.x_worldshift
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update(self.x_worldshift)
        self.enemy_list.update(self.x_worldshift)
        self.Door.update(self.x_worldshift)

    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

    def startover(self):
        self.x_worldshift = self.total

    def scroll(self):
        player_x = self.player.rect.centerx

        if player_x < screen_width / 4 and self.player.change_x < 0:
            self.x_worldshift = 6
            self.player.speed = 0

        elif player_x >  screen_width - screen_width / 4 and self.player.change_x > 0:
            self.x_worldshift = -6
            self.player.speed = 0

        else:
            self.x_worldshift = 0
            self.player.speed=6


# pareille que la classe Level_1
class Level_4(Level):
    #On définit le niveau 4

    def __init__(self,player):
        #Niveau 4


        Level.__init__(self, player)

       
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube2 = 'GRAPHISME\\Cubes2\\invisible.png'
        cube3 = 'GRAPHISME\\Cubes2\\Cubes12.png'
        cube4 = 'GRAPHISME\\Cubes2\\Cubes13.png'
        cube5 = 'GRAPHISME\\Cubes2\\Cubes14.png'
        cube6 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube7 = 'GRAPHISME\\Cubes2\\Cubes8.png'
        cube8 = 'GRAPHISME\\Cubes2\\Cubes9.png'
        cube9 = 'GRAPHISME\\Cubes2\\Cubes10.png'
        cube10 = 'GRAPHISME\\Cubes2\\Cubes11.png'
        # liste de liste représentant les coordonnées des blocs, des fruits et des pics
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,4,4,4,5,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,3,5,0,0,0,0,0,0,0,0,0,0,0,0,15,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,3,4,5,0,0,0,0,0,16,16,16,16,16,16,16,16,16,16,0,0,0,0,0,0,0,0],
        [0,3,4,4,5,0,0,0,0,0,3,4,4,4,4,4,4,4,4,4,4,4,4,5,0,0,0,0,0,0,0],
        ]
        size=75
        y=0

        for line in level:
            y+=size
            x=0
            for object in line:
                if object == 1:
                    block = Platform(size,size,cube1,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    block = Platform(size,size,cube2,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 3:
                    block = Platform(size,size,cube3,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 4:
                    block = Platform(size,size,cube4,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 5:
                    block = Platform(size,size,cube5,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 6:
                    block = Platform(size,size,cube6,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 7:
                    block = Platform(size,size,cube7,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 8:
                    block = Platform(size,size,cube8,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 9:
                    block = Platform(size,size,cube9,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 10:
                    block = Platform(size,size,cube10,x,y)
                    block.player = self.player
                    self.platform_list.add(block)

                if object == 15:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door,x,y)
                    self.Door.add(Door_obj)

                if object == 16:
                    spikes='GRAPHISME\\Spikes.png'
                    monstre = Ennemie(spikes,x,y,(size,size))
                    self.enemy_list.add(monstre)

                x+=size


        self.x_worldshift = 0
        self.total = 0



    def update(self):
        self.total -= self.x_worldshift
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update(self.x_worldshift)
        self.enemy_list.update(self.x_worldshift)
        self.Door.update(self.x_worldshift)

    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

    def startover(self):
        self.x_worldshift = self.total

    def scroll(self):
        player_x = self.player.rect.centerx

        if player_x < screen_width / 4 and self.player.change_x < 0:
            self.x_worldshift = 6
            self.player.speed = 0

        elif player_x >  screen_width - screen_width / 4 and self.player.change_x > 0:
            self.x_worldshift = -6
            self.player.speed = 0

        else:
            self.x_worldshift = 0
            self.player.speed=6

# pareille que la classe Level_1
class Level_5(Level):
    #On définit le niveau 5

    def __init__(self,player):
        #Niveau 5


        Level.__init__(self, player)

        
        Level.__init__(self, player)
        player=player
        self.platform_list = pygame.sprite.Group()
        cube1 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube2 = 'GRAPHISME\\Cubes2\\invisible.png'
        cube3 = 'GRAPHISME\\Cubes2\\Cubes12.png'
        cube4 = 'GRAPHISME\\Cubes2\\Cubes13.png'
        cube5 = 'GRAPHISME\\Cubes2\\Cubes14.png'
        cube6 = 'GRAPHISME\\Cubes2\\Cubes2.png'
        cube7 = 'GRAPHISME\\Cubes2\\Cubes8.png'
        cube8 = 'GRAPHISME\\Cubes2\\Cubes9.png'
        cube9 = 'GRAPHISME\\Cubes2\\Cubes10.png'
        cube10 = 'GRAPHISME\\Cubes2\\Cubes11.png'
        #liste de liste représentant les coordonnées des blocs, des fruits et des pics
        level=[
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0],
        [2,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,0,0,0,15],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,8,0,0,9,0,0,16,16,16,0],
        [2,0,0,0,0,0,0,0,0,0,0,0,0,3,5,0,0,3,5,0,0,9,0,0,9,0,3,4,4,4,5],
        [2,0,0,0,0,0,0,0,3,4,5,0,0,0,0,16,16,0,0,0,0,9,0,0,9,0,0,0,0,0,0],
        [2,0,0,0,0,3,4,5,0,0,0,16,16,0,3,4,4,5,0,16,0,9,0,0,9,0,0,0,0,0,0],
        [2,3,4,4,5,0,0,0,0,0,3,4,4,5,0,0,0,3,4,4,5,10,0,0,10,0,0,0,0,0,0],
        ]
        size=75
        y=0

        for line in level:
            y+=size
            x=0
            for object in line:
                if object == 1:
                    block = Platform(size,size,cube1,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 2:
                    block = Platform(size,size,cube2,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 3:
                    block = Platform(size,size,cube3,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 4:
                    block = Platform(size,size,cube4,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 5:
                    block = Platform(size,size,cube5,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 6:
                    block = Platform(size,size,cube6,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 7:
                    block = Platform(size,size,cube7,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 8:
                    block = Platform(size,size,cube8,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 9:
                    block = Platform(size,size,cube9,x,y)
                    block.player = self.player
                    self.platform_list.add(block)
                if object == 10:
                    block = Platform(size,size,cube10,x,y)
                    block.player = self.player
                    self.platform_list.add(block)

                if object == 15:
                    door = 'GRAPHISME\\Fruit.png'
                    Door_obj = Door(door,x,y)
                    self.Door.add(Door_obj)

                if object == 16:
                    spikes='GRAPHISME\\Spikes.png'
                    monstre = Ennemie(spikes,x,y,(size,size))
                    self.enemy_list.add(monstre)

                x+=size


        self.x_worldshift = 0
        self.total = 0



    def update(self):
        self.total -= self.x_worldshift
        #on update tout les objets, niveaux et entités créées
        self.platform_list.update(self.x_worldshift)
        self.enemy_list.update(self.x_worldshift)
        self.Door.update(self.x_worldshift)

    def draw(self, screen):
        # On place tout les objets, niveaux et entités créées
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)
        self.Door.draw(screen)

    def startover(self):
        self.x_worldshift = self.total

    def scroll(self):
        player_x = self.player.rect.centerx

        if player_x < screen_width / 4 and self.player.change_x < 0:
            self.x_worldshift = 6
            self.player.speed = 0

        elif player_x >  screen_width - screen_width / 4 and self.player.change_x > 0:
            self.x_worldshift = -6
            self.player.speed = 0

        else:
            self.x_worldshift = 0
            self.player.speed=6





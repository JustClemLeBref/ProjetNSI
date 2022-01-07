import sys
import random
import pygame


pygame.init()
screen = pygame.display.set_mode((800, 800))


class Macaco(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('.\\GRAPHISME\\bloobey-logo.png')
        self.rect = self.image.get_rect()
        self.x = 300
        self.y = 640
        self.speed = 20

    def keyboard(self, keys):
        if keys[pygame.K_RIGHT]:
            self.x += self.speed
        elif keys[pygame.K_LEFT]:
            self.x -= self.speed

    def update(self):
        self.rect.topleft = self.x, self.y


class Banana(pygame.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((230, 230, 40))
        self.rect = self.image.get_rect()
        self.x = random.randrange(0, 770)
        self.y = -50
        self.speed = 5

    def update(self):
        self.y += self.speed
        self.rect.topleft = self.x, self.y


macaco = Macaco()
banana = Banana()

all_sprites = pygame.sprite.Group(banana, macaco)
bananas = pygame.sprite.Group(macaco)

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    try:  # used try so that if user pressed other than the given key error will not be shown
        if keyboard.is_pressed('ESC'): # si la touche 'z' est pressé
            print('You Pressed ECHAP Key!')
            running = False

        #si la touche 'q' est appuier
        if keyboard.is_pressed('d'):
            if macaco.x != 1000:
                macaco.x=macaco.x+10
        # si la touche 'q' est appuier
        if keyboard.is_pressed('q'):
            if macaco.x!=-10:
                macaco.x=macaco.x-10
    except:
        break  # si l'utilisateur appuie sur une autre touche, la boucle s'arrete


    all_sprites.update()
    # Collision detection. Check if macaco collided with bananas group,
    # return collided bananas as a list. dokill argument is True, so
    # that collided bananas will be deleted.
    collided_bananas = pygame.sprite.spritecollide(banana, bananas, True)
    for collided_banana in collided_bananas:
        print('Collision.')
    screen.fill((70, 40, 70))
    all_sprites.draw(screen)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

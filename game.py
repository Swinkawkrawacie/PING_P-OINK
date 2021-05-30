import pygame
import pygame_menu
from pygame.locals import *
import os.path

#easy: normal ping-pong
#medium: changing sizes of piglet
#hard: more piglets
#single mode???

screen_size = (800, 600)

#funkcje
def get_image(name, color = False):
    image = pygame.image.load(os.path.join('DATA', name))
    image = image.convert()
    if color == True:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image

#klasy
class Piglet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("pig.png",True)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_size[0]/2,screen_size[1]/2)
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > screen_size[0]:
            self.rect.right = screen_size[0]

        if self.rect.top <= screen_size[1]/2:
            self.rect.top = screen_size[1]/2
        elif self.rect.bottom >= screen_size[1]:
            self.rect.bottom = screen_size[1]

class Bar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("bar2.png")
        self.rect = self.image.get_rect()
        self.rect.center = (24*screen_size[0]/25,screen_size[1])
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_size[1]:
            self.rect.bottom = screen_size[1]
    
    def change_pos(self, width, height):
        self.rect.center = (width, height)

#gra

def game():
    screen = pygame.display.set_mode(screen_size) 
    pygame.display.set_caption("Ping P-oink!")

    background = get_image("oink.png")
    screen.blit(background,(0,0))

    piglet_sprite = pygame.sprite.RenderClear() 
    piglet = Piglet()
    piglet_sprite.add(piglet)

    bar_sprite = pygame.sprite.RenderClear() 
    bar_right = Bar()
    bar_left = Bar()
    bar_left.rect.center = (1*screen_size[0]/25,screen_size[1])
    bar_sprite.add(bar_right)
    bar_sprite.add(bar_left)

    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                elif event.key == K_w:
                    bar_left.y_velocity = -4
                elif event.key == K_s:
                    bar_left.y_velocity = 4
                elif event.key == K_UP:
                    bar_right.y_velocity = -4
                elif event.key == K_DOWN:
                    bar_right.y_velocity = 4
            elif event.type == KEYUP:
                if event.key == K_w:
                    bar_left.y_velocity = 0 
                elif event.key == K_s:
                    bar_left.y_velocity = 0
                elif event.key == K_UP:
                    bar_right.y_velocity = 0
                elif event.key == K_DOWN:
                    bar_right.y_velocity = 0

        #piglet_sprite.update()
        #piglet_sprite.clear(screen, background)
        #piglet_sprite.draw(screen)
        bar_sprite.update()
        bar_sprite.clear(screen, background)
        bar_sprite.draw(screen)
        piglet_sprite.draw(screen)

        
        pygame.display.flip()
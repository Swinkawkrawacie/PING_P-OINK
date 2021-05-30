import pygame
import pygame_menu
from pygame.locals import *
import os.path
from random import randint

#easy: normal ping-pong
#medium: changing sizes of piglet
#hard: more piglets
#single mode???


#---------------------------------------------------------------------
#                           FUNCTIONS
#---------------------------------------------------------------------

def get_image(name, color = False):
    image = pygame.image.load(os.path.join('DATA', name))
    image = image.convert()
    if color == True:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image

def get_sound(name):
    fullname = os.path.join("DATA",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

#---------------------------------------------------------------------
#                            PIGLET
#---------------------------------------------------------------------

class Piglet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("pig.png",True)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_size[0]/2,screen_size[1]/2)
        self.x_velocity = 6
        self.y_velocity = randint(-8,8)

    def update(self):
        self.rect.move_ip((self.x_velocity,self.y_velocity))

    def hit(self):
        self.x_velocity = -self.x_velocity
        self.y_velocity = randint(-8,8)

#---------------------------------------------------------------------
#                              BAR
#---------------------------------------------------------------------

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
    
#---------------------------------------------------------------------
#                           SCORE BOARD
#---------------------------------------------------------------------

class ScoreBoard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.points = 0
        self.wins = 0
        self.text = "Points: "+str(self.points)+"\n Wins: "+str(self.wins)
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()

    def update(self):
        self.text = "Points: "+str(self.points)+"\n Wins: "+str(self.wins)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()

#---------------------------------------------------------------------
#                               GAME
#---------------------------------------------------------------------

def game():

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
    score_sprite = pygame.sprite.RenderClear()
    score_left = ScoreBoard()
    score_right = ScoreBoard()
    score_right.rect.center = (20*screen_size[0]/25,30)
    score_sprite.add(score_left)
    score_sprite.add(score_right)
    score_sprite.draw(screen)
    pygame.display.flip()

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
                    bar_left.y_velocity = -8
                elif event.key == K_s:
                    bar_left.y_velocity = 8
                elif event.key == K_UP:
                    bar_right.y_velocity = -8
                elif event.key == K_DOWN:
                    bar_right.y_velocity = 8
            elif event.type == KEYUP:
                if event.key == K_w:
                    bar_left.y_velocity = 0 
                elif event.key == K_s:
                    bar_left.y_velocity = 0
                elif event.key == K_UP:
                    bar_right.y_velocity = 0
                elif event.key == K_DOWN:
                    bar_right.y_velocity = 0
            
        piglet_sprite.update()
        bar_sprite.update()

        if piglet.rect.x>=screen_size[0]-10: #right
            wolf.play()
            score_left.wins += 1
            score_right.points = 0
            score_sprite.update()
            score_right.rect.center = (20*screen_size[0]/25,30)
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.rect.center = (screen_size[0]/2,screen_size[1]/2)
            piglet.x_velocity = 6
            piglet.y_velocity = randint(-8,8)
        if piglet.rect.x<=0: #left
            wolf.play()
            score_right.wins += 1
            score_left.points = 0
            score_sprite.update()
            score_right.rect.center = (20*screen_size[0]/25,30)
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.rect.center = (screen_size[0]/2,screen_size[1]/2)
            piglet.x_velocity = -6
            piglet.y_velocity = randint(-8,8)
            piglet.x_velocity = -piglet.x_velocity
        if piglet.rect.y>screen_size[1]-30: #down
            piglet.y_velocity = -piglet.y_velocity
        if piglet.rect.y<=0: #up
            piglet.y_velocity = -piglet.y_velocity 

        if pygame.sprite.collide_mask(piglet, bar_left):
            oink.play()
            score_left.points += 1
            score_sprite.update()
            score_right.rect.center = (20*screen_size[0]/25,30)
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.hit()
        
        if pygame.sprite.collide_mask(piglet, bar_right):
            oink.play()
            score_right.points += 1 
            score_sprite.update()
            score_right.rect.center = (20*screen_size[0]/25,30)
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.hit()
            
        
        piglet_sprite.clear(screen, background)
        bar_sprite.clear(screen, background)
        score_sprite.clear(screen, background)
        piglet_sprite.draw(screen)
        bar_sprite.draw(screen)
        score_sprite.draw(screen)
        
        
        pygame.display.flip()

#---------------------------------------------------------------------
#                       DIFFICULTY LEVELS
#---------------------------------------------------------------------

def set_difficulty():
    pass

#---------------------------------------------------------------------
#                         WINDOW AND MENU
#---------------------------------------------------------------------

screen_size = (800, 600)
pygame.init()
screen = pygame.display.set_mode(screen_size) 
pygame.display.set_caption("Ping P-oink!")
background = get_image("oink.png")
screen.blit(background,(0,0))
oink = get_sound("oink.wav")
wolf = get_sound("wolf.wav")

menu = pygame_menu.Menu(300, 400, 'Welcome',
                       theme=pygame_menu.themes.THEME_BLUE)

menu.add.text_input('Name :', default='Gracz')
menu.add.selector('Difficulty :', [('Hard', 1), ('Easy', 2)], onchange=set_difficulty)
menu.add.button('Play', game)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
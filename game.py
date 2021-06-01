from genericpath import isdir
from typing_extensions import runtime
import pygame
import pygame_menu
from pygame.locals import *
import os.path
from random import randint
import time


#---------------------------------------------------------------------
#                           FUNCTIONS
#---------------------------------------------------------------------

def get_image(name:str, color:bool = False):
    """
    Get image from a given file name

    @param name: (str) name of the image file
    @param color: (bool) information if the background of the image should be transparent (default = False)
    @return: (pygame.Surface) requested image
    @raise TypeError: if type of given data is incorrect
    @raise ValueError: if value of given data is incorrect
    """
    if not (isinstance(name, str) and isinstance(color, bool)):
        raise TypeError
    if not os.path.exists('DATA/'+name):
        raise ValueError

    image = pygame.image.load(os.path.join('DATA', name))
    image = image.convert()
    if color == True:
        colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey,RLEACCEL)
    return image

def get_sound(name:str):
    """
    Get sound from a given file name

    @param name: (str) name of the sound file
    @return: (Sound) requested image
    @raise TypeError: if type of given data is incorrect
    @raise ValueError: if value of given data is incorrect
    """
    if not isinstance(name, str):
        raise TypeError
    if not os.path.exists('DATA/'+name):
        raise ValueError

    fullname = os.path.join("DATA",name)
    sound = pygame.mixer.Sound(fullname)
    return sound

def write_to_file(data:list):
    """
    Write new data to score_table.txt

    @param data: (list) list of data to write into the file
    @raise TypeError: of type of given data is incorrect
    """
    if not isinstance(data, list):
        raise TypeError

    with open('score_table.txt', 'w+') as table_file:
        table_file.write(str(data))

#---------------------------------------------------------------------
#                            PIGLET
#---------------------------------------------------------------------

class Piglet(pygame.sprite.Sprite):
    """
    Creation of a piglet
    """
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image(pic_name,True)
        self.rect = self.image.get_rect()
        self.rect.center = (screen_size[0]/2,screen_size[1]/2)
        self.x_velocity = 6
        self.y_velocity = randint(-8,8)

    def update(self):
        """
        Move the piglet
        """
        self.rect.move_ip((self.x_velocity,self.y_velocity))

    def hit(self):
        """
        Change the direction of the piglet's movement
        """
        self.x_velocity = -self.x_velocity
        self.y_velocity = randint(-8,8)

#---------------------------------------------------------------------
#                              BAR
#---------------------------------------------------------------------

class Bar(pygame.sprite.Sprite):
    """
    Creation of a paddles
    """
    def __init__(self, place):
        pygame.sprite.Sprite.__init__(self)
        self.place = place
        self.image = get_image(bar_pic)
        self.hits = 0
        self.rect = self.image.get_rect()
        self.rect.center = self.place
        self.x_velocity = 0
        self.y_velocity = 0

    def update(self):
        """
        Move the paddle
        """
        self.rect.move_ip((self.x_velocity,self.y_velocity))

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom >= screen_size[1]:
            self.rect.bottom = screen_size[1]

#---------------------------------------------------------------------
#                           SCORE BOARD
#---------------------------------------------------------------------

class ScoreBoard(pygame.sprite.Sprite):
    """
    Creation of a scoreboard
    """
    def __init__(self, name:str, place:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.name = name
        self.place = place
        self.maxpoints = 0
        self.points = 0
        self.text = self.name+": "+str(self.maxpoints)
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = self.place


    def update(self):
        """
        Update results on the scoreboard
        """
        if self.points > self.maxpoints:
            self.maxpoints = self.points
        self.text = self.name+": "+str(self.maxpoints)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = self.place

#---------------------------------------------------------------------
#                         COUNTING LIVES
#---------------------------------------------------------------------

class Lives(pygame.sprite.Sprite):
    """
    Creation of a live counter
    """
    def __init__(self, place:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.place = place
        self.maxpoints = 0
        self.points = 0
        self.lives = 5
        self.image = get_image("heart"+str(self.lives)+".png", True)
        self.rect = self.image.get_rect()
        self.rect.center = self.place

    def update(self):
        """
        Change the amount of the hearts on the live counter
        """
        if self.lives <= 0:
            self.text = "You've lost"
            self.font = pygame.font.SysFont(None,50)
            self.image = self.font.render(self.text,1,(255,255,255))
            self.rect = self.image.get_rect()
            self.rect.center = self.place
        else:
            self.image = get_image("heart"+str(self.lives)+".png", True)
            self.rect = self.image.get_rect()
            self.rect.center = self.place

#---------------------------------------------------------------------
#                            GAME OVER
#---------------------------------------------------------------------
#DELETE
class Game_over(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image("game_over.png")
        self.rect = self.image.get_rect()
        self.rect.center = (screen_size[0]/2,screen_size[1]/2)

#---------------------------------------------------------------------
#                           BEST SCORES
#---------------------------------------------------------------------

class BestScores(pygame.sprite.Sprite):
    """
    Creation of a best scores list
    """
    def __init__(self, number:int, score:list, place:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.number = number
        self.score = score
        self.place = place
        if score[1] == 0:
            self.text = str(self.number+1)+'. NO DATA'
        else:
            self.text = str(self.number+1)+'. '+score[0]+' - '+str(score[1])+'p'
        self.font = pygame.font.SysFont(None,50)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = self.place

#---------------------------------------------------------------------
#                       ABOUT THE AUTHOR
#---------------------------------------------------------------------

class Show_text(pygame.sprite.Sprite):
    """
    Preparation for displaying a text
    """
    def __init__(self, type_text:str, place:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.text = type_text
        self.font = pygame.font.SysFont(None,30)
        self.image = self.font.render(self.text,1,(255,255,255))
        self.rect = self.image.get_rect()
        self.rect.center = place

class Show_picture(pygame.sprite.Sprite):
    """
    Preparation for displaying a picture
    """
    def __init__(self, picture, place:tuple):
        pygame.sprite.Sprite.__init__(self)
        self.image = get_image(picture)
        self.rect = self.image.get_rect()
        self.rect.center = place

#---------------------------------------------------------------------
#                               GAME
#---------------------------------------------------------------------

def game():
    """
    Display of the game
    """
    # executing options
    background = get_image(background_name)
    screen.blit(background,(0,0))
    if pic_name == "pig.png":
        animal_sound = get_sound("oink.wav")
    elif pic_name == "duck.png":
        animal_sound = get_sound("kwak.wav")
    else:
        animal_sound = get_sound("mee.wav")
    screen.blit(background,(0,0))

    # creating sprites
    piglet_sprite = pygame.sprite.RenderClear() 
    piglet = Piglet()
    piglet_sprite.add(piglet)

    bar_sprite = pygame.sprite.RenderClear() 
    bar_right = Bar((24*screen_size[0]/25,screen_size[1]))
    bar_left = Bar((1*screen_size[0]/25,screen_size[1]))
    bar_sprite.add(bar_right)
    bar_sprite.add(bar_left)

    score_sprite = pygame.sprite.RenderClear()
    score_left = ScoreBoard(left_name, (5*screen_size[0]/25,30))
    score_right = ScoreBoard(right_name, (20*screen_size[0]/25,30))
    score_sprite.add(score_left)
    score_sprite.add(score_right)
    score_sprite.draw(screen)

    lives_sprite = pygame.sprite.RenderClear()
    lives_left = Lives((5*screen_size[0]/25,60))
    lives_right = Lives((20*screen_size[0]/25,60))
    lives_sprite.add(lives_left)
    lives_sprite.add(lives_right)

    game_over_sprite = pygame.sprite.RenderClear()
    game_over = Game_over()
    game_over_sprite.add(game_over)

    pygame.display.flip()

    # running
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(40)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                lives_left.lives = 0
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    run = False
                    lives_left.lives = 0
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

        #checking if pig hits the wall and adding points

        if piglet.rect.x>=screen_size[0]-10: #right
            wolf.play()
            lives_right.lives -= 1
            if lives_right.lives <= 0:
                run = False
            else:
                lives_sprite.update()
            score_right.points = 0
            bar_left.hits = 0
            bar_right.hits = 0
            score_sprite.update()
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.rect.center = (screen_size[0]/2,screen_size[1]/2)
            piglet.x_velocity = -6
            piglet.y_velocity = randint(-8,8)
        if piglet.rect.x<=0: #left
            wolf.play()
            lives_left.lives -= 1
            if lives_left.lives <= 0:
                run = False
            else:
                lives_sprite.update()
            score_left.points = 0
            bar_left.hits = 0
            bar_right.hits = 0
            score_sprite.update()
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.rect.center = (screen_size[0]/2,screen_size[1]/2)
            piglet.x_velocity = 6
            piglet.y_velocity = randint(-8,8)
        if piglet.rect.y>screen_size[1]-30: #down
            piglet.y_velocity = -piglet.y_velocity
        if piglet.rect.y<=0: #up
            piglet.y_velocity = -piglet.y_velocity 
        
        #checking collisions

        if pygame.sprite.collide_mask(piglet, bar_left):
            if bar_left.hits == bar_right.hits or bar_left.hits+1 == bar_right.hits:
                animal_sound.play()
                bar_left.hits += 1
                score_left.points += 1
            score_sprite.update()
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.hit()
        
        if pygame.sprite.collide_mask(piglet, bar_right):
            if bar_right.hits == bar_left.hits or bar_right.hits+1 == bar_left.hits:
                animal_sound.play()
                bar_right.hits += 1
                score_right.points += 1
            score_sprite.update()
            score_sprite.clear(screen, background)
            score_sprite.draw(screen)
            piglet.hit()
            
        
        piglet_sprite.clear(screen, background)
        bar_sprite.clear(screen, background)
        score_sprite.clear(screen, background)
        lives_sprite.clear(screen, background)
        game_over_sprite.clear(screen, background)
        piglet_sprite.draw(screen)
        bar_sprite.draw(screen)
        score_sprite.draw(screen)
        lives_sprite.draw(screen)



        if lives_left.lives == 0 or lives_right.lives == 0:
            found = False
            if score_left.maxpoints > score_right.maxpoints:
                for i in range(10):
                    if not found:
                        if list_of_scores[i][1] <= score_left.maxpoints:
                            found = True
                            for k in range(8,i-1,-1):
                                list_of_scores[k+1] = list_of_scores[k]
                            list_of_scores[i] = [score_left.name, score_left.maxpoints]
            elif score_right.maxpoints > score_left.maxpoints:
                for i in range(10):
                    if not found:
                        if list_of_scores[i][1] <= score_right.maxpoints:
                            found = True
                            for k in range(8,i-1,-1):
                                list_of_scores[k+1] = list_of_scores[k]
                            list_of_scores[i] = [score_right.name, score_right.maxpoints]
            else:
                for i in range(10):
                    if not found:
                        if list_of_scores[i][1] <= score_left.maxpoints:
                            found = True
                            for k in range(7,i-1,-1):
                                list_of_scores[k+2] = list_of_scores[k]
                            list_of_scores[i] = [score_left.name, score_left.maxpoints]
                            if i+1 <= 9:
                                list_of_scores[i+1] = [score_right.name, score_right.maxpoints]
            write_to_file(list_of_scores)

            game_over_sprite.draw(screen)
            pygame.display.flip()
            time.sleep(5)
        
        
        pygame.display.flip()

#---------------------------------------------------------------------
#                           OPTIONS
#---------------------------------------------------------------------

def set_animal(event1, event2):
    """
    Set the animal of the user's choice
    """
    global pic_name
    if event2 == 2:
        pic_name = "sheep.png"
    elif event2 == 3:
        pic_name = "duck.png"
    else:
        pic_name = "pig.png"

def set_background(event1, event2):
    """
    Set the background of the user's choice

    @param event1: (tuple) !!!!!!!!
    @param event2: (int) the number of the option
    @raise TypeError: if type of given data is incorrect
    """
    if not (isinstance(event1,tuple) and isinstance(event2,int)):
        raise TypeError
    global background_name
    if event2 == 2:
        background_name = "pond.png"
    else:
        background_name = "oink.png"

#---------------------------------------------------------------------
#                             RULES
#---------------------------------------------------------------------

def rules():
    """

    """
    rules_pic = get_image("rules.png")
    screen.blit(rules_pic,(0,0))
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

#---------------------------------------------------------------------
#                            SCORES
#---------------------------------------------------------------------

def scores():
    """
    Display the best scores
    """
    scores_pic = get_image("menu.png")
    screen.blit(scores_pic,(0,0))
    
    best_scores_sprite = pygame.sprite.RenderClear()
    position = [screen_size[0]/2, 50]
    for i in range(10):
        best_scores_sprite.add(BestScores(i, list_of_scores[i], position))
        position[1] += 50
    best_scores_sprite.clear(screen, scores_pic)
    best_scores_sprite.draw(screen)
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



#---------------------------------------------------------------------
#                            AUTHOR
#---------------------------------------------------------------------

def author():
    """
    Display the note and picture about the author
    """
    author_background = get_image("menu.png")
    screen.blit(author_background,(0,0))
    with open("DATA/author.txt", 'r') as text_file:
        text_data = text_file.readlines()
    author_text = []
    position = [screen_size[0]/2, screen_size[1]/5]
    for i in text_data:
        author_text += [Show_text(i[:-1], tuple(position))]
        position[1] += 40
    author_pic = Show_picture("author.png", (screen_size[0]/2, 3*screen_size[1]/4))
    author_pic_sprite = pygame.sprite.RenderClear()
    author_text_sprite = pygame.sprite.RenderClear()
    author_pic_sprite.add(author_pic)
    for i in author_text:
        author_text_sprite.add(i)
    author_pic_sprite.clear(screen, author_background)
    author_text_sprite.clear(screen, author_background)
    author_text_sprite.draw(screen)
    author_pic_sprite.draw(screen)

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

#---------------------------------------------------------------------
#                         SETTING NAME
#---------------------------------------------------------------------

def set_left_name(event):
    """
    Set the name of the left player

    @param event: (str) name given by the user
    @raise TypeError: if type of given data is incorrect
    """
    if not isinstance(event,str):
        raise TypeError
    global left_name
    left_name = event

def set_right_name(event):
    """
    Set the name of the right player

    @param event: (str) name given by the user
    @raise TypeError: if type of given data is incorrect
    """
    if not isinstance(event,str):
        raise TypeError
    global right_name
    right_name = event

#---------------------------------------------------------------------
#                         SETTING DIFFICULTY
#---------------------------------------------------------------------

def set_difficulty(event1, event2):
    """
    Set the difficulty to the level of the user's choice

    @param event1: (tuple) !!!!!!!!
    @param event2: (int) the number of the option
    @raise TypeError: if type of given data is incorrect
    """
    if not (isinstance(event1, tuple) and isinstance(event2, int)):
        raise TypeError
    global bar_pic
    if event2 == 2:
        bar_pic = "bar2.png"
    elif event2 == 3:
        bar_pic = "bar1.png"
    else:
        bar_pic = "bar3.png"

#---------------------------------------------------------------------
#                         WINDOW AND MENU
#---------------------------------------------------------------------

screen_size = (800, 600)
pygame.init()
screen = pygame.display.set_mode(screen_size) 
pygame.display.set_caption("Ping P-oink!")
background_name = "oink.png"
wolf = get_sound("wolf.wav")
pic_name = "pig.png"
left_name = "Player 1"
right_name = "Player 2"
bar_pic = "bar3.png"

if os.path.exists('score_table.txt'):
    with open('score_table.txt', 'r') as table_file:
        score_table = table_file.read()
        #jeszcze obsługę błędów dopisać
    list_of_scores = eval(score_table)
else:
    list_of_scores = [['',0] for i in range(10)]


# creatin menu theme
menu_theme = pygame_menu.Theme(background_color=(0, 0, 0, 0), title_background_color=(247, 136, 181), title_font_color = (0,0,0), title_font = pygame_menu.font.FONT_COMIC_NEUE, selection_color = (255, 0, 102, 1))
menu_pic = pygame_menu.baseimage.BaseImage(image_path=os.path.join('DATA', "menu.png"), drawing_mode=pygame_menu.baseimage.IMAGE_MODE_REPEAT_XY)
menu_theme.background_color = menu_pic
menu_theme.widget_font = pygame_menu.font.FONT_COMIC_NEUE
menu = pygame_menu.Menu(screen_size[1], screen_size[0], 'PING P-OINK!',
                       theme=menu_theme)


menu.add.button('Play', game, font_color = (0, 0, 0), font_size = 100)
menu.add.text_input("Name :", default='Player 1', onchange=set_left_name)
menu.add.text_input("Name :", default='Player 2', onchange=set_right_name)
menu.add.selector('Difficulty :', [('Easy', 1), ('Medium', 2), ("Hard", 3)], onchange=set_difficulty)
menu.add.selector('Animal :', [('Piglet', 1), ('Sheep', 2), ("Duck", 3)], onchange=set_animal)
menu.add.selector('Background :', [('PING P-OINK!', 1), ('Pond', 2)], onchange=set_background)
menu.add.button('Game rules', rules)
menu.add.button('Best scores', scores)
menu.add.button('About the author', author)
menu.add.button('Quit', pygame_menu.events.EXIT)
menu.mainloop(screen)
import pygame
from sys import exit
import math
import random
#Classes
distract_stuff = ["phone", "notify_tablet", "controller"]
school_stuff= ["document", "pencil", "clipboard"]

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_idle = "assets/main_idle.png"
        self.image_walk_1 ="assets/main_walk_1.png"
        self.image_walk_2 ="assets/main_walk_2.png"
        self.image_jump ="assets/main_jump.png"
        self.image_descend  ="assets/main_descend.png"
        self.show_image = self.image_idle
        self.image= pygame.image.load(self.show_image).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100, player_y_pos))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= player_y_pos:
            self.gravity = -20
    def animation_handle(self):
        self.image= pygame.image.load(self.show_image).convert_alpha()
        if self.rect.bottom < player_y_pos:
            self.show_image = self.image_jump
        else:
            self.show_image = self.image_idle
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= player_y_pos:
            self.rect.bottom = player_y_pos
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_handle()

class Stuff(pygame.sprite.Sprite):
    def __init__(self, is_distraction = False, distract = distract_stuff, school = school_stuff):
        super().__init__()
        self.start = random.randint(1600, 1800)
        self.is_distraction = is_distraction
        if is_distraction:
            random_stuff = distract[random.randint(0, len(distract)-1)]
        elif not is_distraction:
            random_stuff = school[random.randint(0, len(school)-1)]
        self.image_path = "assets/%s.png" %random_stuff
        self.image =pygame.image.load(self.image_path).convert_alpha() 
        self.rect = self.image.get_rect(center=(self.start,500))
    def update(self):
        self.rect.x -= 10
        self.destroy()
    def destroy(self):
        if self.rect.x <-100:
            self.kill()
    def draw_test(self):
        self.image =pygame.image.load(self.image_path).convert_alpha() 
#functions
def spawn_stuff():
    if not stuff_group:
        stuff_type = random.choice([True, False])
        stuff_group.add(Stuff(stuff_type))

screen_width = 1600
screen_height = 800
player_y_pos = screen_height -120

#set up
pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("How to Get Better Academic Performance")
clock = pygame.time.Clock()
start_font = pygame.font.Font(None, 50)

player = pygame.sprite.GroupSingle()
player.add(Alien())

stuff_group = pygame.sprite.Group()

testing_group = pygame.sprite.GroupSingle()
testing_group.add(Stuff())
#load assets
bg_sky = pygame.image.load("assets/sky.png").convert()
bg_ground = pygame.image.load("assets/ground.png").convert()


#variables
running = True
bg_scroll = 0
bg_titles = math.ceil(screen_width/bg_sky.get_width())+1



#game loop 
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False
    #scrolling background:
    for i in range(0, bg_titles):
        screen.blit(bg_sky, (i*bg_sky.get_width()+bg_scroll, 0))
    bg_scroll -= 5
    if abs(bg_scroll) >bg_sky.get_width():
        bg_scroll = 0

    screen.blit(bg_ground, (0, player_y_pos))

    stuff_group.draw(screen) 
    stuff_group.update()
    
    testing_group.draw(screen)
    testing_group.update()
    

    player.draw(screen)
    player.update()
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()
exit()
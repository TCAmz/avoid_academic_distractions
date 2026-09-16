import pygame
from sys import exit
import math
import random
#Classes
distract_stuff = ["phone", "notify_tablet", "controller"]
school_stuff= ["document", "pencil", "clipboard", "to_do_list"]

class Alien(pygame.sprite.Sprite):
    def __init__(self, level = 2):
        super().__init__()
        '''self.image_idle = "assets/main_idle.png"
        self.image_walk_1 ="assets/main_walk_1.png"
        self.image_walk_2 ="assets/main_walk_2.png"
        self.image_jump ="assets/main_jump.png"
        self.image_descend  ="assets/main_descend.png"'''
        self.image_eagle_1 = "assets/eagle_1.png"
        self.image_eagle_2 = "assets/eagle_2.png"
        self.image_eagle_3 = "assets/eagle_3.png"
        self.image_eagle_4 = "assets/eagle_4.png"

        self.can_double_jump = True
        self.can_glide = True
        self.can_shoot = True
        self.jumped = False

        match level:
            case 1:
                self.show_image = self.image_eagle_1
            case 2:
                self.show_image = self.image_eagle_2
            case 3:
                self.show_image = self.image_eagle_3
            case 4:
                self.show_image = self.image_eagle_4

        self.image= pygame.image.load(self.show_image).convert_alpha()
        self.rect = self.image.get_rect(midbottom = (100, player_y_pos))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        keys_released = pygame.key.get_just_released()
        if keys[pygame.K_UP]:
                if not self.jumped:  
                    if self.rect.bottom >= player_y_pos:
                        self.gravity = -22
                        self.can_glide = True
                    elif self.can_double_jump:
                        self.gravity = -18
                        self.can_double_jump = False
                        self.can_glide = True
                    self.jumped = True
        if keys[pygame.K_DOWN]:
            '''self.show_image = self.image_descend
            self.image= pygame.image.load(self.show_image).convert_alpha()
            self.rect = self.image.get_rect(midbottom = (100, player_y_pos))'''
            if self.can_glide:
                self.gravity = 2.5
                self.rect.y += self.gravity
        if keys[pygame.K_SPACE]:
            if self.can_shoot:
                shoot_feather()
                self.can_shoot = False
        
        if keys_released[pygame.K_DOWN]:
            '''self.image= pygame.image.load(self.show_image).convert_alpha()
            self.rect = self.image.get_rect(midbottom = (100, player_y_pos))'''
            pass
        if keys_released[pygame.K_UP]:
            self.jumped = False
    def animation_handle(self):'''
        self.image= pygame.image.load(self.show_image).convert_alpha()
        if self.rect.bottom < player_y_pos:
            self.show_image = self.image_jump
        else:
            if self.walk_frame == 1:
                self.show_image = self.image_walk_1
            elif self.walk_frame == 2:
                self.show_image = self.image_walk_2
            else:
                self.show_image = self.image_idle'''
    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= player_y_pos:
            self.rect.bottom = player_y_pos
            self.gravity = 0
            self.can_double_jump = True
            self.can_glide = False
    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_handle()

class Stuff(pygame.sprite.Sprite):
    def __init__(self, is_distraction = False, speed = 10, highest_y = 250, distract = distract_stuff, school = school_stuff):
        super().__init__()
        self.start_x = random.randint(1600, 1800)
        self.start_y = random.randint(player_y_pos-highest_y, player_y_pos-30)
        self.is_distraction = is_distraction
        self.speed = speed
        if is_distraction:
            self.random_stuff = distract[random.randint(0, len(distract)-1)]
        elif not is_distraction:
            self.random_stuff = school[random.randint(0, len(school)-1)]
        self.image_path = "assets/%s.png" %self.random_stuff
        self.image =pygame.image.load(self.image_path).convert_alpha() 
        self.rect = self.image.get_rect(center=(self.start_x,self.start_y))
    def update(self):
        self.rect.x -= self.speed
        self.destroy()
    def destroy(self):
        if self.rect.x <-100:
            self.kill()

class Feather(pygame.sprite.Sprite):
    def __init__(self, player_y_center):
        super().__init__()
        self.image = pygame.image.load("assets/feather.png").convert_alpha()
        self.speed = 15
        self.rect = self.image.get_rect(center = (120, player_y_center))
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > screen_width:
            self.destroy()
    def destroy(self):
        self.kill()
        player.sprite.can_shoot = True

class Barrier(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.text_list = ["Service\nLearning\nProject", "23.5\nCredits","Keystone\nExam", "CTE"]
        self.image = pygame.image.load("assets/barrier.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = (screen_width +80,player_y_pos))
        self.health = 3
        self.text = random.choice(self.text_list)
        if self.text == "CTE":
            self.font_size = 36
        else:
            self.font_size = 30
        self.font = pygame.font.Font(None, self.font_size)
        self.font_surface = self.font.render(self.text, True, (0,0,0))
    def update(self):
        self.rect.x -= 5
        screen.blit(self.font_surface, (self.rect.x +30, self.rect.y + (self.rect.height/2-12)))
        if self.rect.x < -100:
            self.destroy()
    def destroy(self):
        self.kill()

#functions

def spawn_stuff(stuff_speed, highest_y):
    global can_spawn
    global last_spawn_time
    global distraction_in_arow
    if can_spawn == True:
        if distraction_in_arow > 3:
            stuff_type = False
        else:
            stuff_type = random.choice([True, False])

        if stuff_type:
            distraction_in_arow += 1
        else:
            distraction_in_arow = 0
        stuff_group.add(Stuff(stuff_type, stuff_speed, highest_y))
        can_spawn =False
        last_spawn_time = current_time
    else:
        return

def spawn_a_row_stuff(stuff_speed, highest_y):
    global can_spawn
    global last_spawn_time
    global distraction_in_arow
    original_x = 0
    new_y = 250

    new_stuff = Stuff(False, stuff_speed, highest_y)
    new_stuff.rect.y = new_y 
    original_x = new_stuff.rect.x
    stuff_group.add(new_stuff)
    for i in range(0,4):
        new_y += 75
        original_x+= 400
        new_stuff = Stuff(False, stuff_speed, highest_y)
        new_stuff.rect.y = new_y 
        new_stuff.rect.x = original_x
        stuff_group.add(new_stuff)
    can_spawn = False
    
    
    

def shoot_feather():
    player_y = player.sprite.rect.y
    player_y = player_y + player.sprite.rect.height /2
    feather_group.add(Feather(player_y))


def check_collisions():
    global score
    global timer
    if player.sprite:
        collided_stuffs = pygame.sprite.spritecollide(player.sprite, stuff_group, True)
        for stuff in collided_stuffs:
            if stuff.is_distraction == True:
                score -= 10
                timer -= 5
                timer = max(0, timer)
                score = max(0, score)
                fail_sound.play()
            else:
                if stuff.random_stuff == "to_do_list":
                    timer += 5
                else:
                    score += 5
                    score = min(100, score)
                writing_sound.play()
        collided_barrier = pygame.sprite.spritecollide(player.sprite, barrier_group, True)
        for barrier in collided_barrier:
            score -= 20
            score = max(0, score)
            barrier.destroy()
    if feather_group.sprite:
        collided_barrier = pygame.sprite.spritecollide(feather_group.sprite, barrier_group, False)
        for barrier in collided_barrier:
            feather_group.sprite.destroy()
            barrier.health -= 1
            if barrier.health== 0:
                barrier.destroy()
                score += 10
                score = min(100, score)



def display_score_and_timer():
    time_in_minute = int(timer/60)
    time_in_second = timer%60

    score_surf = font.render("Score: "+ str(score), True, (0,0,0))
    score_rect = score_surf.get_rect(topleft=(50, 50))

    timer_surf = font.render(str(time_in_minute) + ":"+str(f"{time_in_second:02}"), True, (0,0,0))
    timer_rect = timer_surf.get_rect(midtop =(screen_width/2, 50))
    screen.blit(score_surf, score_rect)
    screen.blit(timer_surf, timer_rect)



def in_game_scene():
    global bg_scroll
    player.sprite.level = level
    for i in range(0, bg_titles):
            screen.blit(bg_sky, (i*bg_sky.get_width()+bg_scroll, 0))
    bg_scroll -= 3
    if abs(bg_scroll) >bg_sky.get_width():
        bg_scroll = 0

    screen.blit(bg_ground, (0, player_y_pos))

    match level:
        case 1:
            level_1()
        case 2:
            level_2()
        case 3:
            level_3()
        case 4:
            level_4()
    
    player.draw(screen)
    player.update()

    check_collisions()
    display_score_and_timer()  

def result_display():
    grade = ""
    text = ""
    result_font = pygame.font.Font(None, 100)
    commend_font = pygame.font.Font(None, 50)
    result_surf = result_font.render("Game End\nScore: " +str(f"{score:03}"), True, (255, 255, 255))
    result_rect= result_surf.get_rect(midtop=(screen_width/2, 50))
    screen.blit(result_surf, result_rect)

    if score <20:
        grade = "f"
        text = "You didn't pass the test, you should put distractions things out of your sight while learning!"
    elif score <50:
        grade = "d"
        text = "You didn't pass the test, but it's almost there may be try to more focus and try harder in your next time!"
    elif score <60:
        grade = "c"
        text = "You passed the test, but you can do it better if put more effort on it."
    elif score <80:
        grade = "b"
        text = "Good job! The Key is to try to avoid distractions. Easy, isn't it?"
    elif score <= 100:
        grade = "a"
        text = "Wonderful! Keep this momentum going, you're on a roll"
    commend_surf = commend_font.render(text, True, (255, 255, 255))
    commend_rect = commend_surf.get_rect(midtop = (screen_width/2 , screen_height-500))

    grade_image = pygame.image.load("assets/grade_%s.png"%grade).convert_alpha()
    grade_image_rect = grade_image.get_rect(midtop = (screen_width - 300, 50))

    screen.blit(grade_image, grade_image_rect)
    screen.blit(commend_surf, commend_rect)

    
def level_1():
    num_of_stuffs = 2
    highest_y = 250
    stuff_speed = 10

    stuff_group.draw(screen) 
    stuff_group.update()
    if not len(stuff_group)>num_of_stuffs and can_spawn == True:
        spawn_stuff(stuff_speed, highest_y)


def level_2():
    num_of_stuffs = 3
    highest_y = 300
    stuff_speed = 15

    stuff_group.draw(screen) 
    stuff_group.update()
    if not len(stuff_group)>num_of_stuffs and can_spawn == True:
        spawn_stuff(stuff_speed, highest_y)

def level_3():
    num_of_stuffs = 3
    highest_y = 300
    stuff_speed = 25
    rate = random.randint(0, 100)

    stuff_group.draw(screen) 
    stuff_group.update()
    if rate <= 3:
        if not len(stuff_group)>num_of_stuffs and can_spawn == True:
            spawn_a_row_stuff(stuff_speed, highest_y)
    else:
        if not len(stuff_group)>num_of_stuffs and can_spawn == True:
            spawn_stuff(stuff_speed, highest_y)

def level_4():
    global time_passed 
    num_of_stuffs = 3
    highest_y = 460
    stuff_speed = 25
    rate = random.randint(0, 100)
    if time_passed >= 10:
        barrier_group.add(Barrier())
        time_passed -= 10
    barrier_group.draw(screen)
    barrier_group.update()
    feather_group.draw(screen)
    feather_group.update()

    stuff_group.draw(screen) 
    stuff_group.update()
    if rate <= 3:
        if not len(stuff_group)>num_of_stuffs and can_spawn == True:
            spawn_a_row_stuff(stuff_speed, highest_y)
    else:
        if not len(stuff_group)>num_of_stuffs and can_spawn == True:
            spawn_stuff(stuff_speed, highest_y)


#set up

screen_width = 1600
screen_height = 800
player_y_pos = screen_height -120

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("How to Get Better Academic Performance")
clock = pygame.time.Clock()
start_font = pygame.font.Font(None, 50)

player = pygame.sprite.GroupSingle()
player.add(Alien())

stuff_group = pygame.sprite.Group()
feather_group = pygame.sprite.GroupSingle()
barrier_group = pygame.sprite.Group()

#load assets
bg_sky = pygame.image.load("assets/sky.png").convert()
bg_ground = pygame.image.load("assets/ground.png").convert()
 
start_scene = pygame.image.load("assets/start_scene.png").convert()
start_button = pygame.image.load("assets/start_button.png").convert_alpha()
start_button_rect = start_button.get_rect(center=(725, screen_height-75))

end_scene = pygame.image.load("assets/end_scene.png").convert()
exit_button = pygame.image.load("assets/exit_button.png").convert_alpha()
exit_button_rect = exit_button.get_rect(center=(screen_width/2 -250, screen_height-75))

play_again_button = pygame.image.load("assets/play_again_button.png").convert_alpha()
play_again_button_rect = play_again_button.get_rect(center=(screen_width/2+250, screen_height-75))

writing_sound = pygame.mixer.Sound("assets/sfx/writing_cutted.mp3")
writing_sound.set_volume(0.5)

fail_sound = pygame.mixer.Sound("assets/sfx/fail.mp3")
fail_sound.set_volume(0.5)

#variables
level = 4

timer = 25
time_passed = 0

running = True
bg_scroll = 0
bg_titles = math.ceil(screen_width/bg_sky.get_width())+1
distraction_in_arow = 0


game_end = False
game_scene = 0
introduce_scene = 0
score = 0



TIMER_EVENT = pygame.USEREVENT + 1
TIMER_WALKING = pygame.USEREVENT + 2

pygame.time.set_timer(TIMER_EVENT, 1000)
pygame.time.set_timer(TIMER_WALKING, 250)
spawn_timer = 1000
last_spawn_time = 0
can_spawn = True

font = pygame.font.Font(None, 60)

#game loop 
while running:
    current_time= pygame.time.get_ticks()
    if current_time - last_spawn_time >= spawn_timer:
        can_spawn = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:   
            running = False
        if event.type == TIMER_EVENT and game_scene == 1:
            if timer > 0:
                timer -= 1
                time_passed += 1
        '''if event.type == TIMER_WALKING and game_scene == 1:
            if player.sprite.walk_frame ==1 :
                player.sprite.walk_frame = 2
            else:
                player.sprite.walk_frame = 1'''
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if start_button_rect.collidepoint(event.pos):
                    running = True
                    game_scene = 1
                    match level:
                        case 1:
                            timer = 60
                        case 2:
                            timer = 40
                        case 3:
                            40
                        case 4:
                            35
                if exit_button_rect.collidepoint(event.pos):
                    running = False
                if play_again_button_rect.collidepoint(event.pos):
                    score = 0
                    timer = 60
                    game_scene = 1
                    
                    
    if timer <= 0:
        game_scene =2

    if game_scene == 0:
        if introduce_scene == 0:
            screen.blit(start_scene, (0,0))
            screen.blit(start_button, start_button_rect)
        elif introduce_scene == 1:
            pass
    elif game_scene == 1:
        in_game_scene()
    elif game_scene == 2:
        screen.blit(end_scene, (0,0))
        screen.blit(exit_button, exit_button_rect)
        screen.blit(play_again_button, play_again_button_rect)
        result_display()
    
    pygame.display.update()
    clock.tick(60)
pygame.quit()
exit()
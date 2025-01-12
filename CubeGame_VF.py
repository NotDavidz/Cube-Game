# *CubeGame is developed by David Zhang and finalized in 2024/2025 using Python and Pygame
import pygame
import random
import math
pygame.init()
size = (1280,700)

#Initializing Variables 
# 640,350 is center
screen = pygame.display.set_mode(size)
done = False
lv5_finished = False
difficulty = 0
RED = (255,0,0)
PURPLE = (255,0,255)
DARKRED = (75,0,0)
GREEN = (0,255,0)
DARKGREEN = (0,75,0)
BLK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
DARKBLUE = (0,0,75)
GOLD = (255,215,0)
clock = pygame.time.Clock()

# Images and art 
bullet_img = pygame.image.load("Bullet.png")
block_img = pygame.image.load("Bouncing Block.png")
normal_button = pygame.image.load("Normal.png")
hardcore_button = pygame.image.load("Hardcore.png")
infinite_button = pygame.image.load("infinite.png")
start_button = pygame.image.load("start button.png")
help_button = pygame.image.load("help button.png")
quit_button = pygame.image.load("quit button.png")
laser_img = pygame.image.load("laser.png")
zap_img = pygame.image.load("zap.png")
player_img = pygame.image.load("Blue Cube.png")
player_img = pygame.transform.scale(player_img,(25,25))
level1_img = pygame.image.load("lv1 button.png")
level2_img = pygame.image.load("lv2 button.png")
level3_img = pygame.image.load("lv3 button.png")
level4_img = pygame.image.load("lv4 button.png")
level5_img = pygame.image.load("lv5 button.png")
lockedlevel_img = pygame.image.load("lv locked button.png")
normal_pass = pygame.image.load("normal pass.png")
normal_fail = pygame.image.load("normal fail.png")
hardcore_death = pygame.image.load("hardcore death.png")
normal_win = pygame.image.load("normal win.png")
hardcore_win = pygame.image.load("hardcore win.png")
help1 = pygame.image.load("help1.png")
help2 = pygame.image.load("help2.png")
help3 = pygame.image.load("help3.png")
help4 = pygame.image.load("help4.png")
help5 = pygame.image.load("help5.png")
help_left = pygame.image.load("help left.png")
help_left = pygame.transform.scale(help_left,(50,100))
help_right = pygame.image.load("help right.png")
help_right = pygame.transform.scale(help_right,(50,100))
help_cont = pygame.image.load("help cont.png")
difficulty_back = pygame.image.load("difficulty back.png")
infinite_over = pygame.image.load("infinite over.png")
level_reset_btn = pygame.image.load("level reset.png")
yes = pygame.image.load("yes.png")
no = pygame.image.load("no.png")
pygame.display.set_caption('Cube Game')
pygame.display.set_icon(player_img)
font2 = pygame.font.SysFont("Calibri",40,True,False)
help = 1
scene = 0
level = 6
death = 0
infinite_highscore = 0
infinite_score = 0
infinite_end_score = str(infinite_score)
infinite_end_score_img = font2.render(infinite_end_score, True, WHITE)

# Level status to unlock other levels 
Lv1_status = 0
Lv2_status = 0
Lv3_status = 0
Lv4_status = 0
Lv5_status = 0

# Level Tools


def level_reset(keep_hp):
    global laser_cd
    laser_cd = 0
    global laser2_cd 
    laser2_cd = 0
    global laser_duration 
    laser_duration = 30
    global laser2_duration
    laser2_duration = 20
    global prediction_laser 
    prediction_laser = 35
    global prediction_laser2
    prediction_laser2 = 25
    global start_delay
    start_delay = 0
    global bullet_dmg 
    bullet_dmg = False
    global bulletX 
    bulletX = 1290
    global gravity
    gravity = 0.8
    global playerX 
    playerX = 200
    global playerY 
    playerY = 525
    global hp
    if not keep_hp:
        hp = 300
    global moveright 
    moveright = False
    global moveleft 
    moveleft = False
    global ball_xmovement
    ball_xmovement = 7
    global ball_ymovement
    ball_ymovement = 7
    global ball2_xmovement
    ball2_xmovement = -10
    global ball2_ymovement
    ball2_ymovement = -10
    global ballx
    ballx = 640
    global bally
    bally = 200
    global ball2x
    ball2x = 640
    global ball2y 
    ball2y = 220
    global timer
    timer = 2200 


level_reset(True)

def victory_screen_display():
    screen.fill(BLK)
    font = pygame.font.SysFont("Calibri",60,True,False)
    death_message = str(death) 
    death_message_img = font.render(death_message, True, BLK)
    if difficulty == 0:
        screen.blit(normal_win,(340,110))
        screen.blit(death_message_img,(640,350))
    elif difficulty == 1:
        screen.blit(hardcore_win,(340,110))

def infinite_score_display():
    global infinite_score
    global infinite_highscore 
    print(infinite_score)
    print(infinite_highscore)
    if infinite_score > infinite_highscore:
        infinite_highscore = infinite_score
    screen.fill(BLK)
    screen.blit(infinite_over,(340,110))   
    infinite_end_highscore = str(infinite_highscore)
    infinite_end_highscore_img = font2.render(infinite_end_highscore, True, GOLD)
    infinite_end_score = str(infinite_score)
    infinite_end_score_img = font2.render(infinite_end_score, True, WHITE)
    screen.blit(infinite_end_score_img,(595,303))
    screen.blit(infinite_end_highscore_img,(595,390))      
    screen.blit(difficulty_back,(590,450))    


def title_screen_display():
    screen.fill(BLK)
    screen.blit(start_button,(540,200))
    screen.blit(help_button,(540,325))
    screen.blit(quit_button,(540,450))

def difficulty_display():
    screen.fill(BLK)
    screen.blit(infinite_button,(315,300))
    screen.blit(normal_button,(540,300))
    screen.blit(hardcore_button,(765,300))
    screen.blit(difficulty_back,(590,500))

def level_selection_display():
    screen.fill(BLK)
    screen.blit(level1_img,(140,300))
    if Lv1_status == 2:
        screen.blit(level2_img,(340,425))
    else:
        screen.blit(lockedlevel_img,(340,425))
    if Lv2_status == 2:
        screen.blit(level3_img,(540,300))
    else:
        screen.blit(lockedlevel_img,(540,300))        
    if Lv3_status == 2:
        screen.blit(level4_img,(740,425))
    else:
        screen.blit(lockedlevel_img,(740,425))         
    if Lv4_status == 2:
        screen.blit(level5_img,(940,300))
    else:
        screen.blit(lockedlevel_img, (940,300))
    pygame.draw.rect(screen, RED, (630,200,20,20))
    screen.blit(difficulty_back,(590,120))    

def tutorial_display():
    global help
    help_arr = [help1, help2, help3, help4, help5]
    print(help)
    screen.blit(help_arr[help-1],(240,50))
    
    if help > 1:
        screen.blit(help_left,(270,300))
    if help < 5:
        screen.blit(help_right,(960,300))        
    if help == 5:
        screen.blit(help_cont,(590,550))    
        
def level_reset_display():
    screen.fill(BLK)
    screen.blit(level_reset_btn,(340,110))
    screen.blit(yes,(440,450))
    screen.blit(no,(800,450))    


def level_display():
    pass

def damage_check():
    global hp

    if prediction_laser >= 35 and laser_duration < 30:
        if player_rect.colliderect(laser_rect):
            hp = hp - 3
    if prediction_laser2 >= 25 and laser2_duration < 15:
        if player_rect.colliderect(laser2_rect):
            hp = hp - 2
    if bullet_dmg == True:
        if player_rect.colliderect(bullet_rect):
            hp = hp - 15
    if bullet_dmg == True:
        if player_rect.colliderect(bullet_rect):
            hp = hp - 15
    if start_delay > 205 and (level == 4 or level == 5 or level == 6):
        if player_rect.colliderect(block_rect):
            hp = hp - 15
        if level == 5 or level == 6:
            if player_rect.colliderect(block2_rect):
                hp = hp - 20            

def red_laser():
    global laser_cd 
    global prediction_laser 
    global laser_duration
    global laser_location
    global laser_rect 
    
    laser_cd = laser_cd + 1
    if laser_cd > 90:
        laser_location = random.randrange(0,1180)
        laser_cd = 0
        prediction_laser = 0
        laser_duration = 0
    if prediction_laser < 35:
        prediction_laser = prediction_laser + 1
        pygame.draw.rect(screen, DARKRED, [laser_location,0,100,550])
    if prediction_laser >= 35 and laser_duration < 30:
        screen.blit(laser_img,(laser_location,0,100,550))
        laser_rect = ([laser_location,0,100,550])
        laser_duration = laser_duration + 1

def blue_laser():
    pass

def bullet():
    global bulletX
    global bullet_rect
    global bullet_dmg
    
    screen.blit(bullet_img,[bulletX,520])
    bullet_rect = ([bulletX, 520,30,20])
    bulletX = bulletX - 10
    bullet_dmg = True
    if bulletX < -10:
        bulletX = 1290 
        
    #HITBOX DISPLAY FOR DEBUGGING: 
    #pygame.draw.rect(screen, BLUE, [bulletX, 520,30,20])    

def assassin1():
    global ballx, bally, ball_xmovement, ball_ymovement, block_rect 
    screen.blit(block_img,[ballx,bally])
    block_rect = pygame.Rect([ballx,bally,50,50])
    ballx = ballx + ball_xmovement
    bally = bally + ball_ymovement
    if ballx <= 0 or ballx >= 1230:
        ball_xmovement = -ball_xmovement
    if bally <= 0 or bally >= 500:
        ball_ymovement = -ball_ymovement
        
def assassin2():
    global ball2x, ball2y, ball2_xmovement, ball2_ymovement, block2_rect 
    screen.blit(block_img,[ball2x,ball2y])
    block2_rect = pygame.Rect([ball2x,ball2y,50,50])
    ball2x = ball2x + ball2_xmovement
    ball2y = ball2y + ball2_ymovement
    if ball2x <= 0 or ball2x >= 1230:
        ball2_xmovement = -ball2_xmovement
    if ball2y <= 0 or ball2y >= 500:
        ball2_ymovement = -ball2_ymovement   

def mouse_bound(x_min, x_max, y_min, y_max):
    return posX > x_min and posX < x_max and posY > y_min and posY < y_max

def draw_border(x_min, x_max, y_min, y_max):
    if posX > x_min and posX < x_max and posY > y_min and posY < y_max:
        pygame.draw.rect(screen,WHITE,[x_min, y_min ,x_max - x_min ,y_max - y_min],3)     
                    
#RUN GAME
#RUN GAME 
#RUN GAME 
while not done:
    
    # Gets mouse position 
    mousepos = pygame.mouse.get_pos()
    posX = mousepos[0]
    posY = mousepos[1]
    
    #Title Screen

    # Win Screen
    if lv5_finished == True:
        scene = 20
    if scene == 20:
        victory_screen_display()
    
    # Title Screen
    elif scene == 0:
        title_screen_display()
        
    # Difficulty selection screen
    elif scene == 1:
        difficulty_display()
        
    # Infinite Mode Finish Screen
    elif scene == 40:
        infinite_score_display()
        
    # Level selection screen
    elif scene == 2:
        level_selection_display()
    
             
    # Tutorial Screen
    elif scene == 30:
        tutorial_display()
    
    # Level reset display
    elif scene == 50:
        level_reset_display()
                       
    # Death/Win Screen
    elif scene == 10:
        screen.fill(BLK)
        screen.blit(normal_pass,(390,150))

    elif scene == 11:
        screen.fill(BLK)
        screen.blit(normal_fail,(390,150))
        
    elif scene == 12:
        screen.fill(BLK)
        screen.blit(hardcore_death,(390,150))
    
    # Level Screen
    else:

        # Background and Ground
        screen.fill(BLK)
        pygame.draw.rect(screen, WHITE, [0,550,1280,200])
        
        # Vertical Lasers, true for all levels 1-5
        start_delay = start_delay + 1
        if level == 6:
            infinite_score = infinite_score + 1
        if (level == 1 or level == 2 or level == 3 or level == 4 or level == 5 or level == 6) and start_delay > 120:
            red_laser()
            
        # Horzontal bullet shooter, true for levels 2
        if level == 2 and start_delay > 200:
            bullet()

                           
        # Horzontal bullet shooter replaced by horzontal laser, true for level 3-5
        if level == 3 or level == 4 or level == 5 or level == 6:
            if start_delay > 120:
                laser2_cd = laser2_cd + 1
                if laser2_cd > 70:
                    laser2_cd = 0
                    prediction_laser2 = 0
                    laser2_duration = 0
            if prediction_laser2 < 25:
                prediction_laser2 = prediction_laser2 + 1
                pygame.draw.rect(screen, DARKBLUE, [0,500,1280,50])
            if prediction_laser2 >= 25 and laser2_duration < 15:
                screen.blit(zap_img,[0,500])
                laser2_rect = ([0,450,1280,200])
                laser2_duration = laser2_duration + 1
                
        # Damage dealing ball bouncing around, true for level 4 - 5
        if (level == 4 or level == 5 or level == 6) and start_delay > 200:
            assassin1()
            
        if (level == 5 or level == 6) and start_delay > 200:
            assassin2()
                          
            
        #HP and Timer Bar 
        if start_delay < 200:
            pygame.draw.rect(screen, DARKRED, [490,60,start_delay*3/2,10])
        if start_delay > 200:
            pygame.draw.rect(screen, DARKRED, [490,60,300,10])
            if level == 6:
                pygame.draw.rect(screen, PURPLE, [490,60,int(timer/3.33/2),10]) 
            else:
                pygame.draw.rect(screen, RED, [490,60,int(timer/3.33/2),10])
        
        if difficulty == 0:
            pygame.draw.rect(screen, DARKGREEN, [340,40,600,20])
            pygame.draw.rect(screen, GREEN, [340,40,hp*2,20])
            
        #Display Player 
        screen.blit(player_img,(playerX, playerY))
        player_rect = pygame.Rect([playerX,playerY,25,25])
        gravity = gravity + 1
        playerY = playerY + gravity
        if playerX <= 0:
            playerX = 0
        if playerX >= 1255:
            playerX = 1255
        if playerY >= 525:
            playerY = 525
        if moveright:
            if playerX < 1255:
                playerX = playerX + 7
        if moveleft:
            if playerX > 0:
                playerX = playerX - 7
        # Health Damage Conditions 
        damage_check() 
                    
        # Health Display
        if hp < 0:
            if level == 6:
                scene = 40
            else:
                death = death + 1
                if difficulty == 0:
                    scene = 11
                elif difficulty == 1:
                    scene = 12
                laser_cd = 0
                
                # Level Reset
                level_reset(True)
                
                if Lv5_status == 3:
                    Lv5_status = 2
                elif Lv5_status == 1:
                    Lv5_status = 0
                if Lv4_status == 3:
                    Lv4_status = 2
                elif Lv4_status == 1:
                    Lv4_status = 0
                if Lv3_status == 3:
                    Lv3_status = 2
                elif Lv3_status == 1:
                    Lv3_status = 0
                if Lv2_status == 3:
                    Lv2_status = 2
                elif Lv2_status == 1:
                    Lv2_status = 0
                if Lv1_status == 3:
                    Lv1_status = 2
                elif Lv1_status == 1:
                    Lv1_status = 0        
        #Timer
        if not level == 6:
            timer = timer - 1
            # Timer Display
            if timer < 0:
                if Lv5_status == 1:
                    scene = 20
                else:
                    scene = 10
                # Level reset
                level_reset(False)   
                
                if Lv4_status == 1 or Lv4_status == 3:
                    Lv4_status = 2
                if Lv3_status == 1 or Lv3_status == 3:
                    Lv3_status = 2
                if Lv2_status == 1 or Lv2_status == 3:
                    Lv2_status = 2
                if Lv1_status == 1 or Lv1_status == 3:
                    Lv1_status = 2
                if Lv5_status == 1 or Lv5_status == 3:
                    Lv5_status = 2
                    Lv5_finished = True
                    
        
    # Outlines if mouse hovers over buttons 
    if scene == 0:
        draw_border(540, 740, 200, 300)
        draw_border(540, 740, 325, 425)
        draw_border(540, 740, 450, 550)

    if scene == 1:
        draw_border(315, 515, 300, 400)
        draw_border(540, 740, 300, 400)
        draw_border(765, 965, 300, 400)
        draw_border(590, 690, 500, 550)
        
    if scene == 40:
        draw_border(590, 690, 450, 500)       
    if scene == 2:
        draw_border(140, 340, 300, 420)
        if Lv1_status == 2:
            draw_border(340, 540, 425, 545) 
        if Lv2_status == 2:
            draw_border(540, 740, 300, 420) 
        if Lv3_status == 2:
            draw_border(740, 940, 425, 545) 
        if not lv5_finished:
            draw_border(940, 1140, 300, 420) 
        draw_border(590, 690, 120, 170)
        draw_border(630, 650, 200, 220)
            
    if scene == 12:
        draw_border(596, 674, 470, 520)
        
    if scene == 10 or scene == 11:   
        draw_border(580, 691, 425, 489) 
        
    if scene == 20:
        draw_border(455, 580, 440, 506)
        draw_border(694, 819, 440, 506)  
        
    if scene == 30:
        if help == 5:
            draw_border(590, 690, 550, 600)
        if help > 1:
            draw_border(270, 320, 300, 400)
        if help < 5:
            draw_border(960, 1010, 300, 400)
            
    if scene == 50:
        draw_border(440, 490, 450, 500)
        draw_border(800, 900, 450, 500)
            
    # Mouse click input for different scenes 
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            buttons = pygame.mouse.get_pressed()
            if buttons[0]:
                
                if scene == 50:
                    
                    if mouse_bound(440, 490, 450, 500):
                        level_reset(False) 
                        scene = 1
                    if mouse_bound(800, 900, 450, 500): 
                        scene = 2
                        
                if scene == 40:
                    
                    if mouse_bound(590, 690, 450, 500):    
                        level_reset(False)
                        scene = 1
                        
                if scene == 0:
                    
                    if mouse_bound(540, 740, 450, 550):
                        done = True
                    if mouse_bound(540, 740, 200, 300):
                        scene = 1
                    if mouse_bound(540, 740, 325, 425):
                        help = 1
                        scene = 30
                        
                if scene == 1:
                    
                    if mouse_bound(540, 740, 300, 400):
                        scene = 2
                        difficulty = 0
                        hp = 300
                        
                    if mouse_bound(765, 965, 300, 400):
                        scene = 2
                        difficulty = 1
                        hp = 1
                        
                    if mouse_bound(315, 515, 300, 400):
                        scene = 3
                        hp = 300
                        level = 6
                        infinite_score = 0
                        
                    if mouse_bound(590, 690, 500, 550):
                        scene = 0 
                        
                if scene == 11 or scene == 10:
                    
                    if mouse_bound(596, 674, 470, 520):
                        scene = 2
                
                if scene == 12:

                    if mouse_bound(596, 674, 470, 520):
                        done = True
                        
                if scene == 10 or scene == 11:
                    
                    if mouse_bound(580, 691, 425, 489):
                        scene = 2
                
                if scene == 2: 
                    if posX > 590 and posX < 690 and posY > 120 and posY < 170:
                        scene = 50
                    if posX > 630 and posX < 650 and posY > 200 and posY < 220:
                        done = True
                    if posX > 140 and posX < 340 and posY > 300 and posY < 420:
                        if Lv1_status == 2:
                            level = 1
                            scene = 3
                            Lv1_status = 3
                        else:
                            level = 1
                            scene = 3
                            Lv1_status = 1                            
                    if posX > 340 and posX < 540 and posY > 425 and posY < 545:
                        if Lv2_status == 2:
                            level = 2
                            scene = 3
                            Lv2_status = 3
                        elif Lv1_status == 2:
                            level = 2
                            scene = 3
                            Lv2_status = 1
                    if posX > 540 and posX < 740 and posY > 300 and posY < 420:
                        if Lv3_status == 2:
                            level = 3
                            scene = 3
                            Lv3_status = 3
                        elif Lv2_status == 2:
                            level = 3
                            scene = 3
                            Lv3_status = 1
                    if posX > 740 and posX < 940 and posY > 425 and posY < 545:
                        if Lv4_status == 2:
                            level = 4
                            scene = 3
                            Lv4_status = 3
                        elif Lv3_status == 2:
                            level = 4
                            scene = 3
                            Lv4_status = 1
                    if posX > 940 and posX < 1140 and posY > 300 and posY < 420:
                        if Lv5_status == 2:
                            level = 5
                            scene = 3
                            Lv5_status = 3
                        elif Lv4_status == 2:
                            level = 5
                            scene = 3
                            Lv5_status = 1                    
                        
                if scene == 20:
                    if posX > 455 and posX < 580 and posY > 440 and posY < 506:
                        scene = 2
                    if posX > 694 and posX < 819 and posY > 440 and posY < 506:
                        done = True          
                if scene == 30:
                    if posX > 270 and posX < 320 and posY > 300 and posY < 400 and help > 1:
                        help = help - 1
                    if posX > 960 and posX < 1010 and posY > 300 and posY < 400 and help < 5:
                        help = help + 1
                    if posX > 590 and posX < 690 and posY > 550 and posY < 600 and help == 5:
                        scene = 0                   
       
        #Physics        
        if scene == 3: 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    moveleft = True
                if event.key == pygame.K_d:
                    moveright = True 
                if event.key == pygame.K_SPACE:
                    if (playerY == 525):
                        gravity = -20
                if event.key == pygame.K_w:
                    if (playerY == 525):
                        gravity = -20                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    moveleft = False
                if event.key == pygame.K_d:
                    moveright = False
                    
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
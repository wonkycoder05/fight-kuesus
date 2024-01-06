import pygame
from pygame import mixer
from fighter import Fighter


mixer.init()
pygame.init()

#game window


SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FIGHT!!KUESUS")

#framerate
clock = pygame.time.Clock()
FPS = 60

#coloring time!!
YELLOW= (255, 255, 0)
GREEN =(0, 255, 0)
RED   =(255, 0, 0)
WHITE=(255, 255, 255)

#game variables

intro_count = 4
last_count_up = pygame.time.get_ticks()
score = [0, 0] # [p1, p2]
round_over = False
ROUND_CD = 2000

#def fighter var
HERO1_SIZE = 200.25
HERO1_SCALE = 4
HERO1_OFFSET = [90 , 80]
HERO1_DATA = [HERO1_SIZE, HERO1_SCALE, HERO1_OFFSET]
HERO2_SIZE = 200.25
HERO2_SCALE = 4.5
HERO2_OFFSET = [85 , 80]
HERO2_DATA = [HERO2_SIZE, HERO2_SCALE, HERO2_OFFSET]

#VINE GO BOOM HUAHAHAHAHAHAHAHHAAH

pygame.mixer.music.load('assets/audio/battle_theme.ogg')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.5, 50)



#battle theme by: @MadPezkoh on YT
#the other sound effects are stock effects hehehe

sword_fx = pygame.mixer.Sound("assets/audio/shing.mp3")
boing = pygame.mixer.Sound("assets/audio/boing.mp3")



#function for pulling out bgimg
def pull_bg():
    scaled_bg = pygame.transform.scale(bgimg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))


#load da sproots

hero_sheet = pygame.image.load("hero1.png").convert_alpha()
hero2_sheet = pygame.image.load("hero2.png").convert_alpha() 

victory_img = pygame.image.load("menang.png").convert_alpha()
smolvic = pygame.transform.scale(victory_img, (900, 480))
#img by DracoAwesomeness on deviantart

#define number of steps
HERO1_ANIMATION_STEPS = [4, 4, 7, 2, 4, 2, 8, 3]
HERO2_ANIMATION_STEPS = [6, 6, 6, 2, 8, 8, 4, 4]

font = pygame.font.Font("pixel.otf", 80)
scoreboard = pygame.font.Font("pixel.otf", 30)

def txt_display(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

#health bar broskis
def draw_hp(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, ( x, y, 400 , 30))
    pygame.draw.rect(screen, YELLOW, ( x, y, 400 * ratio, 30))
    
#create two fighters:
fighter_1 = Fighter(1, 200, 310, False, HERO1_DATA, hero_sheet, HERO1_ANIMATION_STEPS, sword_fx, boing)
fighter_2 = Fighter(2, 700, 310, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_STEPS, sword_fx, boing)
#load bgimg

bgimg = pygame.image.load("assets/darkshrine.png").convert_alpha()


#loop
run = True
while run:

    clock.tick(FPS)

#pull dat bg
    pull_bg()

    
#show hp bar
    draw_hp(fighter_1.health, 20, 20)
    draw_hp(fighter_2.health, 540, 20)
    txt_display("P1: " + str(score[0]), scoreboard, WHITE, 20, 60)
    txt_display("P2: "+ str(score[1]), scoreboard, WHITE, 540, 60)
    

#moov da pipol:
    if intro_count <= 0 :
        fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)

        fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
    else: 
        txt_display(str(intro_count), font, YELLOW, SCREEN_WIDTH / 2.1, SCREEN_HEIGHT / 3)

        if (pygame.time.get_ticks() -  last_count_up) >= 1000:
            intro_count -=1
            last_count_up = pygame.time.get_ticks()
 

    #up animations
    fighter_1.update()
    fighter_2.update()

#draw fighters:
    fighter_1.draw(screen)
    fighter_2.draw(screen)

    if round_over == False:
        if fighter_1.alive == False:
            score[1] += 1
            round_over = True
            round_overtime = pygame.time.get_ticks()
            

        elif fighter_2.alive == False:
            score[0] += 1
            round_over = True
            round_overtime = pygame.time.get_ticks()
            
    else:
        screen.blit(smolvic, (20, 20))
   
        if pygame.time.get_ticks() - round_overtime > ROUND_CD:
            round_over = False
            intro_count = 4
            fighter_1 = Fighter(1, 200, 310, False, HERO1_DATA, hero_sheet, HERO1_ANIMATION_STEPS, sword_fx, boing)
            fighter_2 = Fighter(2, 700, 310, True, HERO2_DATA, hero2_sheet, HERO2_ANIMATION_STEPS, sword_fx, boing)  



#event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    pygame.display.update()
    pygame.display.flip()

#exit pygame 
pygame.quit()
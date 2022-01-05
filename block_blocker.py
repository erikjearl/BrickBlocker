import pygame
import os
import random
pygame.font.init()

from pygame import display

WIDTH, HEIGHT = 775,650
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("BLOCK BLOCKER")

BLACK = (0,0,0)
PURPLE = (220,208,255)

BORDER_TOP = (640,0, 10, HEIGHT)
BORDER_SIDE = (0,90,WIDTH,10)

FPS = 60
NUM_SPAWN = 0
SPAWN_TIMER = 1100 #ms between spawns
GAME_OVER = False

#hitbox
GRAY_HIT = pygame.USEREVENT + 1
ORANGE_HIT = pygame.USEREVENT + 2
PINK_HIT = pygame.USEREVENT + 3
GRAY_HEART = pygame.USEREVENT + 4
ORANGE_HEART = pygame.USEREVENT + 5
PINK_HEART = pygame.USEREVENT + 6
BLOCKER_HIT = pygame.USEREVENT + 7

STICKMAN_WIDTH = 110
STICKMAN_HEIGHT = 100
STICKMAN_GRAY_FULL = pygame.image.load(os.path.join('Assets','stickman_gray_full.png'))
STICKMAN_GRAY_HALF = pygame.image.load(os.path.join('Assets','stickman_gray_half.png'))
STICKMAN_GRAY_GOLD = pygame.image.load(os.path.join('Assets','stickman_gray_gold.png'))
STICKMAN_ORANGE_FULL = pygame.image.load(os.path.join('Assets','stickman_orange_full.png'))
STICKMAN_ORANGE_HALF = pygame.image.load(os.path.join('Assets','stickman_orange_half.png'))
STICKMAN_ORANGE_GOLD = pygame.image.load(os.path.join('Assets','stickman_orange_gold.png'))
STICKMAN_PINK_FULL = pygame.image.load(os.path.join('Assets','stickman_pink_full.png'))
STICKMAN_PINK_HALF = pygame.image.load(os.path.join('Assets','stickman_pink_half.png'))
STICKMAN_PINK_GOLD = pygame.image.load(os.path.join('Assets','stickman_pink_gold.png'))
STICKMAN_X1 = 15
STICKMAN_X2 = 140
STICKMAN_X3 = 265
STICKMAN_X4 = 390
STICKMAN_X5 = 515
STICKMAN_Y = 525

BLOCKER = pygame.image.load(os.path.join('Assets','blocker.png'))
BLOCKER_X = 125
BLOCKER_Y = 35
BRICK = pygame.image.load(os.path.join('Assets','brick.png'))
BRICK_DIM = 100
BRICK_VEL = 5

HEART = pygame.image.load(os.path.join('Assets','heart.png'))
HEART_X = 90
HEART_Y = 85

BOMB = pygame.image.load(os.path.join('Assets','bomb.png'))
BOMB_X = 80
BOMB_Y = 100

FONT = pygame.font.SysFont('Sitka Text', 65)

def draw_bg(ending):
    WIN.fill(PURPLE)
    pygame.draw.rect(WIN, BLACK, BORDER_TOP)
    pygame.draw.rect(WIN, BLACK, BORDER_SIDE)
    pygame.draw.rect(WIN, BLACK, (STICKMAN_X1,635, 110, 5))
    pygame.draw.rect(WIN, BLACK, (STICKMAN_X2,635, 110, 5))
    pygame.draw.rect(WIN, BLACK, (STICKMAN_X3,635, 110, 5))
    pygame.draw.rect(WIN, BLACK, (STICKMAN_X4,635, 110, 5))
    pygame.draw.rect(WIN, BLACK, (STICKMAN_X5,635, 110, 5))
    #health_text = FONT.render(str(health), 1, BLACK)
    #WIN.blit(health_text, (560,5))
    title = FONT.render("BRICK BLOCKER",4,BLACK) 
    WIN.blit(title,(10,15))
    WIN.blit(HEART, (533,3))
    if GAME_OVER:
        WIN.blit(ending,(50,175))
    
#draw and handle game objects
def draw_window(blocker,gray,orange,pink,bricks,upnext,gray_health,orange_health,pink_health,blocker_health):
    if gray_health >= 3: #GRAY
       WIN.blit(STICKMAN_GRAY_GOLD, (gray.x,gray.y))
    elif gray_health == 2:
        WIN.blit(STICKMAN_GRAY_FULL, (gray.x,gray.y))
    elif gray_health == 1:
        WIN.blit(STICKMAN_GRAY_HALF, (gray.x,gray.y))
    else:
        gray.x = -150
    if orange_health >= 3: #ORANGE
       WIN.blit(STICKMAN_ORANGE_GOLD, (orange.x,orange.y))
    elif orange_health == 2:
        WIN.blit(STICKMAN_ORANGE_FULL, (orange.x,orange.y))
    elif orange_health == 1:
        WIN.blit(STICKMAN_ORANGE_HALF, (orange.x,orange.y))
    else:
        orange.x = -150
    if pink_health >= 3: #PINK
       WIN.blit(STICKMAN_PINK_GOLD, (pink.x,pink.y))
    elif pink_health == 2:
        WIN.blit(STICKMAN_PINK_FULL, (pink.x,pink.y))
    elif pink_health == 1:
        WIN.blit(STICKMAN_PINK_HALF, (pink.x,pink.y))
    else:
        pink.x = -150

    if blocker_health >= 3: #BLOCKER
       WIN.blit(BLOCKER, (blocker.x,blocker.y))
    elif blocker_health == 2:
        WIN.blit(BLOCKER, (blocker.x,blocker.y))
    elif blocker_health == 1:
        WIN.blit(BLOCKER, (blocker.x,blocker.y))
    else:
        blocker.x = -150

    WIN.blit(BLOCKER, (blocker.x,blocker.y))

    for brick in bricks: #DRAW BRICKS
        if brick.width == BRICK_DIM: #check for brick or heart
            WIN.blit(BRICK, (brick.x,brick.y))
        elif brick.width == HEART_X:
            WIN.blit(HEART, (brick.x,brick.y))
        elif brick.width == BOMB_X:
            WIN.blit(BOMB, (brick.x,brick.y))
        else:
            print(brick.width,BRICK_DIM,HEART_X)
    for brick in upnext:
        if brick.width == BRICK_DIM:
            WIN.blit(BRICK, (brick.x,brick.y))
        elif brick.width == HEART_X:
            WIN.blit(HEART, (brick.x,brick.y))
        elif brick.width == BOMB_X:
            WIN.blit(BOMB, (brick.x,brick.y))

    pygame.display.update()

def move_stickman(obj,gray,orange,pink):
    if(random.randrange(2) == 0):
        if obj.x != STICKMAN_X1 and (obj.x - 125) not in [gray.x,orange.x,pink.x,-275]:
            obj.x -= 125
    else:
        if obj.x != STICKMAN_X5 and (obj.x + 125) not in [gray.x,orange.x,pink.x,-25]:
            obj.x += 125

def handle_bricks(bricks,blocker,gray,orange,pink):
    for brick in bricks:
        if brick.x > 640: #SPAWN BRICK
            brick.y = 80
            rand = random.randrange(5)
            if rand == 0:
                brick.x = STICKMAN_X1
            elif rand == 1:
                brick.x = STICKMAN_X2
            elif rand == 2:
                brick.x = STICKMAN_X3
            elif rand == 3:
                brick.x = STICKMAN_X4
            elif rand == 4:
                brick.x = STICKMAN_X5

        brick.y += BRICK_VEL
        #HANDLE COLLISIONS
        if brick.width == BRICK_DIM: #IF BRICK 
            if blocker.colliderect(brick): #blocker collide
                bricks.remove(brick)
            elif gray.colliderect(brick): #gray heart
                pygame.event.post(pygame.event.Event(GRAY_HIT))
                bricks.remove(brick)
            elif orange.colliderect(brick): #orange heart
                pygame.event.post(pygame.event.Event(ORANGE_HIT))
                bricks.remove(brick)
            elif pink.colliderect(brick): #pink heart
                pygame.event.post(pygame.event.Event(PINK_HIT))
                bricks.remove(brick)
            elif brick.y > HEIGHT:
                bricks.remove(brick)
        elif brick.width == HEART_X: #IF HEART            
            if blocker.colliderect(brick): #blocker collide
                bricks.remove(brick)
            elif gray.colliderect(brick): #gray heart
                pygame.event.post(pygame.event.Event(GRAY_HEART))
                bricks.remove(brick)
            elif orange.colliderect(brick): #orange heart
                pygame.event.post(pygame.event.Event(ORANGE_HEART))
                bricks.remove(brick)
            elif pink.colliderect(brick): #pink heart
                pygame.event.post(pygame.event.Event(PINK_HEART))
                bricks.remove(brick)
            elif brick.y > HEIGHT:
                bricks.remove(brick)
        elif brick.width == BOMB_X: #IF BOMB            
            if blocker.colliderect(brick): #blocker collide
                pygame.event.post(pygame.event.Event(BLOCKER_HIT))
                bricks.remove(brick)
            elif gray.colliderect(brick): #gray heart
                pygame.event.post(pygame.event.Event(GRAY_HIT))
                bricks.remove(brick)
            elif orange.colliderect(brick): #orange heart
                pygame.event.post(pygame.event.Event(ORANGE_HIT))
                bricks.remove(brick)
            elif pink.colliderect(brick): #pink heart
                pygame.event.post(pygame.event.Event(PINK_HIT))
                bricks.remove(brick)
            elif brick.y > HEIGHT:
                bricks.remove(brick)
        else: #ELSE UNKNOWN FALLING OBJECT ???
            if brick.y > HEIGHT:
                bricks.remove(brick)


def blocker_movement(keys_pressed,blocker):
    if keys_pressed[pygame.K_SPACE]:
        VEL = 15
    else:
        VEL = 5
    if keys_pressed[pygame.K_LEFT] and blocker.x - VEL > 0 and blocker.x > 0:
        blocker.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blocker.x + VEL < 640 - blocker.width and blocker.x > 0:
        blocker.x += VEL

def main():
    global NUM_SPAWN
    global SPAWN_TIMER
    global GAME_OVER
    bricks = []
    gray_health = 2
    orange_health = 2
    pink_health = 2
    blocker_health = 3
    
    blocker = pygame.Rect(15, 475, BLOCKER_X, BLOCKER_Y)
    gray = pygame.Rect(STICKMAN_X1,STICKMAN_Y, STICKMAN_WIDTH, STICKMAN_HEIGHT)
    orange = pygame.Rect(STICKMAN_X3,STICKMAN_Y, STICKMAN_WIDTH, STICKMAN_HEIGHT)
    pink = pygame.Rect(STICKMAN_X5,STICKMAN_Y, STICKMAN_WIDTH, STICKMAN_HEIGHT)

    upnext = [pygame.Rect(657,500,BRICK_DIM,BRICK_DIM),pygame.Rect(657,500,BRICK_DIM,BRICK_DIM)]
    clock = pygame.time.Clock()
    run = True
    counter = SPAWN_TIMER #ms for block to spawn
    while run:
        counter -= clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.QUIT

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    brick = pygame.Rect(STICKMAN_X1,90,BRICK_DIM,BRICK_DIM)
                    bricks.append(brick)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:
                    brick = pygame.Rect(STICKMAN_X1,90,HEART_X,HEART_Y)
                    bricks.append(brick)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT:
                    brick = pygame.Rect(STICKMAN_X1,90,BOMB_X,BOMB_Y)
                    bricks.append(brick)
        
            if event.type == GRAY_HIT:
                gray_health -= 1
            if event.type == ORANGE_HIT:
                orange_health -= 1
            if event.type == PINK_HIT:
                pink_health -= 1
            if event.type == GRAY_HEART:
                gray_health += 1
            if event.type == ORANGE_HEART:
                orange_health += 1
            if event.type == PINK_HEART:
                pink_health += 1
            if event.type == BLOCKER_HIT:
                blocker_health -= 1

        if counter < 0 and not GAME_OVER: #generate bricks on counter
            rand = random.randrange(5)
            if rand == 0:
                move_stickman(gray,gray,orange,pink)
            elif rand == 1:
                move_stickman(orange,gray,orange,pink)
            elif rand ==2:
                move_stickman(pink,gray,orange,pink)
            if rand == 0:
                item = pygame.Rect(663,500,HEART_X,HEART_Y)
            elif rand == 1:
                item = pygame.Rect(663,500,BOMB_X,BOMB_Y)
            else:
                item = pygame.Rect(663,500,BRICK_DIM,BRICK_DIM)
            upnext.append(item)
            if len(upnext) > 3:
                bricks.append(upnext.pop(0))
            upnext[0].y = 150
            upnext[1].y = 300
            upnext[2].y = 450
            NUM_SPAWN += 1
            if NUM_SPAWN % 10 == 0 and SPAWN_TIMER > 450:
                SPAWN_TIMER -=100
                if SPAWN_TIMER < 700:
                    SPAWN_TIMER += 25
                if SPAWN_TIMER < 500:
                    SPAWN_TIMER += 50
                print(SPAWN_TIMER)
            counter += SPAWN_TIMER

        if gray_health <=0:# right now this breaks the game i think
            SPAWN_TIMER -=150
        if pink_health <=0:
            SPAWN_TIMER -=150
        if orange_health <=0:
            SPAWN_TIMER -=150
        ending = ""
        if gray_health <= 0 and orange_health <= 0 and pink_health <= 0: #GAME OVER
            gameover_text = f"GAME OVER at {NUM_SPAWN}"
            ending = FONT.render(gameover_text,4,BLACK)
            GAME_OVER = True
            

        keys_pressed = pygame.key.get_pressed()
        blocker_movement(keys_pressed,blocker)
        handle_bricks(bricks,blocker,gray,orange,pink)
        draw_bg(ending)
        draw_window(blocker,gray,orange,pink,bricks,upnext,gray_health,orange_health,pink_health,blocker_health)


def start_menu():
    main()

if __name__ == "__main__":
    start_menu()

#TD
#background frame
#brick spawning
#add hearts s
#blocker health
#stickman moving
#next up sidebar
#game over GUI / restart game
#
#add hearts to each stickman
#graphics for full, half, extra heart stickmans
#stickman chance of teleports at  each brick drop

#leader board- print to txt. file to save 

#MENU GUI
#ACTUAL END OF GAME HALDING??


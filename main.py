import pygame,sys,os
import random

pygame.mixer.pre_init(44100,-16,2,512) #frequency,size,channels,buffer_szie
pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 1500,800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption('Pong')

font = pygame.font.SysFont('comicsansms',42)

BGCOLOR = pygame.Color('grey12')
light_grey = (200,200,200)


ball_size = 30
ball = pygame.Rect(SCREEN_WIDTH//2 - ball_size//2,SCREEN_HEIGHT//2 - ball_size//2,ball_size,ball_size)
player = pygame.Rect(SCREEN_WIDTH - 20,SCREEN_HEIGHT//2 - 70,10,140) #20,10
opponent = pygame.Rect(10,SCREEN_HEIGHT//2 - 70,10,140)


ball_speed_x = 7
ball_speed_y = 7


def ball_movement():
    global ball_speed_x,ball_speed_y,left_score,right_score,left_score_text,right_score_text,start_time,player_speed
    ball.x += ball_speed_x

    ball.y += ball_speed_y
    if ball.bottom >= SCREEN_HEIGHT or ball.top <= 0:
        ball_speed_y *= -1

    hit_paddle = False
    collision_tolerance_x = 10
    if ball.colliderect(player) and ball_speed_x > 0:
        pong_sound.play()
        if abs(ball.right - player.left) < collision_tolerance_x: #can only happen if hit paddle from left
            ball_speed_x *= -1
        elif abs(ball.bottom - player.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - player.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
    if ball.colliderect(opponent) and ball_speed_x < 0:
        pong_sound.play()
        if abs(ball.left - opponent.right) < collision_tolerance_x:
            ball_speed_x *= -1
        elif abs(ball.bottom - opponent.top) < 10 and ball_speed_y > 0:
            ball_speed_y *= -1
        elif abs(ball.top - opponent.bottom) < 10 and ball_speed_y < 0:
            ball_speed_y *= -1
    if not hit_paddle and ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        score_sound.play()
        if ball_speed_x < 0:
            right_score += 1
            right_score_text = font.render(f"{right_score}",True,light_grey)
        else:
            left_score += 1
            left_score_text = font.render(f"{left_score}",True,light_grey)
        
        start_time = pygame.time.get_ticks()
        ball.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)



def ball_movement_2():
    global ball_speed_x,ball_speed_y,left_score,right_score,left_score_text,right_score_text,start_time,player_speed
    ball.x += ball_speed_x
    
    if ball.colliderect(player):
        pong_sound.play()
        ball_speed_x *= -1
        ball.right = player.left
    elif ball.colliderect(opponent):
        pong_sound.play()
        ball_speed_x *= -1
        ball.left = opponent.right
    
    ball.y += ball_speed_y
    if ball.bottom >= SCREEN_HEIGHT or ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(player):
        pong_sound.play()
        if ball_speed_y < 0:
            ball.top = player.bottom
        else:
            ball.bottom = player.top
        ball_speed_y *= -1
    elif ball.colliderect(opponent):
        pong_sound.play()
        if ball_speed_y < 0:
            ball.top = opponent.bottom
        else:
            ball.bottom = opponent.top
        ball_speed_y *= -1
    

    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        score_sound.play()
        if ball_speed_x < 0:
            right_score += 1
            right_score_text = font.render(f"{right_score}",True,light_grey)
        else:
            left_score += 1
            left_score_text = font.render(f"{left_score}",True,light_grey)
        
        start_time = pygame.time.get_ticks()
        ball.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)


        



def ball_start():
    global ball_speed_x,ball_speed_y,start_time
    
    current_time = pygame.time.get_ticks()
    
    difference = current_time - start_time
    if difference > 2000:
        number_text = font.render('1',True,light_grey)
    elif difference >= 1000:
        number_text = font.render('2',True,light_grey)
    else:
        number_text = font.render('3',True,light_grey)
    
    if number_text:
        screen.blit(number_text,(SCREEN_WIDTH//2-10,SCREEN_HEIGHT//2 + 20))

    if current_time - start_time > 3000:
        ball_speed_x = random.choice((-start_ball_speed,start_ball_speed))
        ball_speed_y = random.choice((-start_ball_speed,start_ball_speed))
        start_time = None
    else:
        ball_speed_x = ball_speed_y = 0

def player_animation():
    player.y += player_y_speed 
    if player.y <= 0:
        player.y = 0
    elif player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT



def opponent_ai():
    

    if opponent.top < ball.y:
        opponent.top += opponent_speed
    elif opponent.bottom > ball.y:
        opponent.bottom -= opponent_speed

    if opponent.top <= 0:
        opponent.top = 0
    elif opponent.bottom >= SCREEN_HEIGHT:
        opponent.bottom = SCREEN_HEIGHT




left_score = right_score =  0
left_score_text = font.render('0',True,light_grey)
right_score_text = font.render('0',True,light_grey)

player_speed = 7
player_y_speed = 0
opponent_speed =7
start_ball_speed = 7

pong_sound = pygame.mixer.Sound(os.path.join('assets','pong.ogg'))
score_sound = pygame.mixer.Sound(os.path.join('assets','score.ogg'))


start_time = pygame.time.get_ticks()
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                player_y_speed += player_speed
            elif event.key == pygame.K_UP:
                player_y_speed -= player_speed
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                player_y_speed -= player_speed
            elif event.key == pygame.K_UP:
                player_y_speed += player_speed



     

    
    player_animation()
    opponent_ai()
    ball_movement()

    

    screen.fill(BGCOLOR)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
    screen.blit(left_score_text,(SCREEN_WIDTH/2 - left_score_text.get_width() - 10,5))
    screen.blit(right_score_text,(SCREEN_WIDTH/2 + 10 ,5))

    if start_time:
        ball_start()

    pygame.display.update()
    clock.tick(FPS)





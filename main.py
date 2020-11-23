import pygame,sys,os,time
import random

pygame.mixer.pre_init(44100,-16,2,512) #frequency,size,channels,buffer_szie
pygame.font.init()
pygame.init()

SCREEN_WIDTH,SCREEN_HEIGHT = 1500,800
screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
clock = pygame.time.Clock()
FPS = 60
pygame.display.set_caption('Pong')

font = pygame.font.Font(os.path.join('assets','atari.ttf'),42)

BGCOLOR = pygame.Color('grey12')
light_grey = (200,200,200)


ball_size = 30
ball = pygame.Rect(SCREEN_WIDTH//2 - ball_size//2,SCREEN_HEIGHT//2 - ball_size//2,ball_size,ball_size)
ball.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)
player = pygame.Rect(SCREEN_WIDTH - 20,SCREEN_HEIGHT//2 - 70,10,140) #20,10
opponent = pygame.Rect(10,SCREEN_HEIGHT//2 - 70,10,140)


ball_speed_x = 7
ball_speed_y = 7


def ball_movement():
    global ball_speed_x,ball_speed_y,left_score,right_score,left_score_text,right_score_text,start_time,player_speed,game_over,winner_text,info_text
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
            if right_score == 5:
                winner_text = font.render("YOU WIN!",True,light_grey)
                game_over = True
            right_score_text = font.render(f"{right_score}",True,light_grey)
        else:
            left_score += 1
            if left_score == 5:
                winner_text = font.render("COMPUTER WINS",True,light_grey)
                game_over = True
            left_score_text = font.render(f"{left_score}",True,light_grey)
        info_text = font.render("HIT ENTER TO PLAY AGAIN",True,light_grey)
        
        start_time = pygame.time.get_ticks()
        ball.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)




def ball_movement_2():
    global ball_speed_x,ball_speed_y,left_score,right_score,left_score_text,right_score_text,start_time,player_speed,previous_time,winner_text,game_over,info_text
    ball.x += ball_speed_x
    set_ball_right_to_paddle_left = False  
    set_ball_left_to_paddle_right = False  
    
    collided_x = False
    if ball.colliderect(player):
        pong_sound.play()
        ball_speed_x *= -1
        
        if ball_speed_x < 0:
            ball_speed_x = max(ball_speed_x * 1.05,-25)
        else:
            ball_speed_x = min(ball_speed_x * 1.05,25)
        set_ball_right_to_paddle_left = True
        #ball.right = player.left
        collided_x = True
    elif ball.colliderect(opponent):
        pong_sound.play()
        ball_speed_x *= -1

        if ball_speed_x < 0:
            ball_speed_x = max(ball_speed_x * 1.05,-35)
        else:
            ball_speed_x = min(ball_speed_x * 1.05,35)
        set_ball_left_to_paddle_right = True  
        ball.left = opponent.right
        collided_x = True
    ball.y += ball_speed_y
    if ball.bottom >= SCREEN_HEIGHT or ball.top <= 0:
        ball_speed_y *= -1

    if not collided_x and ball.colliderect(player):
        pong_sound.play()
        if ball_speed_y < 0:
            ball.top = player.bottom
        else:
            ball.bottom = player.top
        ball_speed_y *= -1
    elif not collided_x and ball.colliderect(opponent):
        pong_sound.play()
        if ball_speed_y < 0:
            ball.top = opponent.bottom
        else:
            ball.bottom = opponent.top
        ball_speed_y *= -1
    
    if set_ball_right_to_paddle_left:
        ball.right = player.left

    if set_ball_left_to_paddle_right:
        ball.left = opponent.right
        
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        score_sound.play()
        if ball_speed_x < 0:
            right_score += 1
            if right_score == 5:
                winner_text = font.render("YOU WIN!",True,light_grey)
                game_over = True
            right_score_text = font.render(f"{right_score}",True,light_grey)
        else:
            left_score += 1
            if left_score == 5:
                winner_text = font.render("COMPUTER WINS",True,light_grey)
                game_over = True
            left_score_text = font.render(f"{left_score}",True,light_grey)
        info_text = font.render("HIT ENTER TO PLAY AGAIN",True,light_grey)

        
        previous_time = time.time()
        ball.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

        draw()
        pygame.display.update()
        pygame.time.wait(1000)
        start_time = pygame.time.get_ticks()


        



def ball_start():
    global ball_speed_x,ball_speed_y,start_time,previous_difference
    
    current_time = pygame.time.get_ticks()
    
    difference = current_time - start_time
    if difference > 2000:
        #if previous_difference < 2000:
        #    beep_sound.play()
        number_text = font.render('1',True,light_grey)
    elif difference >= 1000:
        #if previous_difference < 1000:
        #    beep_sound.play()
        #    prevoius_difference =difference
        number_text = font.render('2',True,light_grey)
    else:
        number_text = font.render('3',True,light_grey)

    if number_text:
        screen.blit(number_text,(SCREEN_WIDTH//2-10,SCREEN_HEIGHT//2 + 20))

    if current_time - start_time > 3000:
        start_sound.play()
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

def draw():
    screen.fill(BGCOLOR)
    pygame.draw.rect(screen,light_grey,player)
    pygame.draw.rect(screen,light_grey,opponent)
    pygame.draw.ellipse(screen,light_grey,ball)
    pygame.draw.aaline(screen,light_grey,(SCREEN_WIDTH/2,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT))
    screen.blit(left_score_text,(SCREEN_WIDTH/2 - left_score_text.get_width() - 10,5))
    screen.blit(right_score_text,(SCREEN_WIDTH/2 + 10 ,5))


left_score = right_score =  0
left_score_text = font.render('0',True,light_grey)
right_score_text = font.render('0',True,light_grey)

player_speed = 7
player_y_speed = 0
opponent_speed =7
start_ball_speed = 7

pong_sound = pygame.mixer.Sound(os.path.join('assets','pong.ogg'))
score_sound = pygame.mixer.Sound(os.path.join('assets','score.ogg'))
beep_sound = pygame.mixer.Sound(os.path.join('assets','beep.ogg'))
start_sound = pygame.mixer.Sound(os.path.join('assets','start.wav'))
winner_text = info_text = None
game_over = False
start_time = pygame.time.get_ticks()
beep_sound.play()
previous_time = time.time()

while True:
    

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                left_score = right_score = 0
                left_score_text = font.render('0',True,light_grey)
                right_score_text = font.render('0',True,light_grey)
                player.centery =  opponent.centery = SCREEN_HEIGHT//2
                winner_text = None
                info_text = None
                game_over = False
                start_time = pygame.time.get_ticks()
                previous_time = time.time()
                beep_sound.play()
        elif not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    player_y_speed += player_speed
                elif event.key == pygame.K_UP:
                    player_y_speed -= player_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player_y_speed -= player_speed
                elif event.key == pygame.K_UP:
                    player_y_speed += player_speed



     

    if not game_over: 
        player_animation()
        opponent_ai()
        ball_movement_2()

    

    draw() 
    if start_time and not game_over:
        ball_start()
        if start_time:
            current_time = time.time()
            if current_time - previous_time >= 1:
                beep_sound.play()
                previous_time = current_time
    if winner_text:
        screen.blit(winner_text,(SCREEN_WIDTH//2 - winner_text.get_width()//2,SCREEN_HEIGHT//2 - winner_text.get_height()//2 - 40))
        screen.blit(info_text,(SCREEN_WIDTH//2 - info_text.get_width()//2,SCREEN_HEIGHT//2 + 40))
    pygame.display.update()
    clock.tick(FPS)





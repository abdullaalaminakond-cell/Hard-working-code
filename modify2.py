import pygame 
import random

pygame.init()
screen = pygame.display.set_mode((1000,1800))

x, y = 10, 400
x_e = random.randint(400,950)
y_e = random.randint(200,1700)

w, h = 20, 20
w_e, h_e = 40, 40

player_rect = pygame.Rect(x,y,w,h)
enemy_rect = pygame.Rect(x_e,y_e,w_e,h_e)

speed = 5
speed_e = 10

change_x = speed
change_y = 0
change_ex = speed_e
change_ey = 0

white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
green = (0,255,255)
blue=(0,0,255)
yellow=(255,255,0)
ur = pygame.Rect(500,1800,200,100)
dr = pygame.Rect(500,2000,200,100)
lr = pygame.Rect(300,1900,200,100)
rr = pygame.Rect(700,1900,200,100)
snake_list=[]
snake_l=2
enemy_list=[]
enemy_l=2
snake_colour=(red,white,green)
enemy_colour=(black,blue,yellow)
clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            hand = event.pos

            if ur.collidepoint(hand) and change_y == 0:
                change_x, change_y = 0, -speed

            if dr.collidepoint(hand) and change_y == 0:
                change_x, change_y = 0, speed

            if lr.collidepoint(hand) and change_x == 0:
                change_x, change_y = -speed, 0

            if rr.collidepoint(hand) and change_x == 0:
                change_x, change_y = speed, 0

    # player move
    x += change_x
    y += change_y
    player_rect.topleft = (x, y)
    new_colour=random.choice(snake_colour)
    snake_head=[x,y,new_colour]
    snake_list.append(snake_head)
    if len(snake_list)>snake_l:
       del snake_list[0]

    # enemy move
    x_e += change_ex
    y_e += change_ey
    enemy_rect.topleft = (x_e, y_e)
    en_colour=random.choice(enemy_colour)
    enemy_head=[x_e,y_e,en_colour]
    enemy_list.append(enemy_head)
    if len(enemy_list)>enemy_l:
       del enemy_list[0]
    
    if  x_e>1000:x_e=random.randint(10,980)
    if  x_e<0:x_e=random.randint(10,980)
    if  y_e>1000:y_e=random.randint(10,1790)
    if  y_e<0:y_e=random.randint(10,1790)
    if x >1000:x=0
    if x<0: x=1000
    if y>1000:y=0
    if y<0:y=1000
        
    # collision 🔥
    if player_rect.colliderect(enemy_rect):
        x_e = random.randint(0,1000)
        y_e = random.randint(0,1800)
        enemy_rect.topleft = (x_e, y_e)
        snake_l +=1
        enemy_l +=1

    # draw
    screen.fill(black)
    
    for segment in snake_list:
        pygame.draw.rect(screen, segment[2], [segment[0], segment[1], w, h])
    for j in enemy_list:
    
         pygame.draw.rect(screen,j[2],[j[0],j[1],w_e,h_e])

    pygame.draw.rect(screen, white, ur)
    pygame.draw.rect(screen, white, dr)
    pygame.draw.rect(screen, white, lr)
    pygame.draw.rect(screen, white, rr)

    pygame.display.update()
    clock.tick(30)

pygame.quit()
import pygame 
import random
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((1000, 1400))

# --- মিউজিক লিস্ট ---
music_list = [
    "/storage/emulated/0/vidmate/download/1.mp3",
    "/storage/emulated/0/vidmate/download/2.mp3",
    "/storage/emulated/0/vidmate/download/3.mp3",
    "/storage/emulated/0/vidmate/download/4.mp3",
    "/storage/emulated/0/vidmate/download/5.mp3",
    "/storage/emulated/0/vidmate/download/6.mp3",
    "/storage/emulated/0/vidmate/download/7.mp3",
]

if music_list:
    try:
        pygame.mixer.music.load(random.choice(music_list))
        pygame.mixer.music.play(-1)
    except:
        pass

font = pygame.font.SysFont("Arial", 50)
score = 0

x, y = 10, 400
x_e, y_e = random.randint(400, 950), random.randint(200, 1300)
w, h = 30, 30
w_e, h_e = 20, 20

player_rect = pygame.Rect(x, y, w, h)
enemy_rect = pygame.Rect(x_e, y_e, w_e, h_e)

speed, speed_e = 13, 10
change_x, change_y = speed, 0
change_ex, change_ey = speed_e, 0

white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
green, blue, yellow = (0, 255, 0), (0, 0, 255), (255, 255, 0)

# Controls
ur, dr = pygame.Rect(500, 1500, 200, 100), pygame.Rect(500, 1700, 200, 100)
lr, rr = pygame.Rect(300, 1600, 200, 100), pygame.Rect(700, 1600, 200, 100)

snake_list, snake_l = [], 2
enemy_list, enemy_l = [], 2 
snake_colour = (red, white, green)
enemy_colour = (black, blue, yellow)
clock = pygame.time.Clock()

circle_active = False
circle_pos = [0, 0]
circle_radius = 30
circle_timer = 0
spawn_time = 650  
delete_circle=70

# New Features
yellow_active = False
yellow_pos = [0, 0]
yellow_time=0
yellow_delete=60
friend_active = False
friend_body = []
friend_len = 100
frind_speed=7
invincible = False
invincible_timer = 0

boss_snakes = []
boss_active = False
boss_speed = 10
boss_timer = 0
boss_target_time = 350
level = 0

run = True
enemy_timer = 0

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            hand = event.pos
            if ur.collidepoint(hand) and change_y == 0: change_x, change_y = 0, -speed
            if dr.collidepoint(hand) and change_y == 0: change_x, change_y = 0, speed
            if lr.collidepoint(hand) and change_x == 0: change_x, change_y = -speed, 0
            if rr.collidepoint(hand) and change_x == 0: change_x, change_y = speed, 0

    enemy_timer += 1
    if enemy_timer > 20:
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        if direction == 'UP': change_ex, change_ey = 0, -speed_e
        elif direction == 'DOWN': change_ex, change_ey = 0, speed_e
        elif direction == 'LEFT': change_ex, change_ey = -speed_e, 0
        elif direction == 'RIGHT': change_ex, change_ey = speed_e, 0
        enemy_timer = 0

    x += change_x
    y += change_y
    player_rect.topleft = (x, y)
    
    x_e += change_ex
    y_e += change_ey
    enemy_rect.topleft = (x_e, y_e)

    if invincible:
        invincible_timer -= 1
        if invincible_timer <= 0: invincible = False

    # Purple Circle
    circle_timer += 1
    if not circle_active and circle_timer > spawn_time:
        circle_pos = [random.randint(50, 950), random.randint(50, 1350)]
        circle_active = True
        circle_timer = 0
        delete_circle=0
    else:
    	delete_circle+=1
    	if delete_circle>70:
            circle_active=False

    
    if circle_active:
        if player_rect.colliderect(pygame.Rect(circle_pos[0]-30, circle_pos[1]-30, 60, 60)):
            # 🔥 Song change logic eibar thikmote trigger hobo
            if music_list:
                try:
                    pygame.mixer.music.load(random.choice(music_list))
                    pygame.mixer.music.play(-1)
                except:
                    pass
            
            circle_active = False
            level += 1
            boss_active = True
            boss_timer = 0
            boss_snakes = []
            for i in range(level):
                bx, = random.randint(0, 900)
                by=-50
                boss_snakes.append({"body": [[bx, by]], "length": 100})
            
            # Boss asile yellow circle asibo
            yellow_pos = [random.randint(50, 950), random.randint(50, 1300)]
            yellow_active = True
            yellow_delete=0
    yellow_delete+=1
    if yellow_delete>150:
         yellow_active=False
         yellow_delete=0
            

    # Yellow Circle logic
    if yellow_active:
        if player_rect.colliderect(pygame.Rect(yellow_pos[0]-30, yellow_pos[1]-30, 60, 60)):
            yellow_active = False
            friend_active = True
            invincible = True
            invincible_timer = 150 
            friend_body = [[500 ,0]]
            yellow_active=0
        
         	

    # Snake update
    snake_head = [x, y, random.choice(snake_colour)]
    snake_list.append(snake_head)
    if len(snake_list) > snake_l: del snake_list[0]

    enemy_head = [x_e, y_e, random.choice(enemy_colour)]
    enemy_list.append(enemy_head)
    if len(enemy_list) > enemy_l: del enemy_list[0]

    if player_rect.colliderect(enemy_rect):
        x_e, y_e = random.randint(0, 900), random.randint(0, 1300)
        snake_l += 2
        score += 1
    for segment in snake_list[:-1]:
    	if segment==snake_head:
    		run=False
    # Boss & Friend Logic
    if boss_active:
        boss_timer += 1
        for boss in boss_snakes:
            b_head = boss["body"][-1]
            bx, by = b_head[0], b_head[1]
            if bx < x: bx += boss_speed
            elif bx > x: bx -= boss_speed
            if by < y: by += boss_speed
            elif by > y: by -= boss_speed
            boss["body"].append([bx, by])
            if len(boss["body"]) > boss["length"]: del boss["body"][0]
            
            if not invincible:
                for part in boss["body"]:
                    if player_rect.colliderect(pygame.Rect(part[0], part[1], 30, 30)): run = False

        if friend_active and boss_snakes:
            fx, fy = friend_body[-1][0], friend_body[-1][1]
            target = boss_snakes[0]["body"][-1]
            if fx < target[0]: fx += frind_speed
            elif fx > target[0]: fx -= frind_speed
            if fy < target[1]: fy += frind_speed
            elif fy > target[1]: fy -= frind_speed
            friend_body.append([fx, fy])
            if len(friend_body) > friend_len: del friend_body[0]
            
            f_rect = pygame.Rect(fx, fy, 30, 30)
            for b in boss_snakes[:]:
                if f_rect.colliderect(pygame.Rect(b["body"][-1][0], b["body"][-1][1], 30, 30)):
                    boss_snakes.remove(b)
                    score += 500

        if boss_timer > boss_target_time or not boss_snakes:
            boss_active = False
            friend_active = False
            yellow_active = False
       
      
    # Border logic
    if x > 1000: x = 0
    elif x < 0: x = 1000
    if y > 1400: y = 0
    elif y < 0: y = 1400
    
    if x_e > 1000: x_e = 0
    elif x_e < 0: x_e = 1000
    if y_e > 1400: y_e = 0
    elif y_e < 0: y_e = 1400

    # DRAWING
    screen.fill(black)
    
    if circle_active: pygame.draw.circle(screen, (255, 0, 255), circle_pos, 30)
    if yellow_active: pygame.draw.circle(screen, yellow, yellow_pos, 30)
    
    for segment in snake_list:
        pygame.draw.rect(screen, segment[2], [segment[0], segment[1], w, h])
    
    for j in enemy_list:
        pygame.draw.rect(screen, j[2], [j[0], j[1], w_e, h_e])
    
    if boss_active:
        for boss in boss_snakes:
            for part in boss["body"]: pygame.draw.rect(screen, (255, 0, 255), [part[0], part[1], 30, 30])
    
    if friend_active:
        for part in friend_body: pygame.draw.rect(screen, green, [part[0], part[1], 30, 30])

    score_text = font.render(f"Score: {score}", True, white)
    screen.blit(score_text, (50, 50))
    
    for btn in [ur, dr, lr, rr]: pygame.draw.rect(screen, white, btn)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

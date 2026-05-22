import pygame 
import random
import time

pygame.init()
screen = pygame.display.set_mode((1000, 1400))

x, y = 10, 400
x_e, y_e = random.randint(400, 950), random.randint(200, 1300)

w, h = 40, 40
w_e, h_e = 20, 20

player_rect = pygame.Rect(x, y, w, h)
enemy_rect = pygame.Rect(x_e, y_e, w_e, h_e)

speed, speed_e = 20, 10
change_x, change_y = speed, 0
change_ex, change_ey = speed_e, 0

white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
green, blue, yellow = (0, 255, 255), (0, 0, 255), (255, 255, 0)

# বাটন পজিশন
ur, dr = pygame.Rect(500, 1500, 200, 100), pygame.Rect(500, 1700, 200, 100)
lr, rr = pygame.Rect(300, 1600, 200, 100), pygame.Rect(700, 1600, 200, 100)

snake_list, snake_l = [], 2
enemy_list, enemy_l = [], 2
snake_colour = (red, white, green)
enemy_colour = (black, blue, yellow)
clock = pygame.time.Clock()

# --- নতুন ভ্যারিয়েবল (Circle logic) ---
circle_active = False
circle_pos = [0, 0]
circle_radius = 30
circle_timer = 0
spawn_time = 500  # কতক্ষণ পর পর সার্কেল আসবে (ফ্রেম সংখ্যা)
visible_time = 30 # কতক্ষণ সার্কেলটি স্ক্রিনে থাকবে

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

    # এনিমি মুভমেন্ট
    enemy_timer += 1
    if enemy_timer > 20:
        direction = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        if direction == 'UP': change_ex, change_ey = 0, -speed_e
        elif direction == 'DOWN': change_ex, change_ey = 0, speed_e
        elif direction == 'LEFT': change_ex, change_ey = -speed_e, 0
        elif direction == 'RIGHT': change_ex, change_ey = speed_e, 0
        enemy_timer = 0

    # প্লেয়ার এবং এনিমি মুভমেন্ট আপডেট
    x += change_x
    y += change_y
    player_rect.topleft = (x, y)
    
    x_e += change_ex
    y_e += change_ey
    enemy_rect.topleft = (x_e, y_e)

    # সার্কেল স্পন লজিক (Circle Spawn Logic)
    circle_timer += 1
    if not circle_active and circle_timer > spawn_time:
        circle_pos = [random.randint(50, 950), random.randint(50, 1350)]
        circle_active = True
        circle_timer = 0
    elif circle_active and circle_timer > visible_time:
        circle_active = False
        circle_timer = 0

    # স্নেক যখন সার্কেল টাচ করবে (Collision with Circle)
    if circle_active:
        circle_rect = pygame.Rect(circle_pos[0]-circle_radius, circle_pos[1]-circle_radius, circle_radius*2, circle_radius*2)
        if player_rect.colliderect(circle_rect):
            snake_l *= 2  # স্নেকের দৈর্ঘ্য ডাবল হবে
            circle_active = False
            circle_timer = 0

    # স্নেক বডি আপডেট
    snake_head = [x, y, random.choice(snake_colour)]
    snake_list.append(snake_head)
    if len(snake_list) > snake_l: del snake_list[0]

    enemy_head = [x_e, y_e, random.choice(enemy_colour)]
    enemy_list.append(enemy_head)
    if len(enemy_list) > enemy_l: del enemy_list[0]

    # বাউন্ডারি চেকিং
    if x_e > 1000: x_e = 0
    elif x_e < 0: x_e = 1000
    if y_e > 1400: y_e = 0
    elif y_e < 0: y_e = 1400
    
    if x > 1000: x = 0
    elif x < 0: x = 1000
    if y > 1400: y = 0
    elif y < 0: y = 1400

    # এনিমি কলিশন
    if player_rect.colliderect(enemy_rect):
        x_e, y_e = random.randint(0, 900), random.randint(0, 1300)
        snake_l += 2

    # ড্রয়িং
    screen.fill(black)
    
    # সার্কেল আঁকা
    if circle_active:
        pygame.draw.circle(screen, (255, 0, 255), circle_pos, circle_radius) # ম্যাজেন্টা রঙের সার্কেল
    
    for segment in snake_list:
        pygame.draw.rect(screen, segment[2], [segment[0], segment[1], w, h])
    
    for segment in snake_list[:-1]:
        if segment[0] == x and segment[1] == y:
            run = False

    for j in enemy_list:
        pygame.draw.rect(screen, j[2], [j[0], j[1], w_e, h_e])

    # বাটন
    for btn in [ur, dr, lr, rr]: pygame.draw.rect(screen, white, btn)

    pygame.display.update()
    clock.tick(30)

pygame.quit()

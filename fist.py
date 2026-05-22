import pygame
import random
pygame.init()
screen=pygame.display.set_mode((1000,1800))
w=20
h=20
x=10
y=600
speed=5

change_x=speed
change_y=0
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
black=(0,0,0)
white=(255,255,255)
colours=[red,green,blue]

ur=pygame.Rect(500,1800,200,100)
dr=pygame.Rect(500,2000,200,100)
lr=pygame.Rect(300,1900,200,100)
rr=pygame.Rect(700,1900,200,100)
f_x=random.randint(10,960)
f_y=random.randint(10,1350)
f_r=pygame.Rect(f_x,f_y,w,h)
pl_r=pygame.Rect(x,y,w,h)


snake_list=[]
snake_l=10
clock=pygame.time.Clock()
run=True
while run:
   
   for event in pygame.event.get():
	 
	     if event.type==pygame.QUIT:
	     	run=False
	     if event.type==pygame.MOUSEBUTTONDOWN:
        	hand=event.pos
        	if ur.collidepoint(hand) and change_y==0:
        	   change_x,change_y=0,-speed
        	if dr.collidepoint(hand) and change_y==0:
        		change_x,change_y=0,speed
        	if lr.collidepoint(hand) and change_x==0:
        		change_x,change_y=-speed,0
        	if rr.collidepoint(hand) and change_x==0:
        		change_x,change_y=speed,0
   x=x+change_x
   y=y+change_y
  
   pl_r.topleft=(x,y)
   if x>1000:x=0
   if x<0:x=1000
   if y>1800:y=0
   if y<0:y=1800
   snake_head=[x,y,red]
   snake_list.append(snake_head)
   if len(snake_list)>snake_l:
       del snake_list[0]
   if pl_r.colliderect(f_r):	
      f_x=random.randint(10,950)
      f_y=random.randint(10,1350)
      f_r.topleft=(f_x,f_y)
      
      snake_l += 1
      
   screen.fill(black)
   pygame.draw.rect(screen,red,ur)
   pygame.draw.rect(screen,red,dr)
   pygame.draw.rect(screen,red,lr)
   pygame.draw.rect(screen,red,rr)
   for i in snake_list:
    pygame.draw.rect(screen, i[2], [i[0], i[1], w, h])
        
   pygame.draw.rect(screen,blue,f_r)
   clock.tick(30)
   
   pygame.display.update()
pygame.quit()
      
  
         		
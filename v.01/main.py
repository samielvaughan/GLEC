#!/usr/bin/env python

#Origina Code by Samiel Vaughan
#licened under the GPL v3


import os,sys,pygame
from pygame.locals import *
from screen import clock, screen
from pics import rock, timgs
from units import massx, massy
import socket
import string
#getting the world
from focus import *
import time



HOME_FOLDER = os.environ['homepath']

dx = dy = 0
xback = 0
yback = 0
run = False
dash = False

real = focus()

screen_rect = screen.get_rect()
camera = screen_rect.copy()
frame = 0
#starting the loop
while True:
    frame += 1
    
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_q:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_UP:
            dy = -1
        elif event.type == KEYDOWN and event.key == K_DOWN:
            dy = 1
        elif event.type == KEYDOWN and event.key == K_LEFT:
            dx = -1
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            dx = 1
        elif event.type == KEYUP and event.key == K_UP:
            dy = 0
        elif event.type == KEYUP and event.key == K_DOWN:
            dy = 0
        elif event.type == KEYUP and event.key == K_LEFT:
            dx = 0
        elif event.type == KEYUP and event.key == K_RIGHT:
            dx = 0
        elif event.type == KEYDOWN and event.key == K_r:
            run = True
        elif event.type == KEYUP and event.key == K_r:
            run = False
        elif event.type == KEYDOWN and event.key == K_t:
            dash = True
        elif event.type == KEYUP and event.key == K_t:
            dash = False
        elif event.type == KEYDOWN and event.key == K_s:
            pygame.image.save(real.img, \Desktop\world"+str(frame)+".png" )


    screen.fill(Color('black'))
    real.update(dx, dy, run, dash)

    screen.blit(real.img, real.pos)
#    screen.blit(sams_health.img, sams_health.position)

    pygame.display.update()
















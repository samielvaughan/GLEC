import os,sys,pygame
from pygame.locals import *
import pygame.mixer
import random
import var, const

class loop(object):
    def __init__(self)
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((const.LARGE_X, const.LARGE_Y),0,32)
        #pygame.display.set_icon(icon)
        pygame.display.set_caption('Good Luck, Ebola Chan! (No cure, for love!)')
        self.frame = 0

        #detecting the change in directions Delta_x is horizontal movement, Delta_y is vertical
        #positive x is to the right, positive y is down
        var.Delta_x = 0
        var.Delta_y = 0

        #Variables to make the character move
        var.run = False
        var.Dash = False

        self.camera = focus.focus()


        
    def run(self):
    #starting the loop
        while True:
            self.frame += 1
            
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_q:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN and event.key == K_UP:
                    self.Delta_y = -1
                elif event.type == KEYDOWN and event.key == K_DOWN:
                    self.Delta_y = 1
                elif event.type == KEYDOWN and event.key == K_LEFT:
                    self.Delta_x = -1
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    self.Delta_x = 1
                elif event.type == KEYUP and event.key == K_UP:
                    self.Delta_y = 0
                elif event.type == KEYUP and event.key == K_DOWN:
                    self.Delta_y = 0
                elif event.type == KEYUP and event.key == K_LEFT:
                    self.Delta_x = 0
                elif event.type == KEYUP and event.key == K_RIGHT:
                    self.Delta_x = 0
                elif event.type == KEYDOWN and event.key == K_r:
                    run = True
                elif event.type == KEYUP and event.key == K_r:
                    run = False
                elif event.type == KEYDOWN and event.key == K_t:
                    dash = True
                elif event.type == KEYUP and event.key == K_t:
                    dash = False
                elif event.type == KEYDOWN and event.key == K_s:
                    pygame.image.save(real.img, const.HOME + "/"+str(frame)+".png" )
        
        
            self.screen.fill(Color('black'))
            real.update(dx, dy, run, dash)
        
            screen.blit(real.img, real.pos)
        
            pygame.display.update()
        
        
        
                

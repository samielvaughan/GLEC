import pygame
from pygame.locals import *
import cons,var

#this is the mob class which will be used to determine all the characteristics of
#moving characters, also it's pronounced "Mobe" because it's short for mobile
class mob(pygame.sprite.Sprite):
    def __init__(self, spritelist):
        self.ani_speed_init=5
        self.ani_speed = self.ani_speed_init

        self.sprites = spritelist

        #the direction that the mob is facing
        #more can be added for additional directions later
        #0 = down
        #1 = up
        #2 = left
        #4 = right
        self.direction = 0
        self.speed = 1

        #the current frame of the animation
        #if x and y speed hits 0 then so does frame (standing)
        self.frame = 0
        self.frame_max = var.frame_max

        self.injury_timer_init = 100
        self.injury_timer = self.injury_timer_init
        self.life = 20
        
        self.rect = pygame.Rect(0,0,const.SCALE, const.SCALE)

        self.player = False
        self.type = False

    def pos_update(self, x_speed, y_speed):
        if x_speed == 0 or y_speed == 0 and self.frame != 0:
            self.frame = 0
        else if x_speed != 0 or y_speed != 0:
            self.ani_speed -= 1
            if self.ani_speed <= 0:
                self.frame += 1
                self.ani_speed = ani_speed_init
                if self.frame == self.frame_max:
                    self.frame = 0
            if x_speed < 

        x_back = self.rect.left
        y_back = self.rect.top

        self.rect.move(self.rect.left+x_speed,self.rect.top+y_speed)
        
        move = True
        for item in var.solid_array:
            if self.rect.colliderect(item):
                self.rect.move(x_back,y_back)
                move = False
                break

        if move:
            for mob in var.mob_array:
                if self.rect.colliderect(mob):
                    self.rect.move(x_back,y_back)
                    break


    def getpos(self):
        return self.rect

    def set_pos(self, x, y):
        self.rect.move(x,y)

    def set_type(self, new_type):
        self.type = new_type


























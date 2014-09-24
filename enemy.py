#!/usr/bin/env python

import os,sys,pygame
from pygame.locals import *
import pygame.mixer
import glob
import string
import random
from units import *
from pics import * 

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((massx,massy),0,32)
sizex,sizey = screen.get_size()

class enemy(pygame.sprite.Sprite):
    def __init__(self,xdash,ydash, mtype):
        pygame.sprite.Sprite.__init__(self)
        self.x = random.randrange(0+xdash,massx+xdash)
        self.y = random.randrange(0+ydash,massy+ydash)
        self.ani_speed_init = 10
        self.ani_speed = self.ani_speed_init
        exec 'self.anidown = '+mtype+'down'
        exec 'self.aniup = '+mtype+'up'
        exec 'self.anileft = '+mtype+'left'
        exec 'self.aniright = '+mtype+'right'

        if mtype == 0:
            self.assault = 1
        else:
            self.assault = -1

        self.anidown_pos = 0
        self.aniup_pos = 0
        self.anileft_pos = 0
        self.aniright_pos = 0
        self.anidown_max = len(self.anidown)-1
        self.aniup_max = len(self.aniup)-1
        self.anileft_max = len(self.anileft)-1
        self.aniright_max = len(self.aniright)-1
        self.img = self.anidown[0]
        self.rect = self.img.get_rect()
        self.rect.x, self.rect.y = (self.x,self.y)
        self.rectx = self.x + SIZE*2
        self.recty = self.y + SIZE*2
        self.rect.centerx, self.rect.centery = (self.x,self.y)
        self.approachx = 0
        self.approachy = 0
        self.speed = SIZE*random.randrange(10.0,190.0)/100.00
#        self.speed = 1
        self.destroy = False
        self.life = 10

    def update(self,pos,Solids,xdash,ydash,shotsfired):
        for shot in shotsfired:
            if self.rect.colliderect(shot):
                self.life -= 1
        suffer = random.randrange(0,60)
        if suffer == 15:
            self.life -= 1
        posx,posy = pos
        if self.life <= 0:
            self.destroy = True
        listx = [posx,self.x]
        listy = [posy,self.y]

        listx.sort()
        listy.sort()

        newx = listx[1] - listx[0]
        newy = listy[1] - listy[0]

        if newx > newy:
            if self.x < posx:
                self.movement(self.speed,0,Solids,xdash,ydash)
            else:
                self.movement(-self.speed,0,Solids,xdash,ydash)

        else:
            if self.y < posy:
                self.movement(0,self.speed,Solids,xdash,ydash)
            else:
                self.movement(0,-self.speed,Solids,xdash,ydash)

    def movement(self,xpos,ypos,Solids,xdash,ydash):
        if ypos > 0:
            self.ani_speed-=1.5
            if self.ani_speed<=0:
                self.img = self.anidown[self.anidown_pos]
                self.ani_speed=self.ani_speed_init
                if self.anidown_pos == self.anidown_max:
                    self.anidown_pos = 0
                else:
                    self.anidown_pos+=self.assault
        if ypos < 0:
            self.ani_speed-=1.5
            if self.ani_speed<=0:
                self.img = self.aniup[self.aniup_pos]
                self.ani_speed=self.ani_speed_init
                if self.aniup_pos == self.aniup_max:
                    self.aniup_pos = 0
                else:
                    self.aniup_pos+=self.assault
        if xpos < 0:
            self.ani_speed-=1.5
            if self.ani_speed<=0:
                self.img = self.anileft[self.anileft_pos]
                self.ani_speed=self.ani_speed_init
                if self.anileft_pos == self.anileft_max:
                    self.anileft_pos = 0
                else:
                    self.anileft_pos+=self.assault
        if xpos > 0:
            self.ani_speed-=1.5
            if self.ani_speed<=0:
                self.img = self.aniright[self.aniright_pos]
                self.ani_speed=self.ani_speed_init
                if self.aniright_pos == self.aniright_max:
                    self.aniright_pos = 0
                else:
                    self.aniright_pos+=self.assault

        self.x += xpos + xdash
        self.y += ypos + ydash
        self.rect = Rect(self.rectx,self.recty,SIZE*10,SIZE*13)
        self.rectpos = SIZE*3
        self.rectx = self.x + self.rectpos
        self.recty = self.y + self.rectpos
        self.rect.x, self.rect.y = (self.rectx,self.recty)

        for solid in Solids:
            if self.rect.colliderect(solid):
                if ypos < 0: 
                    self.rect.top = solid.getsize().bottom
                    self.x,self.y = (self.rect.x-self.rectpos, self.rect.y-self.rectpos)
                if ypos > 0: 
                    self.rect.bottom = solid.getsize().top
                    self.x,self.y = (self.rect.x-self.rectpos, self.rect.y-self.rectpos)
                if xpos < 0:
                    self.rect.left = solid.getsize().right
                    self.x,self.y = (self.rect.x-self.rectpos, self.rect.y-self.rectpos)
                if xpos > 0:
                    self.rect.right = solid.getsize().left
                    self.x,self.y = (self.rect.x-self.rectpos, self.rect.y-self.rectpos)

#        pygame.draw.rect(screen, (25, 255, 255), self.rect)
        screen.blit(self.img, (self.x,self.y))

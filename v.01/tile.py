from units import scale
from screen import screen
import pygame
import const

class tile(object):

    def __init__(self, x, y, item, solid, portal):
        self.img = item
        self.rect = self.img.get_rect(topleft=(x*scale,y*scale))
        self.hard = solid
        self.portal = portal
        self.player = False
        self.x = x*const.SCALE
        self.y = y*const.SCALE
        self.position = (self.x, self.y)

    def updatex(self,xmove):
        self.x -= xmove
        self.rect.x = self.x

    def updatey(self,xmove):
        self.y -= xmove
        self.rect.y = self.y



    


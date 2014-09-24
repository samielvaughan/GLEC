import os,sys,pygame
from pygame.locals import *
from screen import clock, screen
from pics import rock, timgs
from world import world1
from units import massx, massy, scale
#getting the world
from chunk import chunk

class focus(object):
    
    def __init__(self):
        self.real = chunk(world1)
        self.img = pygame.Surface((massx, massy - scale * 2))
        self.pos = (0, scale * 2)
        self.img.blit(self.real.img, self.real.p_pos)

    def update(self, xmove, ymove, run, dash):
        self.real.update(xmove, ymove, run, dash)
        self.img.blit(self.real.img, self.real.p_pos)







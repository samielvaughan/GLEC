import os,sys,pygame
from pygame.locals import *
import pygame.mixer
import random

class loop(object):
    def __init__(self, scale, offsetx, offsety, massx, massy)
        pygame.init()
        clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((massx,massy),0,32)
        self.sizex = massx
        self.sizey = massy
        #pygame.display.set_icon(icon)
        pygame.display.set_caption('Good Luck, Ebola Chan! (No cure, for love!)')
        

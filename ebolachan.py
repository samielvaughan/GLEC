import pygame
from pygame.locals import *
import const, var

class player(object):

    def __init__(self, x, y):

        self.player = True
        var.player_rect = self.rect

    def update(self):
        if run:
            x_speed = var.Delta_x * 2
            y_speed = var.Delta_y * 2
        else:
            x_speed = var.Delta_x
            y_speed = var.Delta_y
        self.pos_update(var.Delta_x,var.Delta_y)
        var.player_rect.move(self.rect.left, self.rect.top)






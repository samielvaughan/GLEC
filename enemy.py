import pygame
from pygame.locals import *
import const, var

class player(object):

    def __init__(self, ):

        self.player = False
        self.aggressor = True

    #this is the update function which I intend to extend later with a proper AI with pathfinding
    #both victim and attacker will be derived from this class
    def update(self):
        
        dist_x = [self.rect.left,var.player_rect.left].sort()[1] - [self.rect.left,var.player_rect.left].sort()[0]
        dist_y = [self.rect.top,var.player_rect.top].sort()[1] - [self.rect.top,var.player_rect.top].sort()[0]

        if dist_x > dist_y:
            if self.rect.left < var.player_rect.left:
                if self.aggressor:
                    x_speed = self.speed
                else:
                    x_speed = -self.speed
            else:
                if self.aggressor:
                    x_speed = -self.speed
                else:
                    x_speed = self.speed
        else if dist_y < dist_x:
            if self.rect.top < var.player_rect.top:
                if self.aggressor:
                    y_speed = self.speed
                else:
                    y_speed = -self.speed
            else:
                if self.aggressor:
                    y_speed = -self.speed
                else:
                    y_speed = self.speed
        else:
            if self.rect.top < var.player_rect.top:
                if self.aggressor:
                    y_speed = self.speed
                else:
                    y_speed = -self.speed
            else:
                if self.aggressor:
                    y_speed = -self.speed
                else:
                    y_speed = self.speed        
        self.pos_update(x_speed, y_speed)






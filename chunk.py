import ebolachan
from pics import rock, grass, wood
from tile import tile
from units import massx, massy, scale
import pygame
from pygame.locals import *
from world import world1, world2
import enemy

player1 = ebolachan.player(world1[0][0] / 2, world1[0][1] / 2)


class chunk(object):

    def __init__(self, world):
        self.world = world
        self.img = pygame.Surface((self.world[0][0] * scale, self.world[0][1] * scale))
        self.world[1].append(player1)
        for i in self.world[1]:
            self.img.blit(i.img,i.position)
        #self.p_pos = ( - player1.position[0] + massx / 2 - scale / 2,(self.world[0][0] * scale, self.world[0][1] * scale) - player1.position[1] + massy / 2 - scale / 2 )
    	self.p_pos = (50,50)
        #self.WHO = enemy.enemy(30,30,"who")
        #self.NOG = enemy.enemy(60,60,"nog")

    def update(self, xmove, ymove, run, dash):
        # this moves the player
        player1.updatex(xmove, run, dash, self.world)
        player1.updatey(ymove, run, dash, self.world)
        #this tracks the players movements
        self.p_pos = ( - player1.position[0] + massx / 2 - scale / 2 - xmove, - player1.position[1] + massy / 2 - scale / 2 - ymove)
        

        # this fills the void
        self.img.fill(Color('black'))

        # this makes the plain
        for i in self.world[1]:
            self.img.blit(i.img,i.position)

























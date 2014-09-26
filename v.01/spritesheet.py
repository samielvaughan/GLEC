from pygame import Rect, Surface
import pygame
import os
from units import massx, massy, SIZE, scale

pygame.init()
screen = pygame.display.set_mode((massx,massy),0,32)

spritesheet = pygame.transform.scale(pygame.image.load(os.path.join('../res','spritesheet.png')).convert_alpha(),(SIZE*256,SIZE*256))

sprites = []
for x in xrange(spritesheet.get_width()/scale):
    list1 = []
    for y in xrange(spritesheet.get_height()/scale):
        list1.append(spritesheet.subsurface(Rect(x*scale,y*scale,scale,scale)))
    sprites.append(list1)

icon = sprites[8][4]
end = pygame.transform.scale(pygame.image.load(os.path.join("../res", "end.png")).convert_alpha(),screen.get_size())
map1 = pygame.image.load(os.path.join("../res", "map1.png")).convert_alpha()
grass = sprites[2][4]
wood = sprites[6][4]
portal = sprites[6][5]
grid = sprites[9][4]
dirt = sprites[4][4]
dtg1 = sprites[2][5]
dtg2 = sprites[3][5]
rock = sprites[3][4]
blast = sprites[7][4]
heart = sprites[1][4]
eheart = sprites[0][4]

playerdown = [sprites[7][3],sprites[6][3],sprites[7][3],sprites[8][3]]
playerup = [sprites[1][3],sprites[0][3],sprites[1][3],sprites[2][3]]
playerleft = [pygame.transform.flip(sprites[4][3],1,0),
                    pygame.transform.flip(sprites[3][3],1,0),
                    pygame.transform.flip(sprites[4][3],1,0),
                    pygame.transform.flip(sprites[5][3],1,0)]
playerright = [sprites[4][3],sprites[3][3],sprites[4][3],sprites[5][3]]

whodown = [sprites[8][0],sprites[6][0],sprites[8][0],sprites[7][0]]
whoright = [sprites[9][0],sprites[10][0],sprites[9][0],sprites[11][0]]
wholeft = [sprites[3][0],sprites[4][0],sprites[3][0],sprites[5][0]]
whoup = [sprites[2][0],sprites[1][0],sprites[2][0],sprites[0][0]]

nogdown = [sprites[7][2],sprites[8][2],sprites[9][2]]
nogup = [sprites[10][2],sprites[11][2],sprites[12][2]]
nogleft = [pygame.transform.flip(sprites[0][2],1,0),
            pygame.transform.flip(sprites[1][2],1,0),
            pygame.transform.flip(sprites[2][2],1,0),
            pygame.transform.flip(sprites[3][2],1,0),
            pygame.transform.flip(sprites[4][2],1,0),
            pygame.transform.flip(sprites[5][2],1,0),
            pygame.transform.flip(sprites[6][2],1,0)]
nogright = [sprites[0][2],sprites[1][2],sprites[2][2],
              sprites[3][2],sprites[4][2],sprites[5][2],sprites[6][2]]

tdown = [sprites[7][1],sprites[6][1],sprites[7][1],sprites[8][1]]
tup = [sprites[0][1],sprites[1][1],sprites[0][1],sprites[2][1]]
tleft = [pygame.transform.flip(sprites[4][1],1,0),
            pygame.transform.flip(sprites[3][1],1,0),
            pygame.transform.flip(sprites[4][1],1,0),
            pygame.transform.flip(sprites[5][1],1,0)]
tright = [sprites[4][1],sprites[3][1],sprites[4][1],sprites[5][1]]

timgs = [tdown, tup, tleft, tright]



from pics import icon as icon
from units import massx as massx, massy as massy
import pygame

pygame.init()

#doing a clock thing
clock = pygame.time.Clock()

#making the screen
screen = pygame.display.set_mode((massx, massy), 0, 32)
#screen = pygame.display.toggle_fullscreen()

#making it purdy
pygame.display.set_icon(icon)
pygame.display.set_caption('Good Luck, Ebola Chan!')


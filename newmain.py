#!/usr/bin/env python2

import os, sys

import const, var
import loop

__doc__="""This is "Good Luck, Ebola-Chan!" The game where you play as Ebola-Chan to infect people and try to end the world
You get points country by country and try to infect as many people as possible, but if the WHO Doctors catch and kill you then your victory/loss will depend on how well your choices to this point have been.

Main.py sets the constants for the game, const, and var allows different modules and classes to use constants and variables easily

"""

#const is a module which provides immutable constant functionality and allows all modules which import const to access all values assigned by all other modules
#var does the same thing but allows value reassignment

#units determine how many pixels accross the sprites are, size determines the scale 1= normal, 2 = double in size, 3 = triple in size
const.UNITS = 16
const.SIZE = 1
const.SCALE = const.UNITS * const.SIZE

#the homepath variable is obtained to allow read/write access to files contained within so that the game can save data persistantly take screenshots of the game
const.HOME_FOLDER = os.environ['homepath']

#this is the offset of the screen which I completely forget why I have
#it will eb removed if I cant' remember
const.OFFSET_X = 0
const.OFFSET_Y = 0

#this is the size of the screen in tiles, by multiplying LENGTH with SCALE you get the total screen size in pixels
#I forget why I have LENGTH WIDE X/Y, marked for removal
const.LENGTH_X = 40
const.LENGTH_Y = 30

const.LARGE_X = const.SCALE * const.LENGTH_X
const.LARGE_Y = const.SCALE * const.LENGTH_Y

#this is the size of the chunks which are used for faster scene loading
const.CHUNK_SIZE = 4

#odds WHO doctors will spawn 
# for example: 10 will give one in ten
const.WHO_ODDS = 100

const.NOG_ODDS = 10

#getting the users home directory
from os.path import expanduser
const.HOME = expanduser("~")

#this loads the resource files which are used in the game
const.SCRIPT = open('game.sc','r').readlines()

##############################################

gameloop = loop.loop()

if __name__=="__main__":
    gameloop.run()



































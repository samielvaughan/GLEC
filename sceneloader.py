import const, var, pygame
from pygame.locals import *
import scene, os


class sceneloader(object):
    def __init__(self):
        self.scenes = []

        #this creates all the scenes in the game from a script made in a plain text file
        #the key: line makes a key for tile creation, what colors corrispond to what creatures,tiles, object, ect
        #the scene: line contains the name of the file for the scene itself and the script for the scene (any text stuff)
        for line in const.SCRIPT:

            #key is the 
            #if "key" in line.lower():
            #    const.KEY = line.split(":")[1]

            #key that stores values as
            if "spritesheet" in line.lower():
                const.SHEET_KEY = line.split(":")[1]


            else if "color key" in line.lower():
                const.COLOR_KEY = line.split(":")[1]
        for line in const.SCRIPT:
            if "scene" in line.lower():
                self.scenes.append(scene(line.split(":")[1]))

        self.makesprites()

            
        self.scene = self.scenes[0]

        
    def update(self):
        if self.scene.has_changed():
            self.scene = self.scenes[self.scene.get_new_scene()]
        else:
            self.scene.update()

    def get_scene(self):
        return self.scene.get_img()

    def makesprites(self):

        #loads the sprite sheet into memory and resizes it to match the scale
        spritesheet = pygame.transform.scale(pygame.image.load(os.path.join('res','spritesheet.png')).convert_alpha(),(const.SIZE*256,const.SIZE*256))
        #this is the sprites array to store the values
        sprites = []

        #this moves a rect over the sprite sheet and gets small cuts from the sheet
        for x in xrange(spritesheet.get_width()/const.SCALE):
            #temporary sprite array
            current_list = []

            #moves the rect to a new spot and gets the current sprite from the sheet using a subsurface
            for y in xrange(spritesheet.get_height()/const.SCALE):
                current_list.append(spritesheet.subsurface(Rect(x*const.SCALE, y*const.SCALE, const.SCALE, const.SCALE)))
            #appends the finished array to the sprites array
            sprites.append(current_list)

        #initializes the sprite dictionary which the game will use
        #names will be used to retrieve sprites and all will be stored in arrays to allow animation of any given object later
        var.SPRITE_DICT = {}

        #splits the sprite_key constant 
        for item in const.SHEET_KEY.split("/"):

            #splits the current item into name/sprite corrdinates
            this_item = item.split("|")

            #creates the dictionary entry for the current sprites
            var.SPRITE_DICT[this_item[0]] = []

            # the # denotes a multidimentional array, such as for character walking
            #if "#" in this_item[1]:
            #    lists = this_item[1].split("#")
            #    this_current_sprites = []
            #    for Current_list in lists:
            #        Current_list = this_item[1].split("*")
            #        for Current_Sprite in xrange(len(current_list)-1):
            #        
            #            x,y = int(current_list[Current_Sprite].split(",")[0]),int(Current_list[Current_Sprite].split(",")[1])
            #            this_current_sprites.append(sprites[x][y])
            #    var.SPRITE_DICT[this_item[0]].append(this_current_sprites)
            #else:
            Current_list = this_item[1].split("*")
            for Current_Sprite in xrange(len(current_list)-1):
                    
                x,y = int(current_list[Current_Sprite].split(",")[0]),int(Current_list[Current_Sprite].split(",")[1])
                var.SPRITE_DICT[this_item[0]].append(sprites[x][y])

    def make_color_key(self):
        var.COLOR_TILE_KEY = {}
        for key in const.COLOR_KEY.split("|"):
            var.COLOR_TILE_KEY[key.split("/")[0]] = var.SPRITE_DICT[int(key.split("/")[1])]
            























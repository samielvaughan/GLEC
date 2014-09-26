import const, var
import pygame
import ebolachan

class scene(object):
    def __init__(self, scene_description):
        self.desc = scene_description.split("|")
        self.chunks = []
        self.camera = pygame.Surface((const.LARGE_X, const.LARGE_y))
        self.has_changed = False

        self.ebolachan = ebolachan.ebolachan()

    def make_world_map(self):
        this_map = pygame.image.load(os.path.join("res",self.desc[0]))
        self.world_map = pygame.Surface((this_map.get_width()*const.SCALE, this_map.get_height()*const.SCALE))
        composition = []
        size = [this_map.get_width(),this_map.get_height()]
        for x_coord in xrange(size[0]):
            for y_coord in xrange(size[1]):
                color = area.get_at((x_coord,y_coord))
                self.world_map.blit(var.COLOR_TILE_KEY[str(color)][0],x_coord*const.SCALE, y_coord*const.SCALE)


    def make_chunks(self):
        #this_chunk = pygame.Surface(Rect(0,0,const.SCALE*const.CHUNK_SIZE, const.SCALE*const.CHUNK_SIZE))
        #while (this_chunk.colliderect(self.world_map)):
        #    while (this_chunk.colliderect(self.world_map)):
        #        self.chunks.append(
        chunk_size = const.SCALE*const.CHUNK_SIZE
        for x in xrange((self.world_map.get_width()/chunk_size)+1):
            for y in xrange((self.world_map.get_hieght()/chunk_size)+1):
                self.chunks.append(self.world_map.subsurface(Rect(x*chunk_size,y*chunk_size,chunk_size,chunk_size)))

    def update(self):
        self.ebolachan.update()
        self.ebolachan.get_pos()
        
    def set_user_pos(self):
        self.ebolachan.set_pos()

    def get_img(self):
        return self.camera



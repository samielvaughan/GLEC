#!/usr/bin/env python

__doc__ = """
Controls:
    Cursor          : scroll, speed * 1
    Shift cursor    : scroll, speed * 5
    Mouse drag      : scroll, relative mouse * 2

The ScrollBuffer is about 2/3 faster than blitting collapsed tiles on my
dual-core laptop:
    Resolution: (800,600)
    Tile Size: (24, 28)
    Map Size: (102, 102)
    Tiles Per Screen 714.285714286
    Avg FPS: 469.556636556 (cursor keys)
    Avg FPS: 542.942734227 (mouse drag)
"""

import sys
import cProfile
import pstats

import pygame
from pygame.locals import *


class ScrollBuffer(object):
    """A scrolling buffer for a tile-based renderer where tiles comprise a map
    that is larger than the screen.
    
    This class is much more efficient than re-tiling the screen every frame. It
    reduces calls to blit by using pygame's Surface.scroll() to scroll the
    rendered pixels, and only renders tiles when they emerge into view.
    """
    
    def __init__(self, buffer_surface, world_rect):
        """Construct a Scrollbuffer.
        
        buffer_surface is a surface that the ScrollBuffer class will draw on.
        It should be the same size as the scrolling display. The scrolling
        display can be a screen or a subsurface. The buffer_surface can then
        be blitted onto the display in one efficient blit() call.
        
        world_rect supplies the coordinate space for the world, used in various
        calculations. You may pass the world.rect as this argument and it will
        be copied.
        """
        
        # Buffer space.
        self.buffer = buffer_surface
        self.buffer_rect = self.buffer.get_rect()
        
        # Camera: last drawn view, scroll-to view.
        self._camera_rect = Rect(self.buffer_rect)
        self.camera_rect = Rect(self.buffer_rect)
        
        # World space.
        self.world_rect = Rect(world_rect)
        
        self.dirty_world_x = Rect(0,0,0,0)
        self.dirty_world_y = Rect(0,0,0,0)
        
        # Screen space.
        self.dirty_screen_x = Rect(0,0,0,0)
        self.dirty_screen_y = Rect(0,0,0,0)
        
        # Num tiles drawn by render().
        self.num_tiles_x = 0
        self.num_tiles_y = 0
        
        self.dx = 0
        self.dy = 0
        self.top = True
    
    @property
    def surface(self):
        """Return the buffer surface suitable for blitting onto another surface.
        """
        return self.buffer
    
    def set_pos(self, pos, rect_attr='topleft'):
        """Set the view in world coordinates.
        
        rect_attr specifies which camera (rect) attribute gets the value pos.
        Camera, and pos, are specified in world coordinates.
        """
        setattr(self.camera_rect, rect_attr, pos)
    
    def scroll(self, dx, dy):
        """Scroll the display by the delta values.
        
        This method can be called repeatedly between renderings to accumulate
        movements.
        """
        cam_next = self.camera_rect
        cam_next[0] += dx
        cam_next[1] += dy
    
    def render(self, get_tiles):
        """Render exposed tiles.
        
        get_tiles is a function or method that takes a rect as argument, and
        returns a sequence of tiles that intersect with the rect. The rect will
        be specified in world coordinates.
        """
        self.num_tiles_x = 0
        self.num_tiles_y = 0
        
        cam_next = self.camera_rect
        cam_prev = self._camera_rect
        
        DX = cam_next[0] - cam_prev[0]
        DY = cam_next[1] - cam_prev[1]
        
        if self.top and (DX or DY):
            #sys.stdout.write('+')
            self.dx = DX
            self.dy = DY
            
            # dirty_world_x and dirty_world_y are the dirty rects that result when
            # camera moves along the X axis. These need to be filled with the
            # exposed tiles from the map.
            dirty_world_x = self.dirty_world_x
            dirty_world_y = self.dirty_world_y
            dirty_world_x[0] = 0
            dirty_world_x[1] = cam_next[1]
            dirty_world_x[2] = 0
            dirty_world_x[3] = cam_prev[3]
            dirty_world_y[0] = cam_next[0]
            dirty_world_y[1] = 0
            dirty_world_y[2] = cam_prev[2]
            dirty_world_y[3] = 0
            
            # shift_x and shift_w modify dirty_y based on dirty_x, to avoid
            # redrawing the overlapping corner.
            shift_x = 0
            shift_w = 0
            
            # The movement cases. These calculate dirty rects.
            if DX > 0:
                dirty_world_x[0] = cam_prev.right
                dirty_world_x[2] = abs(DX)
                shift_w = -dirty_world_x[2]
            elif DX < 0:
                dirty_world_x[0] = cam_next[0]
                dirty_world_x[2] = abs(DX)
                shift_x = dirty_world_x[2]
                shift_w = -dirty_world_x[2]
            if DY > 0:
                dirty_world_y[1] = cam_prev.bottom
                dirty_world_y[3] = abs(DY)
                dirty_world_y[0] += shift_x
                dirty_world_y[2] += shift_w
            elif DY < 0:
                dirty_world_y[1] = cam_next.top
                dirty_world_y[3] = abs(DY)
                dirty_world_y[2] -= dirty_world_x[2]
                dirty_world_y[0] += shift_x
            
            # dirty_screen_x and dirty_screen_y are the translations of
            # dirty_world_x and dirty_world_y to screen space.
            dirty_screen_x = self.dirty_screen_x
            dirty_screen_y = self.dirty_screen_y
            dirty_screen_x[0] = dirty_world_x[0] - cam_next[0]
            dirty_screen_x[1] = 0
            dirty_screen_x[2] = dirty_world_x[2]
            dirty_screen_x[3] = dirty_world_x[3]
            dirty_screen_y[0] = shift_x
            dirty_screen_y[1] = dirty_world_y[1] - cam_next[1]
            dirty_screen_y[2] = dirty_world_y[2]
            dirty_screen_y[3] = dirty_world_y[3]
            
            cam_prev[0:2] = cam_next[0:2]
            self.buffer.scroll(-DX,-DY)
        
        if self.top:
            dirty_screen_x = self.dirty_screen_x
            if dirty_screen_x[2]:
                self.buffer.fill((0,0,0), dirty_screen_x)
                dirty_world_x = self.dirty_world_x
                collides = dirty_world_x.colliderect
                tiles = [t for t in get_tiles(dirty_world_x) if collides(t.rect)]
                self.num_tiles_x = len(tiles)
                self._render_tiles_x(tiles)
                dirty_screen_x[2] = 0
            self.top = False
        else:
            dirty_screen_y = self.dirty_screen_y
            if dirty_screen_y[3]:
                self.buffer.fill((0,0,0), dirty_screen_y)
                dirty_world_y = self.dirty_world_y
                collides = dirty_world_y.colliderect
                tiles = [t for t in get_tiles(dirty_world_y) if collides(t.rect)]
                self.num_tiles_y = len(tiles)
                self._render_tiles_y(tiles)
                dirty_screen_y[3] = 0
            self.top = True
    
    def render_tiles_all(self, get_tiles):
        """Render all visible tiles.
        
        This method is intended to post a full screen, for initialization of
        the scroll buffer.
        
        get_tiles is a function or method that takes a rect as argument, and
        returns a sequence of tiles that intersect with the rect. The rect will
        be specified in world coordinates.
        """
        dirty_world = self.camera_rect
        dirty_screen = self.buffer_rect
        tiles = get_tiles(dirty_world)
        self._render_tiles(tiles, dirty_world, dirty_screen)
    
    def _render_tiles_x(self, tiles):
        """Render the X axis tiles (right or left edge).
        """
        self._render_tiles(tiles, self.dirty_world_x, self.dirty_screen_x)
    
    def _render_tiles_y(self, tiles):
        """Render the Y axis tiles (top or bottom edge).
        """
        self._render_tiles(tiles, self.dirty_world_y, self.dirty_screen_y)
    
    def _render_tiles(self, tiles, dirty_world, dirty_screen):
        """Render tiles from dirty_world rect to dirty_screen rect.
        """
        if len(tiles) == 0:
            return
        area = Rect(dirty_world)
        leftmost = reduce(min, [t.rect.x for t in tiles])
        topmost = reduce(min, [t.rect.y for t in tiles])
        worldx = dirty_world[0]
        worldy = dirty_world[1]
        blit = self.buffer.blit
        for tile in tiles:
            tile_rect = tile.rect
            tilex = tile_rect[0]
            tiley = tile_rect[1]
            area[0] = worldx - tilex
            area[1] = worldy - tiley
            blit(tile.image, dirty_screen, area)
    
    def blit(self, screen):
        """A convenience method to blit the buffer to the screen.
        
        Alternatively one could screen.blit(scrollbuffer.surface, (0,0)).
        """
        screen.blit(self.buffer, (0,0))


class ScrollBufferOpt(ScrollBuffer):
    """Scroll buffer with optimized renderer.
    
    This renderer is completely compatible with ScrollBuffer. It gains some
    FPS by alternately rendering exposed X and Y edges. At low FPS this
    rendering trick can be visible at the top or bottom of the screen,
    especially when DY is more than one pixel.
    """
    
    def render(self, get_tiles):
        """Render exposed tiles.
        
        get_tiles is a function or method that takes a rect as argument, and
        returns a sequence of tiles that intersect with the rect. The rect will
        be specified in world coordinates.
        """
        self.num_tiles_x = 0
        self.num_tiles_y = 0
        
        cam_next = self.camera_rect
        cam_prev = self._camera_rect
        
        DX = cam_next[0] - cam_prev[0]
        DY = cam_next[1] - cam_prev[1]
        
        # Return if camera has not moved.
        if not (DX or DY):
            return
        
        # dirty_world_x and dirty_world_y are the dirty rects that result when
        # camera moves along the X axis. These need to be filled with the
        # exposed tiles from the map.
        dirty_world_x = self.dirty_world_x
        dirty_world_y = self.dirty_world_y
        dirty_world_x[0] = 0
        dirty_world_x[1] = cam_next[1]
        dirty_world_x[2] = 0
        dirty_world_x[3] = cam_prev[3]
        dirty_world_y[0] = cam_next[0]
        dirty_world_y[1] = 0
        dirty_world_y[2] = cam_prev[2]
        dirty_world_y[3] = 0
        
        # shift_x and shift_w modify dirty_y based on dirty_x, to avoid
        # redrawing the overlapping corner.
        shift_x = 0
        shift_w = 0
        
        # The movement cases. These calculate dirty rects.
        if DX > 0:
            dirty_world_x[0] = cam_prev.right
            dirty_world_x[2] = abs(DX)
            shift_w = -dirty_world_x[2]
        elif DX < 0:
            dirty_world_x[0] = cam_next[0]
            dirty_world_x[2] = abs(DX)
            shift_x = dirty_world_x[2]
            shift_w = -dirty_world_x[2]
        if DY > 0:
            dirty_world_y[1] = cam_prev.bottom
            dirty_world_y[3] = abs(DY)
            dirty_world_y[0] += shift_x
            dirty_world_y[2] += shift_w
        elif DY < 0:
            dirty_world_y[1] = cam_next.top
            dirty_world_y[3] = abs(DY)
            dirty_world_y[2] -= dirty_world_x[2]
            dirty_world_y[0] += shift_x
        
        # dirty_screen_x and dirty_screen_y are the translations of
        # dirty_world_x and dirty_world_y to screen space.
        dirty_screen_x = self.dirty_screen_x
        dirty_screen_y = self.dirty_screen_y
        dirty_screen_x[0] = dirty_world_x[0] - cam_next[0]
        dirty_screen_x[1] = 0
        dirty_screen_x[2] = dirty_world_x[2]
        dirty_screen_x[3] = dirty_world_x[3]
        dirty_screen_y[0] = shift_x
        dirty_screen_y[1] = dirty_world_y[1] - cam_next[1]
        dirty_screen_y[2] = dirty_world_y[2]
        dirty_screen_y[3] = dirty_world_y[3]
        
        self.buffer.scroll(-DX,-DY)
        if DX:
            self.buffer.fill((0,0,0), dirty_screen_x)
            collides = dirty_world_x.colliderect
            tiles = [t for t in get_tiles(dirty_world_x) if collides(t.rect)]
            self.num_tiles_x = len(tiles)
            self._render_tiles_x(tiles)
        if DY:
            self.buffer.fill((0,0,0), dirty_screen_y)
            collides = dirty_world_y.colliderect
            tiles = [t for t in get_tiles(dirty_world_y) if collides(t.rect)]
            self.num_tiles_y = len(tiles)
            self._render_tiles_y(tiles)
        
        cam_prev.move_ip(DX,DY)


def main():
    global global_debug
    global_debug = False
    
    # Init pygame stuff.
    pygame.init()
    resolution = 800,600
    screen = pygame.display.set_mode(resolution, DOUBLEBUF)
    screen_rect = screen.get_rect()
    clock = pygame.time.Clock()
    black = Color('black')
    
    # Map, camera, and scroll buffer.
    world_map = tiledmap.TiledMap('map/mini2.tmx')
    print 'Resolution:',resolution
    print 'Tile Size:', world_map.tile_size
    print 'Map Size:', world_map.size
    print 'Tiles Per Screen', (screen_rect.w/float(world_map.tile_width)) * (screen_rect.h/float(world_map.tile_height))
    cam_rect = Rect(screen_rect)
    sbuf = ScrollBuffer(screen.copy(), world_map.rect)
#    sbuf = ScrollBufferOpt(screen.copy(), world_map.rect)
    
    # Render buffer in full.
    sbuf.render_tiles_all(world_map.get_tiles_in_rect)
    screen.blit(sbuf.surface, (0,0))
    pygame.display.flip()
    
    mouse_down = False
    mouse_pos = None
    keyx = keyy = 0
    dx = dy = 0
    speed = 1
    elapsed = 0
    nfps = fps = 0
    running = True
    
    while running:
        
        # FPS meter.
        elapsed += clock.tick()
        if elapsed >= 1000:
            pygame.display.set_caption('{0:.0f} fps | Tiles: {1},{2}'.format(
                clock.get_fps(),
                sbuf.num_tiles_x,
                sbuf.num_tiles_y,
            ))
            fps += clock.get_fps()
            nfps += 1
            elapsed %= 1000
        
        # Controls: (shift) cursor keys; mouse drag.
        dx = dy = 0
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                if e.key == K_RIGHT: keyx = 1
                elif e.key == K_LEFT: keyx = -1
                elif e.key == K_DOWN: keyy = 1
                elif e.key == K_UP: keyy = -1
                elif e.key == K_F2: global_debug = not global_debug
                elif e.key == K_ESCAPE: running = False
            elif e.type == KEYUP:
                if e.key in (K_LEFT,K_RIGHT): keyx = 0
                elif e.key in (K_DOWN,K_UP): keyy = 0
            elif e.type == QUIT: running = False
            elif e.type == MOUSEBUTTONDOWN:
                mouse_down = True
            elif e.type == MOUSEBUTTONUP:
                mouse_down = False
            elif e.type == MOUSEMOTION:
                dx += e.rel[0]
                dy += e.rel[1]
        
        # Update the camera position and render the buffer.
        if mouse_down:
            sbuf.scroll(dx*2,dy*2)
            sbuf.render(world_map.get_tiles_in_rect)
        else:
            shift = 1
            if pygame.key.get_mods() & KMOD_SHIFT:
                shift = 5
            dx = keyx * speed * shift
            dy = keyy * speed * shift
            sbuf.scroll(dx,dy)
            sbuf.render(world_map.get_tiles_in_rect)
        
        # Render the display.
        #screen.fill(black)
        screen.blit(sbuf.surface, (0,0))
        pygame.display.flip()
    
    print 'Avg FPS:', fps / nfps


if __name__ == '__main__':
    import paths
    import tiledmap
    if True:
        main()
    else:
        cProfile.run('main()', 'prof.dat')
        p = pstats.Stats('prof.dat')
        p.sort_stats('time').print_stats()

#!/usr/bin/env python

import sys
import cProfile
import pstats

import pygame
from pygame.locals import *

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

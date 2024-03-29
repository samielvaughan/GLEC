#!/usr/bin/python
# -*- coding: utf-8 -*-

u"""
TileMap loader for python for Tiled, a generic tile map editor
from http://mapeditor.org/ .
It loads the \*.tmx files produced by Tiled.


"""

# Versioning scheme based on: http://en.wikipedia.org/wiki/Versioning#Designating_development_stage
#
#   +-- api change, probably incompatible with older versions
#   |     +-- enhancements but no api change
#   |     |
# major.minor[.build[.revision]]
#                |
#                +-|* 0 for alpha (status)
#                  |* 1 for beta (status)
#                  |* 2 for release candidate
#                  |* 3 for (public) release
#
# For instance:
#     * 1.2.0.1 instead of 1.2-a
#     * 1.2.1.2 instead of 1.2-b2 (beta with some bug fixes)
#     * 1.2.2.3 instead of 1.2-rc (release candidate)
#     * 1.2.3.0 instead of 1.2-r (commercial distribution)
#     * 1.2.3.5 instead of 1.2-r5 (commercial distribution with many bug fixes)

__revision__ = "$Rev: 314 $"
__version__ = "3.0.0." + __revision__[6:-2]
__author__ = u'DR0ID @ 2009-2011'

if __debug__:
    print __version__
    import sys
    sys.stdout.write(u'%s loading ... \n' % (__name__))
    import time
    _start_time = time.time()

#  -----------------------------------------------------------------------------


import sys
from xml.dom import minidom, Node
import StringIO
import os.path

import pyglet

import tiledtmxloader

#  -----------------------------------------------------------------------------
class ResourceLoaderPyglet(tiledtmxloader.AbstractResourceLoader):

    def __init__(self):
        tiledtmxloader.AbstractResourceLoader.__init__(self)

    def _load_image(self, filename, colorkey=None, fileobj=None):
        img = self._img_cache.get(filename, None)
        if img is None:
            if fileobj:
                img = pyglet.image.load(filename, fileobj, pyglet.image.codecs.get_decoders("*.png")[0])
            else:
                img = pyglet.image.load(filename)
            self._img_cache[filename] = img
        return img

    def _load_image_part(self, filename, x, y, w, h, colorkey=None):
        image = self._load_image(filename, colorkey)
        img_part = image.get_region(x, y, w, h)
        return img_part

    def _load_image_parts(self, filename, margin, spacing, tile_width, tile_height, colorkey=None): #-> [images]
        source_img = self._load_image(filename, colorkey)
        images = []
        # Reverse the map column reading to compensate for pyglet's y-origin.
        for y in range(source_img.height - tile_height, margin - tile_height,
            -tile_height - spacing):
            for x in range(margin, source_img.width, tile_width + spacing):
                img_part = self._load_image_part(filename, x, y - spacing, tile_width, tile_height)
                images.append(img_part)
        return images

    def _load_image_file_like(self, file_like_obj, colorkey=None): # -> image
        # pyglet.image.load can load from a path and from a file-like object
        # that is why here it is redirected to the other method
        return self._load_image(file_like_obj, colorkey, file_like_obj)


#  -----------------------------------------------------------------------------


def demo_pyglet(file_name):
    """Thanks to: HydroKirby from #pyglet on freenode.org

    Loads and views a map using pyglet.

    Holding the arrow keys will scroll along the map.
    Holding the left shift key will make you scroll faster.
    Pressing the escape key ends the application.

    TODO:
    Maybe use this to put topleft as origin:

        glMatrixMode(GL_PROJECTION);
        glLoadIdentity();
        glOrtho(0.0, (double)mTarget->w, (double)mTarget->h, 0.0, -1.0, 1.0);

    """

    import pyglet
    from pyglet.gl import glTranslatef, glLoadIdentity

    world_map = tiledtmxloader.TileMapParser().parse_decode(file_name)
    # delta is the x/y position of the map view.
    # delta is a list so that it can be accessed from the on_draw method of
    # window and the update function. Note that the position is in integers to
    # match Pyglet Sprites. Using floating-point numbers causes graphical
    # problems. See http://groups.google.com/group/pyglet-users/browse_thread/thread/52f9ae1ef7b0c8fa?pli=1
    delta = [0, 0]
    frames_per_sec = 1.0 / 30.0
    window = pyglet.window.Window()

    @window.event
    def on_draw():
        window.clear()
        # Reset the "eye" back to the default location.
        glLoadIdentity()
        # Move the "eye" to the current location on the map.
        glTranslatef(delta[0], delta[1], 0.0)
        # TODO: [21:03]	thorbjorn: DR0ID_: You can generally determine the range of tiles that are visible before your drawing loop, which is much faster than looping over all tiles and checking whether it is visible for each of them.
        # [21:06]	DR0ID_: probably would have to rewrite the pyglet demo to use a similar render loop as you mentioned
        # [21:06]	thorbjorn: Yeah.
        # [21:06]	DR0ID_: I'll keep your suggestion in mind, thanks
        # [21:06]	thorbjorn: I haven't written a specific OpenGL renderer yet, so not sure what's the best approach for a tile map.
        # [21:07]	thorbjorn: Best to create a single texture with all your tiles, bind it, set up your vertex arrays and fill it with the coordinates of the tiles currently on the screen, and then let OpenGL draw the bunch.
        # [21:08]	DR0ID_: for each layer?
        # [21:08]	DR0ID_: yeah, probably a good approach
        # [21:09]	thorbjorn: Ideally for all layers at the same time, if you don't have to draw anything in between.
        # [21:09]	DR0ID_: well, the NPC and other dynamic things need to be drawn in between, right?
        # [21:09]	thorbjorn: Right, so maybe once for the bottom layers, then your complicated stuff, and then another time for the layers on top.

        batch.draw()

    keys = pyglet.window.key.KeyStateHandler()
    window.push_handlers(keys)
    resources = ResourceLoaderPyglet()
    resources.load(world_map)

    def update(dt):
        # The speed is 3 by default.
        # When left Shift is held, the speed increases.
        # The speed interpolates based on time passed, so the demo navigates
        # at a reasonable pace even on huge maps.
        speed = (3 + keys[pyglet.window.key.LSHIFT] * 6) * \
                int(dt / frames_per_sec)
        if keys[pyglet.window.key.LEFT]:
            delta[0] += speed
        if keys[pyglet.window.key.RIGHT]:
            delta[0] -= speed
        if keys[pyglet.window.key.UP]:
            delta[1] -= speed
        if keys[pyglet.window.key.DOWN]:
            delta[1] += speed

    # Generate the graphics for every visible tile.
    batch = pyglet.graphics.Batch()
    sprites = []
    for group_num, layer in enumerate(world_map.layers):
        if not layer.visible:
            continue
        if layer.is_object_group:
            # This is unimplemented in this minimal-case example code.
            # Should you as a user of tiledtmxloader need this layer,
            # I hope to have a separate demo using objects as well.
            continue
        group = pyglet.graphics.OrderedGroup(group_num)
        for ytile in range(layer.height):
            # To compensate for pyglet's upside-down y-axis, the Sprites are
            # placed in rows that are backwards compared to what was loaded
            # into the map. The next operation puts all rows upside-down.
            for xtile in range(layer.width):
                image_id = layer.content2D[xtile][ytile]
                if image_id:
                    # o_x and o_y are offsets. They are not helpful here.
                    o_x, o_y, image_file = resources.indexed_tiles[image_id]
                    sprites.append(pyglet.sprite.Sprite(image_file,
                        world_map.tilewidth * xtile,
                        world_map.tileheight * (layer.height - ytile),
                        batch=batch, group=group))

    pyglet.clock.schedule_interval(update, frames_per_sec)
    pyglet.app.run()


#  -----------------------------------------------------------------------------
def main():

    args = sys.argv[1:]
    if len(args) == 1:
        demo_pyglet(args[0])
    else:
        #print 'usage: python helperspyglet.py mapfile.tmx'
        print('usage: python %s your_map.tmx' % os.path.basename(__file__))

#  -----------------------------------------------------------------------------

if __name__ == '__main__':
    # import cProfile
    # cProfile.run('main()', "stats.profile")
    # import pstats
    # p = pstats.Stats("stats.profile")
    # p.strip_dirs()
    # p.sort_stats('time')
    # p.print_stats()

    main()


if __debug__:
    _dt = time.time() - _start_time
    sys.stdout.write(u'%s loaded: %fs \n' % (__name__, _dt))

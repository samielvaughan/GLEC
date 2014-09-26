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


import sdl2.ext


class MenuRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(MenuRenderer, self).__init__(window)

    def render(self, components, x=None, y=None):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(128, 128, 128))
        super(MenuRenderer, self).render(components)

import sdl2.ext

class Component(object):
    def __init__(self, window, world):
        self.next_state_class = None
        self.handing_off = False
        self.window = window
        self.world = world

    def clean_up(self):
        while self.world.entities:
            entity = self.world.entities.pop()
            self.world.delete(entity)
        for system in self.world.systems:
            self.world.remove_system(system)

    def prepare(self):
        print "Unimplemented"

    def post_process(self):
        print "Unimplemented"

    def hand_off(self):
        self.clean_up()
        next_state = self.next_state_class(self.window, self.world)
        next_state.prepare()
        return next_state

    def handle_events(self, event):
        print "Unimplemented"





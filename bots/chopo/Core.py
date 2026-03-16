from cambc import Controller, Direction, EntityType, Environment, Position
import random
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class Core:
    def __init__(self, ct: Controller):
        self.ct = ct
        self.builder_bots_spawned = 0
    
    def run(self):
        print("Core running")
        if self.builder_bots_spawned < 3:
            # if we haven't spawned 3 builder bots yet, try to spawn one on a random tile
            spawn_pos = self.ct.get_position().add(random.choice(DIRECTIONS))
            if self.ct.can_spawn(spawn_pos):
                self.ct.spawn_builder(spawn_pos)
                self.builder_bots_spawned += 1

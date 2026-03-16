from cambc import Controller, Direction, EntityType, Environment, Position
import random

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class BuilderBot:
    def __init__(self, ct: Controller):
        self.ct = ct
    
    def run(self):
        for d in Direction:
            check_pos = self.ct.get_position().add(d)
            if self.ct.can_build_harvester(check_pos):
                self.ct.build_harvester(check_pos)
                break
        self.lookForOre()
        # move in a random direction
        move_dir = random.choice(DIRECTIONS)
        move_pos = self.ct.get_position().add(move_dir)
        # we need to place a conveyor or road to stand on, before we can move onto a tile
        if self.ct.can_build_road(move_pos):
            self.ct.build_road(move_pos)
        if self.ct.can_move(move_dir):
            self.ct.move(move_dir)

    
    def lookForOre(self):
        for tile in self.ct.get_nearby_tiles():
            if self.ct.get_tile_env(tile) in [Environment.ORE_TITANIUM, Environment.ORE_AXIONITE]:
                print("Found ore at " + str(tile))
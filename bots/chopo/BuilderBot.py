from enum import Enum, auto
from cambc import Controller, Direction, EntityType, Environment, Position
import random
from collections import defaultdict

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class State(Enum):
    EXPLORING = auto()

class BuilderBot:
    def __init__(self, ct: Controller):
        self.ct = ct
        self.state = State.EXPLORING
    
    def run(self):
        if self.state == State.EXPLORING:
            self.step_exploring()

    def step_exploring(self):
        for d in Direction:
            check_pos = self.ct.get_position().add(d)
            if self.ct.can_build_harvester(check_pos):
                self.ct.build_harvester(check_pos)
                break
        
        # choose direction based on walls and roads (with a small chance of randomness to avoid loops)
        move_dir = self.get_best_direction()
        move_pos = self.ct.get_position().add(move_dir)
        # we need to place a conveyor or road to stand on, before we can move onto a tile
        if self.ct.can_build_road(move_pos):
            self.ct.build_road(move_pos)
        if self.ct.can_move(move_dir):
            self.ct.move(move_dir)

    def get_best_direction(self) -> Direction:
        WALL_WEIGHT = 3
        ROAD_WEIGHT = 2

        visible_tiles = self.ct.get_nearby_tiles()
        visible_entities = self.ct.get_nearby_entities()
        unit_pos = self.ct.get_position()

        direction_votes: dict[Direction, int] = defaultdict(int)

        wall_positions = (tile_pos for tile_pos in visible_tiles if self.ct.get_tile_env(tile_pos) == Environment.WALL)
        road_positions = (self.ct.get_position(entity_id) for entity_id in visible_entities if self.ct.get_entity_type(entity_id) == EntityType.ROAD)

        for positions, weight in [(wall_positions, WALL_WEIGHT), (road_positions, ROAD_WEIGHT)]:
            for pos in positions:
                if pos == unit_pos:
                    continue
                position_difference = Position(unit_pos.x-pos.x,unit_pos.y-pos.y)
                direction = Position(0, 0).direction_to(position_difference)
                for dir in (direction, direction.rotate_left(), direction.rotate_right()):
                    direction_votes[dir] += weight

        if not direction_votes:
            best_direction = random.choice(DIRECTIONS)
        else:
            best_direction = max(direction_votes.items(), key=lambda item: item[1])[0]
            # add randomness
            if random.randint(0, 1):
                best_direction = best_direction.rotate_left()
            if random.randint(0, 1):
                best_direction = best_direction.rotate_right()
        return best_direction

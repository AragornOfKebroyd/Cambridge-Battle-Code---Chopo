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
        # prefer the direction with the least walls and roads
        # walls are tiles (need to filter)
        # roads are entities (need to filter)
        # per wall, get its normalised vector, and add the opposite direction to a cumulative thing

        direction_votes: dict[Direction, int] = defaultdict(int)
        print(direction_votes)

        for tile_pos in visible_tiles:
            tile_env = self.ct.get_tile_env(tile_pos)
            if tile_env == Environment.WALL:
                position_difference = Position(unit_pos.x-tile_pos.x,unit_pos.y-tile_pos.y)
                direction = Position(0, 0).direction_to(position_difference)
                for dir in (direction, direction.rotate_left(), direction.rotate_right()):
                    direction_votes[dir] += WALL_WEIGHT

        for entity_id in visible_entities:
            type = self.ct.get_entity_type(entity_id)
            if type == EntityType.ROAD:
                entity_pos = self.ct.get_position(entity_id)
                position_difference = Position(unit_pos.x-entity_pos.x,unit_pos.y-entity_pos.y)
                direction = Position(0, 0).direction_to(position_difference)
                for dir in (direction, direction.rotate_left(), direction.rotate_right()):
                    direction_votes[dir] += ROAD_WEIGHT

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

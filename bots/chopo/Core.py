from cambc import Controller, Direction, EntityType, Environment, Position
import random
DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class OreCluster:
    def __init__(self, positions: list[Position]):
        self.positions = positions
        self.harvested = False

    def add_position(self, pos: Position):
        self.positions.append(pos)

    def in_cluster(self, pos: Position):
        for p in self.positions:
            if p == pos:
                return True
        return False

    def is_part_of_cluster(self, pos: Position):
        for p in self.positions:
            if abs(p[0] - pos[0]) <= 1 and abs(p[1] - pos[1]) <= 1:
                return True
        return False

MAX_SPAWNED_BUILDER_BOTS = 10

class Core:
    def __init__(self, ct: Controller):
        self.ct = ct
        self.builder_bots_spawned = 0
        self.setupDone = False
        self.oreClusters = []
        self.globalWalls = []
        self.builderBotIDs = []
        self.position = None
        self.directionScores = []
        self.best_spawns = []
        self.best_spawn_index = 0

    def setup(self):
        self.scanVisible()
        self.position = self.ct.get_position()
        self.decide_bot_directions()
        print(self.directionScores)
    
    def within_bounds(self,pos):
        return pos[0] >= 0 and pos[0] < self.ct.get_map_width() and pos[1] >= 0 and pos[1] < self.ct.get_map_height()

    def scanVisible(self):
        oreClusters: list[OreCluster] = []
        # run through visible tiles
        for tile in self.ct.get_nearby_tiles():
            if self.ct.get_tile_env(tile) == Environment.WALL:
                self.globalWalls.append(tile)
            if self.ct.get_tile_env(tile) in [Environment.ORE_TITANIUM, Environment.ORE_AXIONITE]:
                for oreCluster in oreClusters:
                    if oreCluster.is_part_of_cluster(tile):
                        oreCluster.add_position(tile)
                        break
                else:
                    oreClusters.append(OreCluster([tile]))
        self.oreClusters = oreClusters    

    def decide_bot_directions(self):
        directionScores = {}
        for direction in DIRECTIONS:
            basic_dirs = [direction.rotate_left(), direction, direction.rotate_right()]

            # evaluate how good this direction is for spawning builder bots in, based on how many ore clusters are in that direction and how many builder bots we already have in that direction
            score = 0
            posQueue = [self.ct.get_position().add(direction)] # guaranteed to be reachable
            inQ = set(posQueue[0])
            clusters = set()
            while len(posQueue) > 0:
                pos = posQueue.pop(0)
                for dir in basic_dirs:
                    new_pos = pos.add(dir)
                    if new_pos not in inQ and self.within_bounds(new_pos) and self.ct.is_in_vision(new_pos) and self.ct.get_tile_env(new_pos) != Environment.WALL:
                        # print(f"{direction} {new_pos}")
                        # score for reachable tiles
                        score += 1
                        inQ.add(new_pos)
                        posQueue.append(new_pos)
                        # score for new clusters
                        for cluster in self.oreClusters:
                            if cluster in clusters: continue
                            if cluster.in_cluster(new_pos):
                                clusters.add(cluster)
                                score += 5
                
            directionScores[direction] = score

        self.directionScores = sorted(directionScores.items(), key=lambda x: x[1], reverse=True)
        self.best_spawns = list(filter(lambda x: x[1]>10, self.directionScores))
        self.best_spawn_index = 0

    def run(self):
        # one time setup
        if self.setupDone == False:
            self.setup()
            self.setupDone = True

        # decide which directions to spawn builder bots in
        if self.builder_bots_spawned < MAX_SPAWNED_BUILDER_BOTS:
            # if we haven't spawned MAX_SPAWNED_BUILDER_BOTS builder bots yet, try to spawn one
            self.best_spawn_index = (self.best_spawn_index + 1) % len(self.best_spawns)

            spawn_dir, _ = self.best_spawns[self.best_spawn_index]

            spawn_pos = self.ct.get_position().add(spawn_dir)
            if self.ct.can_spawn(spawn_pos):
                self.ct.spawn_builder(spawn_pos)
                self.builder_bots_spawned += 1
                self.builderBotIDs.append(self.ct.get_tile_builder_bot_id(spawn_pos))
    
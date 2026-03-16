import sys
sys.path.append("bots/chopo")

from Core import Core
from Conveyor import Conveyor

from cambc import Controller, Direction, EntityType, Environment, Position

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class Player:
    def __init__(self, *args):
        self.num_spawned = 0
        self.control = None
    
    def setupControl(self, ct: Controller):
        match ct.get_entity_type():
            case EntityType.CORE:
                self.control = Core(ct)
            case EntityType.CONVEYOR:    
                self.control = Conveyor(ct)

    def run(self, ct: Controller):
        if self.control is None:
            self.setupControl(ct)
        self.control.run(ct)
import sys
sys.path.append("bots/chopo")

from Core import Core
from Conveyor import Conveyor
from Turret import Turret
from Launcher import Launcher
from Splitter import Splitter
from Bridge import Bridge
from Harvester import Harvester
from Foundry import Foundry
from Road import Road
from Barrier import Barrier
from Marker import Marker
from BuilderBot import BuilderBot

from cambc import Controller, Direction, EntityType, Environment, Position

DIRECTIONS = [d for d in Direction if d != Direction.CENTRE]

class Player:
    def __init__(self, *args):
        self.num_spawned = 0
        self.control = None
    
    def setupControl(self, ct: Controller):
        match ct.get_entity_type():
            case EntityType.BUILDER_BOT:
                self.control = BuilderBot(ct)
            case EntityType.CORE:
                self.control = Core(ct)
            case EntityType.GUNNER | EntityType.SENTINEL | EntityType.BREACH:
                self.control = Turret(ct, ct.get_entity_type())
            case EntityType.LAUNCHER:
                self.control = Launcher(ct)
            case EntityType.CONVEYOR | EntityType.ARMOURED_CONVEYOR:
                self.control = Conveyor(ct, ct.get_entity_type())
            case EntityType.SPLITTER:
                self.control = Splitter(ct)
            case EntityType.BRIDGE:
                self.control = Bridge(ct)
            case EntityType.HARVESTER:
                self.control = Harvester(ct)
            case EntityType.FOUNDRY:
                self.control = Foundry(ct)
            case EntityType.ROAD:
                self.control = Road(ct)
            case EntityType.BARRIER:
                self.control = Barrier(ct)
            case EntityType.MARKER:
                self.control = Marker(ct)

    def run(self, ct: Controller):
        if self.control is None:
            self.setupControl(ct)
        self.control.run(ct)
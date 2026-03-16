from cambc import Controller, Direction, EntityType, Environment, Position

class Conveyor:
    def __init__(self, ct: Controller, conveyorType: EntityType):
        self.ct = ct
        self.conveyorType = conveyorType
    
    def run(self):
        pass
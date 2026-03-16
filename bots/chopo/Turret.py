from cambc import Controller, Direction, EntityType, Environment, Position

class Turret:
    def __init__(self, ct: Controller, turretType: EntityType):
        self.ct = ct
        self.turretType = turretType

    def run(self):
        pass
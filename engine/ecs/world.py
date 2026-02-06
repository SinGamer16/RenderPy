class World:
    def __init__(self):
        self.entities = []
        self.components = {}
        self.systems = []

    def create_entity(self):
        eid = len(self.entities)
        self.entities.append(eid)
        return eid

    def add_component(self, entity, component):
        self.components.setdefault(type(component), {})[entity] = component

    def get(self, component_type):
        return self.components.get(component_type, {}).items()
    
    def try_get(self, entity, component_type):
        return self.components.get(component_type, {}).get(entity, None)

    def add_system(self, system):
        system.world = self
        self.systems.append(system)

    def update(self, dt):
        for s in self.systems:
            if hasattr(s, "update"):
                s.update(dt)

    def render(self):
        for s in self.systems:
            if hasattr(s, "render"):
                s.render()

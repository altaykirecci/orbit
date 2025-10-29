import random
from .enums import CelestialType, StarType, BlackHoleClass, PlanetType

class CelestialObject:
    def __init__(self, x: int, y: int, obj_type: CelestialType, name: str = ""):
        self.x = x
        self.y = y
        self.obj_type = obj_type
        self.name = name or f"{obj_type.value}_{random.randint(1, 1000)}"

# Star class
class Star:
    def __init__(self, x: float, y: float, star_type: StarType, radius: float, star_id: int):
        self.x = x
        self.y = y
        self.star_type = star_type
        self.radius = radius
        self.star_id = star_id
        self.planets = []
        self.asteroid_belts = []

# Black hole class
class BlackHole:
    def __init__(self, x: float, y: float, bh_class: BlackHoleClass, bh_id: int):
        self.x = x
        self.y = y
        self.bh_class = bh_class
        self.bh_id = bh_id
        
        # Influence radius and exclusion radius
        self.R_infl = {"stellar": 400, "intermediate": 2500, "super": 10000}[bh_class.value]
        self.R_excl = 1.5 * self.R_infl

# Planet class
class Planet:
    def __init__(self, x: float, y: float, orbit_radius: float, orbit_angle: float, 
                 planet_type: PlanetType, radius: float, star_id: int, planet_id: int):
        self.x = x
        self.y = y
        self.orbit_radius = orbit_radius
        self.orbit_angle = orbit_angle
        self.planet_type = planet_type
        self.radius = radius
        self.star_id = star_id
        self.planet_id = planet_id
        self.resources = {}

# Asteroid belt class
class AsteroidBelt:
    def __init__(self, star_id: int, center_radius: float, width: float, belt_id: int):
        self.star_id = star_id
        self.center_radius = center_radius
        self.width = width
        self.belt_id = belt_id
        self.radius = width / 2  # Belt radius as half of width
        self.fragment_count = random.randint(20, 200)
        self.resource_pool = {}

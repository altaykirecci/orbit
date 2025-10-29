from enum import Enum

# Yön enum'u
class Direction(Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

# Celestial object types
class CelestialType(Enum):
    SUN = "sun"
    BLACK_HOLE = "black_hole"
    ASTEROID_BELT = "asteroid_belt"
    PLANET = "planet"
    COMET = "comet"

# Star types
class StarType(Enum):
    M = "M"
    K = "K"
    G = "G"
    F = "F"
    A = "A"
    B = "B"
    O = "O"

# Black hole classes
class BlackHoleClass(Enum):
    STELLAR = "stellar"
    INTERMEDIATE = "intermediate"
    SUPERMASSIVE = "supermassive"

# Planet types
class PlanetType(Enum):
    ROCKY = "rocky"
    GAS_GIANT = "gas_giant"
    ICE_GIANT = "ice_giant"
    TERRESTRIAL = "terrestrial"

# Resource types
class ResourceType(Enum):
    IRON = "Iron"
    COPPER = "Copper"
    GOLD = "Gold"
    SILVER = "Silver"
    BAUXITE = "Bauxite"
    CHROMIUM = "Chromium"
    LEAD = "Lead"
    ZINC = "Zinc"
    NICKEL = "Nickel"
    BORON = "Boron"
    COAL = "Coal"
    LIGNITE = "Lignite"
    SULFUR = "Sulfur"
    URANIUM = "Uranium"
    THORIUM = "Thorium"
    CARBON = "Carbon"
    OXYGEN = "Oxygen"
    NITROGEN = "Nitrogen"

# Resource richness levels
class ResourceRichness(Enum):
    POOR = "poor"
    NORMAL = "normal"
    RICH = "rich"

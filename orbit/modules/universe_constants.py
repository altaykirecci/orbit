from .enums import ResourceType

class UniverseConstants:
    BASE_STAR_DENOMINATOR = 2000      # normal preset: 1 star / 2000 area units
    MIN_STAR_COUNT = 3
    MAX_STAR_COUNT = 20000            # game / performance limit
    BH_DENOMINATOR = 1_000_000       # 1 BH per 1M area (normal)
    ASTEROID_BELT_PROB = 0.30        # asteroid belt creation probability per star
    PLANET_MEAN_PER_STAR = 3.5       # average planet count (Poisson)
    PLANET_ORBIT_RATIO_RANGE = (1.2, 1.6)
    MIN_STAR_SPACING_FACTOR = 0.5     # D_min = factor * sqrt(A/N)
    BH_EXCLUSION_FACTOR = 1.5         # exclusion radius = factor * R_infl
    
    # Resource base abundance values
    BASE_RESOURCE_ABUNDANCE = {
        # Metals - Common to rare
        ResourceType.IRON: {"planet": 0.8, "asteroid": 1.0},
        ResourceType.COPPER: {"planet": 0.6, "asteroid": 0.8},
        ResourceType.LEAD: {"planet": 0.4, "asteroid": 0.6},
        ResourceType.ZINC: {"planet": 0.3, "asteroid": 0.5},
        ResourceType.NICKEL: {"planet": 0.2, "asteroid": 0.4},
        ResourceType.CHROMIUM: {"planet": 0.15, "asteroid": 0.3},
        ResourceType.BAUXITE: {"planet": 0.1, "asteroid": 0.2},
        ResourceType.SILVER: {"planet": 0.05, "asteroid": 0.15},
        ResourceType.GOLD: {"planet": 0.02, "asteroid": 0.08},
        ResourceType.BORON: {"planet": 0.01, "asteroid": 0.05},
        
        # Energy Resources
        ResourceType.COAL: {"planet": 0.7, "asteroid": 0.3},
        ResourceType.LIGNITE: {"planet": 0.5, "asteroid": 0.2},
        ResourceType.SULFUR: {"planet": 0.3, "asteroid": 0.4},
        ResourceType.URANIUM: {"planet": 0.01, "asteroid": 0.05},
        ResourceType.THORIUM: {"planet": 0.005, "asteroid": 0.02},
        
        # Gases - Atmospheric
        ResourceType.CARBON: {"planet": 0.4, "asteroid": 0.1},
        ResourceType.OXYGEN: {"planet": 0.6, "asteroid": 0.2},
        ResourceType.NITROGEN: {"planet": 0.5, "asteroid": 0.1}
    }
    
    # Resource richness thresholds
    RESOURCE_THRESHOLD_HIGH = 1.0
    RESOURCE_THRESHOLD_LOW = 0.2

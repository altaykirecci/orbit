from datetime import datetime
from typing import Optional
from .enums import Direction

class Ship:
    def __init__(self, x: int, y: int, universe_size: int = 200):
        self.x = x
        self.y = y
        self.direction = Direction.UP
        # Enerji: evrendeki tüm noktaları 3 defa ziyaret edecek kadar
        # Her nokta değişikliğinde 1 birim enerji kaybedecek
        self.max_energy = universe_size * universe_size * 3
        self.energy = self.max_energy
        self.speed = 1  # dakika cinsinden
        self.is_moving = False
        self.start_time: Optional[datetime] = None
        self.mission_start_time: Optional[datetime] = None

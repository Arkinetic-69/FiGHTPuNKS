import pygame

"""In-game attributes module.
This module contains the Attributes class, which defines various attributes
for characters, such as atk, hp, speed, and more."""

class Attributes:
    """Class to define fighter attributes."""
    
    def __init__(self):
        """Initialize fighter attributes."""
        self.atk = 10  # Base attack power
        self.hp = 100  # Health points
        self.speed = 5  # Movement speed
        self.jump_height = 10  # Jump height
        self.gravity = 1  # Gravity effect
        self.block_power = 5  # Blocking power
        self.dash_speed = 15  # Dash speed
        self.combo_multiplier = 1.2  # Combo attack multiplier
        self.attack_cooldown = 500  # Cooldown time for attacks in milliseconds
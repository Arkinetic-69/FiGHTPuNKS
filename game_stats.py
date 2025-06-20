import pygame

"""In-game statistics module.
This module contains the GameStats class, which tracks various statistics
for a player during the game, such as score, health, combo count, and more."""

class GameStats:
    """Class to track game statistics for a player."""
    
    def __init__(self):
        """Initialize statistics."""
        self.reset_stats()
        self.game_active = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.score = 0
        self.health = 100
        self.combo_count = 0
        self.attack_count = 0
        self.dash_count = 0
        self.jump_count = 0
        self.block_count = 0

    def update_score(self, points):
        """Update the score by adding points."""
        self.score += points
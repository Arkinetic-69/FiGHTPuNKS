import pygame

"""In-game mechanics module.
This module contains the Mechanics class, which handles various in-game mechanics
such as movement, jumping, attacking, and blocking for characters.
As well as round management and game state transitions; and the health system.
Subject to change."""

class Mechanics:
    """Class to handle in-game mechanics for a fighter character."""
    
    def __init__(self, fighter):
        """Initialize the mechanics with a fighter instance."""
        self.fighter = fighter
        self.is_jumping = False
        self.is_attacking = False
        self.is_blocking = False
        self.is_dashing = False
        self.health = 100  # Initial health
        self.max_health = 100  # Maximum health

    def jump(self):
        """Handle jumping mechanics."""
        if not self.is_jumping:
            self.is_jumping = True
            # Logic for jumping (e.g., apply vertical velocity)
    
    def attack(self):
        """Handle attacking mechanics."""
        if not self.is_attacking:
            self.is_attacking = True
            # Logic for attacking (e.g., apply damage, create hitbox)
    
    def block(self):
        """Handle blocking mechanics."""
        if not self.is_blocking:
            self.is_blocking = True
            # Logic for blocking (e.g., reduce damage taken)
    
    def dash(self):
        """Handle dashing mechanics."""
        if not self.is_dashing:
            self.is_dashing = True
            # Logic for dashing (e.g., apply dash speed)
    
    def update_health(self, amount):
        """Update the fighter's health."""
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health
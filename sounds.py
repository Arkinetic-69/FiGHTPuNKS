import pygame

"""Handles the in-game sounds, ost, and sfx.
This module contains the Sounds class, which manages the background music,
sound effects, and other audio elements in the game."""

class Sounds:
    """Class to handle in-game sounds, OST, and SFX."""
    
    def __init__(self):
        """Initialize the sound system."""
        pygame.mixer.init()
        self.background_music = None
        self.sound_effects = {}
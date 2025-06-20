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
    
    def load_background_music(self, music_path):
        """Load background music from a file."""
        self.background_music = music_path
        pygame.mixer.music.load(music_path)
    
    def play_background_music(self, loops=-1):
        """Play the background music."""
        if self.background_music:
            pygame.mixer.music.play(loops=loops)
    
    def stop_background_music(self):
        """Stop the background music."""
        pygame.mixer.music.stop()
    
    def load_sound_effect(self, name, sound_path):
        """Load a sound effect from a file."""
        self.sound_effects[name] = pygame.mixer.Sound(sound_path)
    
    def play_sound_effect(self, name):
        """Play a sound effect by name."""
        if name in self.sound_effects:
            self.sound_effects[name].play()
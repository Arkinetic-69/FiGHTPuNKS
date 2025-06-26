import pygame

"""Handles the in-game sounds, ost, and sfx.
This module contains the Sounds class, which manages the background music,
sound effects, and other audio elements in the game."""

class Sounds:
    """Class to handle in-game sounds, OST, and SFX."""
    
    def __init__(self):
        """Initialize the sound system."""
        pygame.mixer.init()
        self.menu_music = r'assets\audio\music\OST\main menu\Oddysey.m4a'
        self.stage_music = {
            'stage1': r'assets\audio\music\OST\stages\Enemy State.m4a',
            'stage2': r'assets\audio\music\OST\stages\Nano-angstrom.m4a',
            'stage3': r'assets\audio\music\OST\stages\!!.m4a',
        }
        self.sound_effects = {
            'combat':{'atk 1': r'assets\audio\sfx\hit.wav', 
             'atk 2': r'assets\audio\sfx\kick.wav',
             'ability': r'assets\audio\sfx\punch.wav',
             'jump': r'assets\audio\sfx\jump.wav',
             'block': r'assets\audio\sfx\block.wav',
             'hit': r'assets\audio\sfx\hit.wav',
             'death': r'assets\audio\sfx\death.wav'
            },
            'button': r'assets\audio\sfx\button_click.wav',
            'victory': r'assets\audio\sfx\victory.m4a'
        }
        self.credits_music = r'assets\audio\music\OST\Space Cowboy.m4a'
        self.load_sounds()
        
    def play_menu_music(self):
        """Play the main menu music."""
        pygame.mixer.music.load(self.menu_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
    
    def play_stage_music(self, stage):
        """Play the stage music based on the stage name."""
        if stage in self.stage_music:
            pygame.mixer.music.load(self.stage_music[stage])
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        else:
            print(f"Stage music for '{stage}' not found.")
    
    def play_sound_effect(self, effect):
        """Play a sound effect based on the effect name."""
        if effect in self.sound_effects['combat']:
            sound = pygame.mixer.Sound(self.sound_effects['combat'][effect])
            sound.set_volume(0.5)
            sound.play()
        elif effect in self.sound_effects:
            sound = pygame.mixer.Sound(self.sound_effects[effect])
            sound.set_volume(0.5)
            sound.play()
        else:
            print(f"Sound effect '{effect}' not found.")
    
    def play_credits_music(self):
        """Play the credits music."""
        pygame.mixer.music.load(self.credits_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
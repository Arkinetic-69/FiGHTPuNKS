import pygame

"""Handles the in-game sounds, ost, and sfx.
This module contains the Sounds class, which manages the background music,
sound effects, and other audio elements in the game."""

class Sounds:
    """Class to handle in-game sounds, OST, and SFX."""
    
    def __init__(self):
        """Initialize the sound system."""
        pygame.mixer.init()
        self.menu_music = r'assets\audio\music\OST\main menu\Oddysey.mp3'
        self.stage_music = {
            'stage1': r'assets\audio\music\OST\stages\!!.mp3',
            'stage2': r'assets\audio\music\OST\stages\Space Cowboys.mp3',
            'stage3': r'assets\audio\music\OST\stages\Nano-angstrom.mp3',
            'stage4': r'assets\audio\music\OST\stages\Enemy State.mp3',
        }
        self.sound_effects = {
            'combat':{'atk 1': r'assets\audio\sfx\atk_1.wav', 
             'atk 2': r'assets\audio\sfx\atk_2.wav',
             'jump': r'assets\audio\sfx\jump.wav',
             'block': r'assets\audio\sfx\block.wav',
             'hit': r'assets\audio\sfx\hit.wav',
             'death': r'assets\audio\sfx\death.wav'
            },
            'button': r'assets\audio\sfx\button_click.wav',
            'victory': r'assets\audio\sfx\victory.mp3'
        }
        
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
    
    # def play_sound_effect(self, effect):
    #     """Play a sound effect based on the effect name."""
    #     try:
    #         if effect in self.sound_effects['combat']:
    #             sound = pygame.mixer.Sound(self.sound_effects['combat'][effect])
    #             sound.set_volume(0.7)  # Slightly louder for combat sounds
    #             sound.play()
    #             print(f"Playing combat sound: {effect}")
    #         elif effect in self.sound_effects:
    #             sound = pygame.mixer.Sound(self.sound_effects[effect])
    #             sound.set_volume(0.5)
    #             sound.play()
    #             print(f"Playing sound effect: {effect}")
    #         else:
    #             print(f"Sound effect '{effect}' not found.")
    #     except pygame.error as e:
    #         print(f"Error playing sound effect '{effect}': {e}")

    def play_combat_sound(self, action_type):
        """Play combat sounds based on specific fighter actions."""
        combat_sound_map = {
            'punch': 'atk 1',
            'punch2': 'atk 2', 
            'jump': 'jump',
            'block': 'block',
            'hit': 'hit',
            'death': 'death'
        }
        
        if action_type in combat_sound_map:
            self.play_sound_effect(combat_sound_map[action_type])
    
    def play_credits_music(self):
        """Play the credits music."""
        pygame.mixer.music.load(self.credits_music)
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)
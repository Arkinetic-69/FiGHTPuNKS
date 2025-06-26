import pygame

from menu import Menus

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
            'combat':{'atk 1': r'assets\audio\sfx\hit.wav', 
             'atk 2': r'assets\audio\sfx\kick.wav',
             'ability': r'assets\audio\sfx\punch.wav',
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
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        try:
            pygame.mixer.music.load(self.menu_music)
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            print("Menu music started playing.")
        except pygame.error as e:
            print(f"Error loading menu music: {e}")

    def play_stage_music(self, stage):
        """Play the stage music based on the stage name."""
        # Stop any currently playing music
        pygame.mixer.music.stop()
        
        # Map of valid stages
        valid_stages = ['stage1', 'stage2', 'stage3', 'stage4']
        
        if stage in valid_stages and stage in self.stage_music:
            try:
                pygame.mixer.music.load(self.stage_music[stage])
                pygame.mixer.music.set_volume(0.5)
                pygame.mixer.music.play(-1)  # -1 means loop indefinitely
                print(f"Playing {stage} music: {self.stage_music[stage]}")
            except pygame.error as e:
                print(f"Error loading stage music for '{stage}': {e}")
        else:
            print(f"Stage music for '{stage}' not found or invalid stage.")
            # Fallback to stage1 music if available
            if 'stage1' in self.stage_music:
                try:
                    pygame.mixer.music.load(self.stage_music['stage1'])
                    pygame.mixer.music.set_volume(0.5)
                    pygame.mixer.music.play(-1)
                    print("Playing fallback stage1 music.")
                except pygame.error as e:
                    print(f"Error loading fallback music: {e}")
    
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
    
    def stop_music(self):
        """Stop all music playback."""
        pygame.mixer.music.stop()

    def fade_out_music(self, fade_time=1000):
        """Fade out the current music over specified time in milliseconds."""
        pygame.mixer.music.fadeout(fade_time)
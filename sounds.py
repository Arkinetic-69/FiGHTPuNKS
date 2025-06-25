import pygame
from typing import Dict, Optional

"""This module contains the SoundManager class, which handles all game audio
and works with the AssetManager for loading sound files."""

class SoundManager:
    """Centralized sound management system."""
    
    def __init__(self, asset_manager=None):
        """Initialize the sound manager."""
        self.asset_manager = asset_manager
        self.master_volume = 1.0
        self.music_volume = 0.8
        self.sfx_volume = 0.9
        self.enabled = True
        
        # Initialize pygame mixer
        try:
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Could not initialize audio: {e}")
            self.enabled = False
            
        # Sound categories
        self.background_music = None
        self.current_music_path = None
        
    def set_asset_manager(self, asset_manager):
        """Set the asset manager reference."""
        self.asset_manager = asset_manager
        
    def set_master_volume(self, volume: float):
        """Set master volume (0.0 to 1.0)."""
        self.master_volume = max(0.0, min(1.0, volume))
        if self.background_music:
            pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
            
    def set_music_volume(self, volume: float):
        """Set music volume (0.0 to 1.0)."""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.background_music:
            pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
            
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume (0.0 to 1.0)."""
        self.sfx_volume = max(0.0, min(1.0, volume))
        
    def play_sound(self, sound_path: str, volume: float = 1.0) -> bool:
        """Play a sound effect."""
        if not self.enabled or not self.asset_manager:
            return False
            
        try:
            sound = self.asset_manager.load_sound(sound_path)
            final_volume = self.master_volume * self.sfx_volume * volume
            sound.set_volume(final_volume)
            sound.play()
            return True
        except Exception as e:
            print(f"Error playing sound {sound_path}: {e}")
            return False
            
    def play_music(self, music_path: str, loop: bool = True, fade_in: int = 0) -> bool:
        """Play background music."""
        if not self.enabled:
            return False
            
        try:
            full_path = f"audio/{music_path}"
            if self.current_music_path != full_path:
                pygame.mixer.music.load(full_path)
                self.current_music_path = full_path
                
            loops = -1 if loop else 0
            
            if fade_in > 0:
                pygame.mixer.music.play(loops, fade_ms=fade_in)
            else:
                pygame.mixer.music.play(loops)
                
            pygame.mixer.music.set_volume(self.master_volume * self.music_volume)
            return True
            
        except pygame.error as e:
            print(f"Error playing music {music_path}: {e}")
            return False
            
    def stop_music(self, fade_out: int = 0):
        """Stop background music."""
        if fade_out > 0:
            pygame.mixer.music.fadeout(fade_out)
        else:
            pygame.mixer.music.stop()
            
    def pause_music(self):
        """Pause background music."""
        pygame.mixer.music.pause()
        
    def resume_music(self):
        """Resume background music."""
        pygame.mixer.music.unpause()
        
    def is_music_playing(self) -> bool:
        """Check if music is currently playing."""
        return pygame.mixer.music.get_busy()
        
    def play_fighter_sound(self, fighter_name: str, action: str, volume: float = 1.0) -> bool:
        """Play fighter-specific sound."""
        sound_path = f"fighters/{fighter_name.lower()}/{action}.wav"
        return self.play_sound(sound_path, volume)
        
    def play_hit_sound(self, hit_type: str = "hit", volume: float = 1.0) -> bool:
        """Play hit sound effect."""
        sound_path = f"sfx/{hit_type}.wav"
        return self.play_sound(sound_path, volume)
        
    def play_ui_sound(self, ui_action: str, volume: float = 1.0) -> bool:
        """Play UI sound effect."""
        sound_path = f"ui/{ui_action}.wav"
        return self.play_sound(sound_path, volume)
        
    def enable_audio(self):
        """Enable audio system."""
        self.enabled = True
        
    def disable_audio(self):
        """Disable audio system."""
        self.enabled = False
        self.stop_music()
        
    def get_audio_info(self) -> Dict:
        """Get audio system information."""
        return {
            'enabled': self.enabled,
            'master_volume': self.master_volume,
            'music_volume': self.music_volume,
            'sfx_volume': self.sfx_volume,
            'music_playing': self.is_music_playing(),
            'current_music': self.current_music_path
        }
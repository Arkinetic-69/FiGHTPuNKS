import pygame
import json
from typing import Dict, Tuple, List
from anim import AnimationManager
from ass import AssetManager
from sounds import SoundManager

"""This module contains the Settings class, which manages the game settings,
including screen dimensions, background color, and game engine configuration."""

class Settings:
    """Singleton Settings class for game configuration."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize game settings."""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        
        # Load configuration
        self.config = self._load_config()
        self.stats = self._load_stats()
        
        # Initialize managers
        self.asset_manager = AssetManager()
        self.anim_manager = AnimationManager(self.asset_manager)
        self.sound_manager = SoundManager(self.asset_manager)
        
        # Link managers
        self.anim_manager.set_asset_manager(self.asset_manager)
        self.sound_manager.set_asset_manager(self.asset_manager)
        
        # Screen settings
        self._setup_display_settings()
        
        # Game settings
        self._setup_gameplay_settings()
        
        # Audio settings
        self._setup_audio_settings()
        
        # Initialize scaling
        self.scale_factor = self.config["graphics"]["scale_factor"]
        self.base_resolution = (self.config["display"]["screen_width"], 
                               self.config["display"]["screen_height"])
        
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open('game_config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config file: {e}")
            return self._get_default_config()
    
    def _load_stats(self) -> dict:
        """Load game statistics from JSON file."""
        try:
            with open('game_stats.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load stats file: {e}")
            return self._get_default_stats()
    
    def _get_default_config(self) -> dict:
        """Get default configuration."""
        return {
            "display": {
                "screen_width": 1200,
                "screen_height": 700,
                "title": "FiGHTPuNKS",
                "fullscreen": False,
                "vsync": True,
                "fps": 60
            },
            "graphics": {
                "scale_factor": 1.0,
                "supported_resolutions": [[800, 600], [1200, 700], [1920, 1080]],
                "minimum_resolution": [800, 600]
            },
            "gameplay": {
                "fighter_speed": 15.0,
                "fighter_vel_y": 40.0,
                "fighter_gravity": 5.0,
                "fighter_jump": 40.0,
                "fighter_dash": 50.0
            },
            "audio": {
                "master_volume": 1.0,
                "music_volume": 0.8,
                "sfx_volume": 0.9,
                "enabled": True
            }
        }
    
    def _get_default_stats(self) -> dict:
        """Get default statistics."""
        return {
            "session": {"games_played": 0, "total_playtime": 0},
            "players": {"player1": {"wins": 0, "losses": 0}, "player2": {"wins": 0, "losses": 0}},
            "fighters": {"Kevin": {"times_played": 0}, "Fire Girl": {"times_played": 0}}
        }
    
    def _setup_display_settings(self):
        """Setup display-related settings."""
        display_config = self.config["display"]
        self.screen_width = display_config["screen_width"]
        self.screen_height = display_config["screen_height"]
        self.game_title = display_config["title"]
        self.fullscreen = display_config["fullscreen"]
        self.fps = display_config["fps"]
        
        # Colors
        self.bg_color = (128, 128, 128)
    
    def _setup_gameplay_settings(self):
        """Setup gameplay-related settings."""
        gameplay_config = self.config["gameplay"]
        self.fighter_speed = gameplay_config["fighter_speed"]
        self.fighter_vel_y = gameplay_config["fighter_vel_y"]
        self.fighter_gravity = gameplay_config["fighter_gravity"]
        self.fighter_jump = gameplay_config["fighter_jump"]
        self.fighter_dash = gameplay_config["fighter_dash"]
        
    def _setup_audio_settings(self):
        """Setup audio-related settings."""
        audio_config = self.config["audio"]
        self.sound_manager.set_master_volume(audio_config["master_volume"])
        self.sound_manager.set_music_volume(audio_config["music_volume"])
        self.sound_manager.set_sfx_volume(audio_config["sfx_volume"])
        
        if not audio_config["enabled"]:
            self.sound_manager.disable_audio()
    
    def set_resolution(self, width: int, height: int) -> bool:
        """Set screen resolution with validation."""
        min_width, min_height = self.config["graphics"]["minimum_resolution"]
        
        if width < min_width or height < min_height:
            print(f"Resolution {width}x{height} is below minimum {min_width}x{min_height}")
            return False
        
        self.screen_width = width
        self.screen_height = height
        
        # Update scale factor
        base_width, base_height = self.base_resolution
        scale_x = width / base_width
        scale_y = height / base_height
        self.scale_factor = min(scale_x, scale_y)  # Maintain aspect ratio
        
        # Update config
        self.config["display"]["screen_width"] = width
        self.config["display"]["screen_height"] = height
        self.config["graphics"]["scale_factor"] = self.scale_factor
        
        return True
    
    def get_supported_resolutions(self) -> List[Tuple[int, int]]:
        """Get list of supported resolutions."""
        return [tuple(res) for res in self.config["graphics"]["supported_resolutions"]]
    
    def scale_value(self, value: float) -> float:
        """Scale a value based on current scale factor."""
        return value * self.scale_factor
    
    def scale_position(self, x: float, y: float) -> Tuple[float, float]:
        """Scale a position based on current scale factor."""
        return (x * self.scale_factor, y * self.scale_factor)
    
    def scale_size(self, width: float, height: float) -> Tuple[float, float]:
        """Scale dimensions based on current scale factor."""
        return (width * self.scale_factor, height * self.scale_factor)
    
    def get_scaled_font_size(self, base_size: int) -> int:
        """Get scaled font size."""
        return max(8, int(base_size * self.scale_factor))
    
    def save_config(self):
        """Save current configuration to file."""
        try:
            with open('game_config.json', 'w') as f:
                json.dump(self.config, f, indent=2)
        except IOError as e:
            print(f"Error saving config: {e}")
    
    def save_stats(self):
        """Save current statistics to file."""
        try:
            with open('game_stats.json', 'w') as f:
                json.dump(self.stats, f, indent=2)
        except IOError as e:
            print(f"Error saving stats: {e}")
    
    def update_stat(self, category: str, subcategory: str, key: str, value):
        """Update a specific statistic."""
        if category in self.stats and subcategory in self.stats[category]:
            self.stats[category][subcategory][key] = value
    
    def get_stat(self, category: str, subcategory: str, key: str, default=0):
        """Get a specific statistic."""
        return self.stats.get(category, {}).get(subcategory, {}).get(key, default)
    
    def increment_stat(self, category: str, subcategory: str, key: str, amount: int = 1):
        """Increment a statistic."""
        current = self.get_stat(category, subcategory, key, 0)
        self.update_stat(category, subcategory, key, current + amount)
    
    def reset_stats(self):
        """Reset all statistics."""
        self.stats = self._get_default_stats()
        self.save_stats()
    
    def initialize_assets(self):
        """Initialize and preload assets."""
        # Preload common assets
        self.asset_manager.preload_common_assets()
        
        # Load fighter animations into animation manager
        fighters = ['Kevin', 'Fire Girl']
        
        for fighter_name in fighters:
            fighter_animations = self.asset_manager.load_fighter_animations(fighter_name)
            if fighter_animations:
                self.anim_manager.load_fighter_animations(fighter_name, fighter_animations)
    
    def get_background_image(self, stage_name: str = 'stage1.bmp') -> pygame.Surface:
        """Get scaled background image."""
        bg_image = self.asset_manager.get_stage_image(stage_name)
        
        # Scale to current resolution if needed
        if self.scale_factor != 1.0:
            new_width = int(bg_image.get_width() * self.scale_factor)
            new_height = int(bg_image.get_height() * self.scale_factor)
            bg_image = pygame.transform.scale(bg_image, (new_width, new_height))
        
        return bg_image
    
    def play_sound_effect(self, sound_name: str, volume: float = 1.0):
        """Play a sound effect."""
        self.sound_manager.play_sound(f"sfx/{sound_name}.wav", volume)
        
    def play_background_music(self, music_name: str, loop: bool = True):
        """Play background music."""
        self.sound_manager.play_music(f"music/{music_name}", loop)
        
    def get_display_info(self) -> dict:
        """Get comprehensive display information."""
        return {
            'resolution': (self.screen_width, self.screen_height),
            'base_resolution': self.base_resolution,
            'scale_factor': self.scale_factor,
            'fullscreen': self.fullscreen,
            'fps': self.fps
        }

# Global settings instance getter
def get_settings() -> Settings:
    """Get the global settings instance."""
    return Settings()


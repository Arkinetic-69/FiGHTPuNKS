import pygame
import os
import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path

"""This module contains the AssetManager class, which manages all game assets
including images, sounds, fonts, and fighter animations."""

class AssetManager:
    """Centralized asset management system."""
    
    _instance = None
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Initialize the asset manager."""
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[str, pygame.font.Font] = {}
        self.fighter_animations: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        
        # Load configuration
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        try:
            with open('game_config.json', 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Warning: Could not load config file: {e}")
            return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Get default configuration if file is missing."""
        return {
            "paths": {
                "assets": "assets",
                "fighters": "assets/images/fighters",
                "stages": "assets/images/stages",
                "audio": "assets/audio",
                "fonts": "assets/fonts"
            }
        }
    
    def load_image(self, path: str, convert_alpha: bool = True, scale: Optional[Tuple[int, int]] = None) -> pygame.Surface:
        """Load and cache an image."""
        cache_key = f"{path}_{scale}" if scale else path
        
        if cache_key not in self.images:
            try:
                full_path = os.path.join(self.config["paths"]["assets"], path)
                image = pygame.image.load(full_path)
                
                if convert_alpha:
                    image = image.convert_alpha()
                else:
                    image = image.convert()
                
                if scale:
                    image = pygame.transform.scale(image, scale)
                
                self.images[cache_key] = image
                
            except pygame.error as e:
                print(f"Error loading image {path}: {e}")
                # Create placeholder image
                placeholder = pygame.Surface((100, 100))
                placeholder.fill((255, 0, 255))  # Magenta placeholder
                self.images[cache_key] = placeholder
        
        return self.images[cache_key]
    
    def load_sound(self, path: str) -> pygame.mixer.Sound:
        """Load and cache a sound."""
        if path not in self.sounds:
            try:
                full_path = os.path.join(self.config["paths"]["audio"], path)
                self.sounds[path] = pygame.mixer.Sound(full_path)
            except pygame.error as e:
                print(f"Error loading sound {path}: {e}")
                # Create silent sound as placeholder
                self.sounds[path] = pygame.mixer.Sound(buffer=b'\x00\x00' * 1000)
        
        return self.sounds[path]
    
    def load_font(self, path: str, size: int) -> pygame.font.Font:
        """Load and cache a font."""
        cache_key = f"{path}_{size}"
        
        if cache_key not in self.fonts:
            try:
                if path:
                    full_path = os.path.join(self.config["paths"]["fonts"], path)
                    self.fonts[cache_key] = pygame.font.Font(full_path, size)
                else:
                    self.fonts[cache_key] = pygame.font.Font(None, size)
            except pygame.error as e:
                print(f"Error loading font {path}: {e}")
                self.fonts[cache_key] = pygame.font.Font(None, size)
        
        return self.fonts[cache_key]
    
    def load_fighter_animations(self, fighter_name: str) -> Dict[str, List[pygame.Surface]]:
        """Load all animations for a fighter."""
        if fighter_name in self.fighter_animations:
            return self.fighter_animations[fighter_name]
        
        fighter_animations = {}
        
        # Map display names to folder names
        folder_mapping = {
            'Kevin': 'kevin',
            'Fire Girl': 'fIREgIRLSPRITE'
        }
        
        folder_name = folder_mapping.get(fighter_name, fighter_name.lower())
        fighter_path = os.path.join(self.config["paths"]["fighters"], folder_name)
        
        # Load different animation types
        animation_types = ['idle', 'walk', 'attack1', 'attack2', 'jump', 'dash', 'death', 'stun']
        
        for anim_type in animation_types:
            frames = self._load_animation_frames(r'assets\images\fighters', anim_type)
            if frames:
                fighter_animations[anim_type] = frames
        
        self.fighter_animations[fighter_name] = fighter_animations
        return fighter_animations
    
    def _load_animation_frames(self, fighter_path: str, anim_type: str) -> List[pygame.Surface]:
        """Load animation frames from directory."""
        anim_path = os.path.join(fighter_path, anim_type)
        frames = []
        
        if not os.path.exists(anim_path):
            return frames
        
        try:
            # Get all image files and sort them
            filenames = [f for f in os.listdir(anim_path) 
                        if f.lower().endswith(('.bmp', '.png', '.jpg', '.jpeg'))]
            
            # Sort numerically if possible
            try:
                filenames.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
            except:
                filenames.sort()  # Fallback to alphabetical
            
            for filename in filenames:
                file_path = os.path.join(anim_path, filename)
                try:
                    frame = pygame.image.load(file_path).convert_alpha()
                    frames.append(frame)
                except pygame.error as e:
                    print(f"Error loading frame {file_path}: {e}")
                    
        except OSError as e:
            print(f"Error accessing directory {anim_path}: {e}")
        
        return frames
    
    def get_stage_image(self, stage_name: str) -> pygame.Surface:
        """Load a stage background image."""
        return self.load_image(f"stages/{stage_name}")
    
    def preload_common_assets(self):
        """Preload commonly used assets."""
        # Preload stage backgrounds
        stage_files = ['stage1.bmp']  # Add more as needed
        for stage_file in stage_files:
            self.get_stage_image(stage_file)
        
        # Preload fighter animations
        fighters = ['Kevin', 'Fire Girl']
        for fighter in fighters:
            self.load_fighter_animations(fighter)
    
    def clear_cache(self):
        """Clear all cached assets."""
        self.images.clear()
        self.sounds.clear()
        self.fonts.clear()
        self.fighter_animations.clear()
    
    def get_memory_usage(self) -> dict:
        """Get memory usage statistics."""
        return {
            'images': len(self.images),
            'sounds': len(self.sounds),
            'fonts': len(self.fonts),
            'fighter_animations': len(self.fighter_animations)
        }
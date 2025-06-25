import pygame
from typing import Dict, List, Optional

"""This module contains the AnimationManager class, which handles all fighter animations
and works with the AssetManager for loading animation frames."""

class AnimationManager:
    """Centralized animation management system."""
    
    def __init__(self, asset_manager=None):
        """Initialize the animation manager."""
        self.asset_manager = asset_manager
        self.animations: Dict[str, Dict[str, List[pygame.Surface]]] = {}
        self.current_animations: Dict[str, str] = {}  # fighter_id -> current_anim
        self.animation_indices: Dict[str, float] = {}  # fighter_id -> current_index
        self.animation_speeds: Dict[str, float] = {}   # fighter_id -> anim_speed
        self.animation_loops: Dict[str, bool] = {}     # fighter_id -> should_loop
        
    def set_asset_manager(self, asset_manager):
        """Set the asset manager reference."""
        self.asset_manager = asset_manager
        
    def load_fighter_animations(self, fighter_name: str, animations_dict: Dict[str, List[pygame.Surface]]):
        """Load all animations for a fighter from asset manager."""
        self.animations[fighter_name] = animations_dict
        
    def create_fighter_instance(self, fighter_id: str, fighter_name: str, anim_speed: float = 0.2):
        """Create a new fighter animation instance."""
        # Load fighter animations if not already loaded
        if fighter_name not in self.animations and self.asset_manager:
            fighter_animations = self.asset_manager.load_fighter_animations(fighter_name)
            self.load_fighter_animations(fighter_name, fighter_animations)
        
        self.current_animations[fighter_id] = 'idle'
        self.animation_indices[fighter_id] = 0.0
        self.animation_speeds[fighter_id] = anim_speed
        self.animation_loops[fighter_id] = True
        
    def set_animation(self, fighter_id: str, animation_name: str, reset_index: bool = True, loop: bool = True):
        """Set the current animation for a fighter."""
        if fighter_id not in self.current_animations:
            return
            
        # Only change if it's different or we're forcing a reset
        if self.current_animations[fighter_id] != animation_name or reset_index:
            if reset_index:
                self.animation_indices[fighter_id] = 0.0
            self.current_animations[fighter_id] = animation_name
            self.animation_loops[fighter_id] = loop
        
    def update_animation(self, fighter_id: str) -> Optional[pygame.Surface]:
        """Update and return the current animation frame."""
        if fighter_id not in self.current_animations:
            return self._get_placeholder_frame()
            
        fighter_name = self._get_fighter_name_from_id(fighter_id)
        current_anim = self.current_animations[fighter_id]
        
        # Get animation frames
        frames = self.animations.get(fighter_name, {}).get(current_anim, [])
        if not frames:
            # Try fallback to idle animation
            frames = self.animations.get(fighter_name, {}).get('idle', [])
            if not frames:
                return self._get_placeholder_frame()
            
        # Update animation index
        current_index = self.animation_indices[fighter_id]
        speed = self.animation_speeds[fighter_id]
        should_loop = self.animation_loops[fighter_id]
        
        # Check if animation should advance
        if should_loop or current_index < len(frames) - 1:
            self.animation_indices[fighter_id] += speed
            
            if self.animation_indices[fighter_id] >= len(frames):
                if should_loop:
                    self.animation_indices[fighter_id] = 0.0
                else:
                    self.animation_indices[fighter_id] = len(frames) - 1
        
        # Return current frame
        frame_index = int(self.animation_indices[fighter_id])
        frame_index = min(frame_index, len(frames) - 1)  # Clamp to valid range
        return frames[frame_index]
    
    def _get_placeholder_frame(self) -> pygame.Surface:
        """Create a placeholder frame."""
        placeholder = pygame.Surface((125, 320))
        placeholder.fill((255, 0, 255))  # Magenta
        return placeholder
        
    def get_current_animation(self, fighter_id: str) -> str:
        """Get the current animation name for a fighter."""
        return self.current_animations.get(fighter_id, 'idle')
        
    def is_animation_finished(self, fighter_id: str) -> bool:
        """Check if the current animation cycle is complete."""
        if fighter_id not in self.current_animations:
            return True
            
        fighter_name = self._get_fighter_name_from_id(fighter_id)
        current_anim = self.current_animations[fighter_id]
        frames = self.animations.get(fighter_name, {}).get(current_anim, [])
        
        if not frames:
            return True
            
        # If looping, never "finished"
        if self.animation_loops.get(fighter_id, True):
            return False
            
        return self.animation_indices[fighter_id] >= len(frames) - 1
        
    def get_animation_progress(self, fighter_id: str) -> float:
        """Get animation progress as percentage (0.0 to 1.0)."""
        if fighter_id not in self.current_animations:
            return 0.0
            
        fighter_name = self._get_fighter_name_from_id(fighter_id)
        current_anim = self.current_animations[fighter_id]
        frames = self.animations.get(fighter_name, {}).get(current_anim, [])
        
        if not frames:
            return 0.0
            
        return min(1.0, self.animation_indices[fighter_id] / len(frames))
        
    def _get_fighter_name_from_id(self, fighter_id: str) -> str:
        """Extract fighter name from fighter ID (e.g., 'player1_Kevin' -> 'Kevin')."""
        return fighter_id.split('_')[-1] if '_' in fighter_id else fighter_id
        
    def set_animation_speed(self, fighter_id: str, speed: float):
        """Set animation speed for a fighter."""
        if fighter_id in self.animation_speeds:
            self.animation_speeds[fighter_id] = speed
        
    def pause_animation(self, fighter_id: str):
        """Pause animation for a fighter."""
        self.set_animation_speed(fighter_id, 0.0)
        
    def resume_animation(self, fighter_id: str, speed: float = 0.2):
        """Resume animation for a fighter."""
        self.set_animation_speed(fighter_id, speed)
        
    def has_animation(self, fighter_name: str, animation_name: str) -> bool:
        """Check if a fighter has a specific animation."""
        return animation_name in self.animations.get(fighter_name, {})
        
    def get_available_animations(self, fighter_name: str) -> List[str]:
        """Get list of available animations for a fighter."""
        return list(self.animations.get(fighter_name, {}).keys())
        
    def cleanup_fighter(self, fighter_id: str):
        """Remove a fighter's animation data."""
        self.current_animations.pop(fighter_id, None)
        self.animation_indices.pop(fighter_id, None)
        self.animation_speeds.pop(fighter_id, None)
        self.animation_loops.pop(fighter_id, None)
        
    def get_debug_info(self, fighter_id: str) -> Dict:
        """Get debug information for a fighter's animation."""
        if fighter_id not in self.current_animations:
            return {}
            
        fighter_name = self._get_fighter_name_from_id(fighter_id)
        current_anim = self.current_animations[fighter_id]
        frames = self.animations.get(fighter_name, {}).get(current_anim, [])
        
        return {
            'fighter_name': fighter_name,
            'current_animation': current_anim,
            'current_index': self.animation_indices[fighter_id],
            'total_frames': len(frames),
            'animation_speed': self.animation_speeds[fighter_id],
            'is_looping': self.animation_loops[fighter_id],
            'progress': self.get_animation_progress(fighter_id)
        }
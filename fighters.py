import pygame
from settings import Settings
from pygame.sprite import Sprite
from typing import Dict, Any

"""This module defines the Fighter class and all fighter-related functionality,
including attributes, stats, and behaviors for both player and dummy characters."""

class Fighter(Sprite):
    """Centralized Fighter class for both player and dummy characters."""
    
    def __init__(self, x, y, fighter_name, is_player_1, settings=None, is_dummy=False):
        """Initialize Fighter's behavior and attributes."""
        
        super().__init__()
        # Use shared settings instance or create new one
        self.settings = settings if settings else Settings()
        self.is_player_1 = is_player_1
        self.is_dummy = is_dummy
        self.screen = pygame.display.get_surface()
        self.fighter_name = fighter_name
        
        # Initialize fighter attributes
        self.fighter_attributes = FighterAttributes(fighter_name)
        
        # Create unique fighter ID for animation tracking
        player_type = "dummy" if is_dummy else ("player1" if is_player_1 else "player2")
        self.fighter_id = f"{player_type}_{fighter_name}"
        
        # Register with animation manager
        self.settings.anim_manager.create_fighter_instance(self.fighter_id, fighter_name)

        # Get initial frame
        self.image = self.settings.anim_manager.update_animation(self.fighter_id)
        if self.image is None:
            self.image = self._create_placeholder_sprite()
        
        # Scale based on settings
        sprite_width = int(self.settings.scale_value(125))
        sprite_height = int(self.settings.scale_value(320))
        self.rect = pygame.Rect((x, y, sprite_width, sprite_height))

        # Fighter stats (from attributes)
        self.max_health = self.fighter_attributes.get_attribute('health')
        self.current_health = self.max_health
        self.speed = self.settings.scale_value(self.fighter_attributes.get_attribute('speed'))
        self.jump_power = self.settings.scale_value(self.fighter_attributes.get_attribute('jump_power'))
        self.dash_power = self.settings.scale_value(self.fighter_attributes.get_attribute('dash_power'))
        self.attack_damage = self.fighter_attributes.get_attribute('attack_damage')
        self.defense = self.fighter_attributes.get_attribute('defense')
        self.weight = self.fighter_attributes.get_attribute('weight')
        
        # Movement states
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.dash_right = False
        self.dash_left = False
        self.blocking = False
        self.attack_1 = False
        self.attack_2 = False
        self.is_attacking_1 = False
        self.is_attacking_2 = False
        self.is_stunned = False
        self.is_dead = False

        # Attack properties (can be customized per fighter)
        self.attack_1_start_time = 0
        self.attack_1_duration = 200  # milliseconds
        self.attack_2_start_time = 0
        self.attack_2_duration = 400  # milliseconds

        # Hitbox properties (based on fighter attributes)
        attack_range = self.fighter_attributes.get_attribute('attack_range')
        base_width = int(125 * attack_range) if attack_range else 125
        
        self.attack_1_hitbox_width = base_width
        self.attack_1_hitbox_height = 320
        self.attack_1_hitbox_offset_x_right = -50
        self.attack_1_hitbox_offset_x_left = -self.attack_1_hitbox_width + 5
        self.attack_1_hitbox_offset_y = 0
        self.attack_1_hitbox_rect = pygame.Rect(0, 0, 0, 0)

        self.attack_2_hitbox_width = base_width
        self.attack_2_hitbox_height = 320
        self.attack_2_hitbox_offset_x_right = -50
        self.attack_2_hitbox_offset_x_left = -self.attack_2_hitbox_width + 5
        self.attack_2_hitbox_offset_y = 0
        self.attack_2_hitbox_rect = pygame.Rect(0, 0, 0, 0)

        # Dash variables
        self.last_press_time = 0
        self.double_press_window = 200  # milliseconds
        self.is_dashing = False
        self.dash_start_time = 0
        self.dash_duration = 100

        # Physics variables
        self.vel_y = 0.0
        self.on_ground = True
        self.x = float(self.rect.x)
        
        # Dummy-specific AI variables
        if self.is_dummy:
            self.ai_timer = 0
            self.ai_action_delay = 1000  # milliseconds between AI actions
            self.ai_state = 'idle'  # 'idle', 'attacking', 'moving'

    def update(self):
        """Update Fighter based on movement flags and AI (if dummy)."""
        # Handle dummy AI
        if self.is_dummy:
            self._update_dummy_ai()
        
        # Check if fighter is dead
        if self.current_health <= 0 and not self.is_dead:
            self.is_dead = True
            # Handle death animation/logic here
            
        # Skip update if stunned or dead
        if self.is_stunned or self.is_dead:
            return
            
        # Determine current animation based on state
        self._update_animation_state()
        
        # Movement (use fighter's speed attribute)
        if self.moving_right and not self.is_dashing:
            self.rect.x += self.speed
        if self.moving_left and not self.is_dashing:
            self.rect.x -= self.speed

        # Dashing (use fighter's dash power)
        if self.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time < self.dash_duration:
                if self.dash_right:
                    self.rect.x += self.dash_power
                elif self.dash_left: 
                    self.rect.x -= self.dash_power
            else:
                self.is_dashing = False
                self.dash_right = False
                self.dash_left = False 

        # Jumping and gravity (use fighter's jump power)
        if self.jumping and self.on_ground:
            self.vel_y = -self.jump_power
            self.on_ground = False
            self.jumping = False

        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.settings.fighter_gravity
            self.rect.y += self.vel_y
            
            ground_level = self.settings.screen_height - self.rect.height
            if self.rect.y >= ground_level:
                self.rect.y = ground_level
                self.vel_y = 0
                self.on_ground = True

        # Attack states
        self._handle_attack_states()
              
        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
            
        # Update animation and get current frame
        self.image = self.settings.anim_manager.update_animation(self.fighter_id)
        
        # Flip sprite for player 2 or left-facing dummies
        if not self.is_player_1 or (self.is_dummy and self._should_face_left()):
            self.image = pygame.transform.flip(self.image, True, False)

    def _update_dummy_ai(self):
        """Simple AI for dummy characters."""
        current_time = pygame.time.get_ticks()
        
        if current_time - self.ai_timer > self.ai_action_delay:
            self.ai_timer = current_time
            
            # Simple AI logic
            import random
            action = random.choice(['idle', 'move_left', 'move_right', 'attack', 'jump'])
            
            # Reset movement states
            self.moving_left = False
            self.moving_right = False
            
            if action == 'move_left':
                self.moving_left = True
                self.ai_state = 'moving'
            elif action == 'move_right':
                self.moving_right = True
                self.ai_state = 'moving'
            elif action == 'attack':
                self.start_attack_1()
                self.ai_state = 'attacking'
            elif action == 'jump':
                self.jumping = True
            else:
                self.ai_state = 'idle'

    def _should_face_left(self) -> bool:
        """Determine if dummy should face left (simple logic)."""
        # This could be expanded with more sophisticated AI
        return self.moving_left

    def _handle_attack_states(self):
        """Handle attack timing and hitboxes."""
        current_time = pygame.time.get_ticks()
        
        # Attack 1
        if self.is_attacking_1:
            if current_time - self.attack_1_start_time < self.attack_1_duration:
                self._update_attack_hitbox(1)
            else:
                self.is_attacking_1 = False
                self.attack_1_hitbox_rect.size = (0, 0)

        # Attack 2
        if self.is_attacking_2:
            if current_time - self.attack_2_start_time < self.attack_2_duration:
                self._update_attack_hitbox(2)
            else:
                self.is_attacking_2 = False
                self.attack_2_hitbox_rect.size = (0, 0)

    def _update_attack_hitbox(self, attack_num: int):
        """Update attack hitbox position."""
        if attack_num == 1:
            hitbox_rect = self.attack_1_hitbox_rect
            width = self.attack_1_hitbox_width
            height = self.attack_1_hitbox_height
            offset_x_right = self.attack_1_hitbox_offset_x_right
            offset_x_left = self.attack_1_hitbox_offset_x_left
            offset_y = self.attack_1_hitbox_offset_y
        else:
            hitbox_rect = self.attack_2_hitbox_rect
            width = self.attack_2_hitbox_width
            height = self.attack_2_hitbox_height
            offset_x_right = self.attack_2_hitbox_offset_x_right
            offset_x_left = self.attack_2_hitbox_offset_x_left
            offset_y = self.attack_2_hitbox_offset_y
        
        # Determine hitbox position based on facing direction
        if self.is_player_1 or not self._should_face_left():
            hitbox_x = self.rect.x + self.rect.width + offset_x_right
        else:
            hitbox_x = self.rect.x + offset_x_left
        
        hitbox_y = self.rect.y + offset_y
        hitbox_rect.topleft = (hitbox_x, hitbox_y)
        hitbox_rect.width = width
        hitbox_rect.height = height

    def _update_animation_state(self):
        """Update the current animation based on fighter state."""
        current_anim = self.settings.anim_manager.get_current_animation(self.fighter_id)
        
        # Determine what animation should be playing
        if self.is_dead:
            desired_anim = 'death'
        elif self.is_stunned:
            desired_anim = 'stun'
        elif self.is_attacking_1:
            desired_anim = 'attack1'
        elif self.is_attacking_2:
            desired_anim = 'attack2'
        elif self.is_dashing:
            desired_anim = 'dash'
        elif not self.on_ground:
            desired_anim = 'jump'
        elif self.moving_left or self.moving_right:
            desired_anim = 'walk'
        else:
            desired_anim = 'idle'
            
        # Change animation if needed
        if current_anim != desired_anim:
            self.settings.anim_manager.set_animation(self.fighter_id, desired_anim)

    def take_damage(self, damage: int, knockback_force: float = 0):
        """Apply damage to the fighter."""
        if self.blocking:
            damage = max(1, damage // 2)  # Reduce damage when blocking
        
        # Apply defense
        actual_damage = max(1, damage - self.defense)
        self.current_health = max(0, self.current_health - actual_damage)
        
        # Apply knockback (affected by weight)
        if knockback_force > 0:
            knockback = knockback_force / self.weight
            # Apply knockback logic here
            
        # Check for death
        if self.current_health <= 0:
            self.is_dead = True

    def heal(self, amount: int):
        """Heal the fighter."""
        self.current_health = min(self.max_health, self.current_health + amount)

    def start_attack_1(self):
        """Start attack 1."""
        if not self.is_attacking_1 and not self.is_attacking_2 and not self.is_stunned:
            self.is_attacking_1 = True
            self.attack_1_start_time = pygame.time.get_ticks()

    def start_attack_2(self):
        """Start attack 2."""
        if not self.is_attacking_1 and not self.is_attacking_2 and not self.is_stunned:
            self.is_attacking_2 = True
            self.attack_2_start_time = pygame.time.get_ticks()

    def start_dash(self, direction: str):
        """Start dash in given direction."""
        if not self.is_dashing and not self.is_stunned:
            self.is_dashing = True
            self.dash_start_time = pygame.time.get_ticks()
            if direction == 'right':
                self.dash_right = True
                self.dash_left = False
            elif direction == 'left':
                self.dash_left = True
                self.dash_right = False

    def stun(self, duration: int):
        """Stun the fighter for a given duration."""
        self.is_stunned = True
        pygame.time.set_timer(pygame.USEREVENT + 1, duration)  # Custom event for unstun

    def get_health_percentage(self) -> float:
        """Get health as a percentage."""
        return (self.current_health / self.max_health) * 100

    def get_fighter_info(self) -> Dict[str, Any]:
        """Get comprehensive fighter information."""
        return {
            'name': self.fighter_name,
            'health': self.current_health,
            'max_health': self.max_health,
            'health_percentage': self.get_health_percentage(),
            'is_player': not self.is_dummy,
            'is_dead': self.is_dead,
            'is_stunned': self.is_stunned,
            'attributes': self.fighter_attributes.attributes
        }
        
    def draw(self, surface):
        """Draw Fighter onto the screen."""
        # Draw the sprite
        surface.blit(self.image, self.rect)
        
        # Draw debug rectangles (optional)
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 2)

        # Draw Attack hitboxes (for debugging)
        if self.is_attacking_1 and self.attack_1_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (255, 0, 0), self.attack_1_hitbox_rect, 2)

        if self.is_attacking_2 and self.attack_2_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (0, 255, 0), self.attack_2_hitbox_rect, 2)
            
        # Draw health bar for dummies or debug mode
        if self.is_dummy or True:  # Change to debug flag
            self._draw_health_bar(surface)

    def _draw_health_bar(self, surface):
        """Draw health bar above fighter."""
        bar_width = 100
        bar_height = 8
        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15
        
        # Background (red)
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        
        # Health (green)
        health_width = int(bar_width * (self.current_health / self.max_health))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(surface, (255, 255, 255), (bar_x, bar_y, bar_width, bar_height), 1)
            
    def __del__(self):
        """Cleanup when fighter is destroyed."""
        if hasattr(self, 'settings') and hasattr(self.settings, 'anim_manager'):
            self.settings.anim_manager.cleanup_fighter(self.fighter_id)

class FighterAttributes:
    """Base class for fighter attributes and stats."""
    
    def __init__(self, fighter_name: str):
        """Initialize fighter attributes based on fighter name."""
        self.fighter_name = fighter_name
        
        # Base stats that all fighters share
        self.base_stats = {
            'health': 100,
            'speed': 15.0,
            'jump_power': 40.0,
            'dash_power': 50.0,
            'attack_damage': 10,
            'defense': 5,
            'weight': 1.0,
        }
        
        # Fighter-specific attributes
        self.attributes = self._load_fighter_attributes()
        
    def _load_fighter_attributes(self) -> Dict[str, Any]:
        """Load specific attributes for each fighter."""
        fighter_data = {
            'Kevin': {
                'health': 120,
                'speed': 12.0,
                'jump_power': 35.0,
                'dash_power': 45.0,
                'attack_damage': 15,
                'defense': 8,
                'weight': 1.2,
                'special_abilities': ['power_punch', 'ground_slam'],
                'combo_count': 3,
                'attack_range': 1.2,
            },
            'Fire Girl': {
                'health': 90,
                'speed': 18.0,
                'jump_power': 45.0,
                'dash_power': 55.0,
                'attack_damage': 12,
                'defense': 4,
                'weight': 0.8,
                'special_abilities': ['fire_blast', 'flame_dash'],
                'combo_count': 4,
                'attack_range': 1.5,
            }
        }
        
        return fighter_data.get(self.fighter_name, self.base_stats.copy())
    
    def get_attribute(self, attribute_name: str) -> Any:
        """Get a specific attribute value."""
        return self.attributes.get(attribute_name, self.base_stats.get(attribute_name, 0))
    
    def set_attribute(self, attribute_name: str, value: Any):
        """Set a specific attribute value."""
        self.attributes[attribute_name] = value
    
    def modify_attribute(self, attribute_name: str, modifier: float):
        """Modify an attribute by a percentage."""
        current_value = self.get_attribute(attribute_name)
        if isinstance(current_value, (int, float)):
            self.set_attribute(attribute_name, current_value * modifier)

# Factory functions for easy fighter creation
def create_player_fighter(x: int, y: int, fighter_name: str, is_player_1: bool, settings=None) -> Fighter:
    """Create a player-controlled fighter."""
    return Fighter(x, y, fighter_name, is_player_1, settings, is_dummy=False)

def create_dummy_fighter(x: int, y: int, fighter_name: str, settings=None) -> Fighter:
    """Create a dummy/AI fighter."""
    return Fighter(x, y, fighter_name, False, settings, is_dummy=True)
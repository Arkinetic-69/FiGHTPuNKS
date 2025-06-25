import pygame
import time
from enum import Enum

"""This module contains the Mechanics class, which handles various in-game mechanics such as
movement, jumping, attacking, and blocking for characters.
The RoundManager class manages the state of the game rounds.
The GameState class defines the different states of the game,
and the GameStateManager class manages transitions between these states.
To be revised."""

class Mechanics:
    """Class to handle in-game mechanics for a fighter character."""
    
    def __init__(self, fighter):
        """Initialize the mechanics with a fighter instance."""
        self.fighter = fighter
        self.is_jumping = False
        self.is_attacking = False
        self.is_blocking = False
        self.is_dashing = False
        self.health = 100  # Initial health
        self.max_health = 100  # Maximum health
        
        # Physics constants
        self.gravity = 0.8
        self.jump_velocity = -15
        self.dash_speed = 12
        self.normal_speed = 5
        
        # State timers
        self.attack_duration = 0.3  # seconds
        self.dash_duration = 0.2  # seconds
        self.block_cooldown = 0.1  # seconds
        
        # Current state tracking
        self.velocity_y = 0
        self.velocity_x = 0
        self.ground_y = None  # Will be set by game
        self.attack_start_time = 0
        self.dash_start_time = 0
        self.last_block_time = 0
        
        # Combo system
        self.combo_count = 0
        self.last_attack_time = 0
        self.combo_window = 1.0  # seconds

    def jump(self):
        """Handle jumping mechanics."""
        if not self.is_jumping and self.ground_y is not None:
            self.is_jumping = True
            self.velocity_y = self.jump_velocity
            return True
        return False
    
    def attack(self, attack_type="basic"):
        """Handle attacking mechanics."""
        current_time = time.time()
        
        if not self.is_attacking:
            self.is_attacking = True
            self.attack_start_time = current_time
            
            # Combo system
            if current_time - self.last_attack_time <= self.combo_window:
                self.combo_count += 1
            else:
                self.combo_count = 1
            
            self.last_attack_time = current_time
            
            # Create hitbox based on attack type
            damage = self._calculate_attack_damage(attack_type)
            hitbox = self._create_hitbox(attack_type)
            
            return {"damage": damage, "hitbox": hitbox, "combo": self.combo_count}
        return None
    
    def block(self):
        """Handle blocking mechanics."""
        current_time = time.time()
        
        if current_time - self.last_block_time >= self.block_cooldown:
            self.is_blocking = True
            self.last_block_time = current_time
            return True
        return False
    
    def stop_blocking(self):
        """Stop blocking."""
        self.is_blocking = False

    def dash(self, direction):
        """Handle dashing mechanics."""
        current_time = time.time()
        
        if not self.is_dashing:
            self.is_dashing = True
            self.dash_start_time = current_time
            self.velocity_x = self.dash_speed * direction
            return True
        return False
    
    def update_health(self, amount):
        """Update the fighter's health."""
        old_health = self.health
        self.health += amount
        
        if self.health > self.max_health:
            self.health = self.max_health
        elif self.health < 0:
            self.health = 0
            
        return self.health != old_health
    
    def take_damage(self, damage):
        """Apply damage to the fighter, considering blocking."""
        if self.is_blocking:
            # Reduce damage when blocking
            damage *= 0.3
        
        self.update_health(-damage)
        return self.health <= 0  # Return True if fighter is defeated
    
    def heal(self, amount):
        """Heal the fighter."""
        return self.update_health(amount)
    
    def update_physics(self, dt):
        """Update physics-based movement."""
        current_time = time.time()
        
        # Update jumping physics
        if self.is_jumping:
            self.velocity_y += self.gravity
            new_y = self.fighter.y + self.velocity_y
            
            if self.ground_y is not None and new_y >= self.ground_y:
                # Landed
                self.fighter.y = self.ground_y
                self.is_jumping = False
                self.velocity_y = 0
            else:
                self.fighter.y = new_y
        
        # Update dashing
        if self.is_dashing:
            if current_time - self.dash_start_time >= self.dash_duration:
                self.is_dashing = False
                self.velocity_x = 0
            else:
                self.fighter.x += self.velocity_x
        
        # Update attacking
        if self.is_attacking:
            if current_time - self.attack_start_time >= self.attack_duration:
                self.is_attacking = False
    
    def move(self, direction):
        """Handle basic movement."""
        if not self.is_dashing and not self.is_attacking:
            self.fighter.x += self.normal_speed * direction
    
    def set_ground_level(self, ground_y):
        """Set the ground level for physics calculations."""
        self.ground_y = ground_y
    
    def reset_combo(self):
        """Reset the combo counter."""
        self.combo_count = 0
    
    def get_state(self):
        """Get current state information."""
        return {
            "health": self.health,
            "max_health": self.max_health,
            "health_percentage": (self.health / self.max_health) * 100,
            "is_jumping": self.is_jumping,
            "is_attacking": self.is_attacking,
            "is_blocking": self.is_blocking,
            "is_dashing": self.is_dashing,
            "combo_count": self.combo_count,
            "is_defeated": self.health <= 0
        }
    
    def _calculate_attack_damage(self, attack_type):
        """Calculate damage based on attack type and combo."""
        base_damage = {
            "basic": 10,
            "heavy": 20,
            "special": 25
        }.get(attack_type, 10)
        
        # Combo multiplier
        combo_multiplier = 1 + (self.combo_count - 1) * 0.1
        return int(base_damage * combo_multiplier)
    
    def _create_hitbox(self, attack_type):
        """Create hitbox based on attack type."""
        # Basic hitbox rectangles relative to fighter position
        hitboxes = {
            "basic": pygame.Rect(0, 0, 30, 20),
            "heavy": pygame.Rect(0, 0, 50, 30),
            "special": pygame.Rect(0, 0, 60, 40)
        }
        
        hitbox = hitboxes.get(attack_type, hitboxes["basic"])
        hitbox.center = (self.fighter.x + 30, self.fighter.y + 20)  # Adjust based on fighter size
        return hitbox

class RoundManager:
    """Manages round state and transitions."""
    
    def __init__(self, rounds_to_win=2):
        self.rounds_to_win = rounds_to_win
        self.player1_rounds = 0
        self.player2_rounds = 0
        self.current_round = 1
        self.round_time = 99  # seconds
        self.round_start_time = None
        self.is_round_active = False
        
    def start_round(self):
        """Start a new round."""
        self.round_start_time = time.time()
        self.is_round_active = True
        
    def end_round(self, winner):
        """End the current round and update scores."""
        self.is_round_active = False
        
        if winner == 1:
            self.player1_rounds += 1
        elif winner == 2:
            self.player2_rounds += 1
            
        self.current_round += 1
        
    def check_match_winner(self):
        """Check if there's a match winner."""
        if self.player1_rounds >= self.rounds_to_win:
            return 1
        elif self.player2_rounds >= self.rounds_to_win:
            return 2
        return None
        
    def get_remaining_time(self):
        """Get remaining time in current round."""
        if not self.is_round_active or self.round_start_time is None:
            return self.round_time
            
        elapsed = time.time() - self.round_start_time
        remaining = max(0, self.round_time - elapsed)
        return remaining
        
    def is_time_up(self):
        """Check if time is up for current round."""
        return self.get_remaining_time() <= 0
    
class GameState(Enum):
    MENU = "menu"
    CHARACTER_SELECT = "character_select"
    FIGHTING = "fighting"
    ROUND_END = "round_end"
    MATCH_END = "match_end"
    PAUSED = "paused"

class GameStateManager:
    """Manages overall game state transitions and flow."""
    
    def __init__(self):
        self.current_state = GameState.MENU
        self.previous_state = None
        self.round_manager = RoundManager()
        self.player1_character = None
        self.player2_character = None
        self.match_result = None
        
    def change_state(self, new_state):
        """Change to a new game state."""
        self.previous_state = self.current_state
        self.current_state = new_state
        
    def start_match(self, player1_char, player2_char):
        """Start a new match with selected characters."""
        self.player1_character = player1_char
        self.player2_character = player2_char
        self.round_manager = RoundManager()
        self.change_state(GameState.FIGHTING)
        self.round_manager.start_round()
        
    def end_round(self, winner):
        """Handle round ending."""
        self.round_manager.end_round(winner)
        match_winner = self.round_manager.check_match_winner()
        
        if match_winner:
            self.match_result = match_winner
            self.change_state(GameState.MATCH_END)
        else:
            self.change_state(GameState.ROUND_END)
            
    def next_round(self):
        """Start the next round."""
        self.change_state(GameState.FIGHTING)
        self.round_manager.start_round()
        
    def pause_game(self):
        """Pause the game."""
        if self.current_state == GameState.FIGHTING:
            self.change_state(GameState.PAUSED)
            
    def resume_game(self):
        """Resume from pause."""
        if self.current_state == GameState.PAUSED:
            self.change_state(GameState.FIGHTING)
            
    def return_to_menu(self):
        """Return to main menu."""
        self.change_state(GameState.MENU)
        self.round_manager = RoundManager()
        self.match_result = None
        
    def get_game_info(self):
        """Get current game information."""
        return {
            "state": self.current_state,
            "round": self.round_manager.current_round,
            "player1_rounds": self.round_manager.player1_rounds,
            "player2_rounds": self.round_manager.player2_rounds,
            "remaining_time": self.round_manager.get_remaining_time(),
            "match_result": self.match_result
        }
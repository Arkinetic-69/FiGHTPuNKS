import sys
import pygame
from enum import Enum

from settings import get_settings
from fighters import create_player_fighter, create_dummy_fighter
from menu import Menu

"""Main file to run the FiGHTPuNKS game."""

class GameState(Enum):
    """Game state enumeration."""
    MENU = 1
    PLAYING = 2
    PAUSED = 3
    GAME_OVER = 4
    QUIT = 5

class FiGHTPuNKS:
    """Class to manage game assets and behaviour."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        
        # Get singleton settings instance
        self.settings = get_settings()
        
        # Initialize assets
        self.settings.initialize_assets()
        
        # Initialize display
        self._init_display()
        
        # Initialize game components
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MENU
        self.menu = Menu(self.screen)
        
        # Game objects (initialized when game starts)
        self.fighter = None
        self.dummy = None
        self.paused = False
        
        # Game statistics
        self.game_time = 0
        self.round_time = 0
        self.max_round_time = 99  # seconds
        
        # Initialize joystick support
        pygame.joystick.init()
        self.joysticks = []
        self._init_joysticks()
        
        # Start background music
        self._start_background_music()

    def _init_display(self):
        """Initialize the display."""
        flags = 0
        if self.settings.vsync:
            flags |= pygame.DOUBLEBUF
        if self.settings.fullscreen:
            flags |= pygame.FULLSCREEN
            
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height), 
            flags
        )
        pygame.display.set_caption(self.settings.game_title)
        
    def _init_joysticks(self):
        """Initialize joystick controllers."""
        for i in range(pygame.joystick.get_count()):
            joystick = pygame.joystick.Joystick(i)
            joystick.init()
            self.joysticks.append(joystick)
            print(f"Joystick {i}: {joystick.get_name()}")
            
    def _start_background_music(self):
        """Start background music."""
        self.settings.sound_manager.play_music("menu_music.ogg", loop=True)

    def run_game(self):
        """Start the main loop for the game."""
        running = True
        
        while running:
            # Calculate delta time
            dt = self.clock.tick(self.settings.fps) / 1000.0
            
            # Handle events
            self._handle_events()
            
            # Update based on game state
            if self.game_state == GameState.MENU:
                self._update_menu(dt)
            elif self.game_state == GameState.PLAYING:
                self._update_game(dt)
            elif self.game_state == GameState.PAUSED:
                self._update_pause(dt)
            elif self.game_state == GameState.GAME_OVER:
                self._update_game_over(dt)
            elif self.game_state == GameState.QUIT:
                running = False
                
            # Render
            self._render()
            
            # Check for state changes
            if self.menu.should_quit():
                self.game_state = GameState.QUIT
            elif self.menu.should_start_game():
                self._start_new_game()
                
        self._cleanup()

    def _handle_events(self):
        """Handle all pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_state = GameState.QUIT
                
            elif event.type == pygame.JOYDEVICEADDED:
                joystick = pygame.joystick.Joystick(event.device_index)
                joystick.init()
                self.joysticks.append(joystick)
                print(f"Joystick connected: {joystick.get_name()}")
                
            elif event.type == pygame.JOYDEVICEREMOVED:
                for i, joystick in enumerate(self.joysticks):
                    if joystick.get_instance_id() == event.instance_id:
                        self.joysticks.pop(i)
                        print("Joystick disconnected")
                        break
                        
            # Handle events based on game state
            if self.game_state == GameState.MENU:
                self.menu.handle_input(event)
            elif self.game_state == GameState.PLAYING:
                self._handle_game_events(event)
            elif self.game_state == GameState.PAUSED:
                self._handle_pause_events(event)

    def _handle_game_events(self, event):
        """Handle events during gameplay."""
        if event.type == pygame.KEYDOWN:
            # Pause game
            if event.key == pygame.K_ESCAPE:
                self._toggle_pause()
                return
                
            self._handle_keydown_events(event)
            
        elif event.type == pygame.KEYUP:
            self._handle_keyup_events(event)
            
        elif event.type == pygame.JOYBUTTONDOWN:
            self._handle_joystick_events(event)

    def _handle_keydown_events(self, event):
        """Handle keyboard press events."""
        if not self.fighter or not self.dummy:
            return
            
        # Player 1 Controls (WASD + XC)
        if event.key == pygame.K_d:
            self.fighter.moving_right = True
            self._handle_dash(self.fighter, 'right')
        elif event.key == pygame.K_a:
            self.fighter.moving_left = True
            self._handle_dash(self.fighter, 'left')
        elif event.key == pygame.K_w:
            self.fighter.jumping = True
        elif event.key == pygame.K_s:
            self.fighter.blocking = True
        elif event.key == pygame.K_x:
            self.fighter.start_attack_1()
            self.settings.sound_manager.play_fighter_sound(self.fighter.fighter_name, 'attack1')
        elif event.key == pygame.K_c:
            self.fighter.start_attack_2()
            self.settings.sound_manager.play_fighter_sound(self.fighter.fighter_name, 'attack2')
            
        # Player 2 Controls (Arrow keys + M,N)
        elif event.key == pygame.K_RIGHT:
            self.dummy.moving_right = True
            self._handle_dash(self.dummy, 'right')
        elif event.key == pygame.K_LEFT:
            self.dummy.moving_left = True
            self._handle_dash(self.dummy, 'left')
        elif event.key == pygame.K_UP:
            self.dummy.jumping = True
        elif event.key == pygame.K_DOWN:
            self.dummy.blocking = True
        elif event.key == pygame.K_m:
            self.dummy.start_attack_1()
            self.settings.sound_manager.play_fighter_sound(self.dummy.fighter_name, 'attack1')
        elif event.key == pygame.K_n:
            self.dummy.start_attack_2()
            self.settings.sound_manager.play_fighter_sound(self.dummy.fighter_name, 'attack2')

    def _handle_keyup_events(self, event):
        """Handle keyboard release events."""
        if not self.fighter or not self.dummy:
            return
            
        # Player 1 Controls
        if event.key == pygame.K_d:
            self.fighter.moving_right = False
        elif event.key == pygame.K_a:
            self.fighter.moving_left = False
        elif event.key == pygame.K_s:
            self.fighter.blocking = False
            
        # Player 2 Controls
        elif event.key == pygame.K_RIGHT:
            self.dummy.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.dummy.moving_left = False
        elif event.key == pygame.K_DOWN:
            self.dummy.blocking = False

    def _handle_dash(self, fighter, direction):
        """Handle dash input with double-tap detection."""
        current_time = pygame.time.get_ticks()
        if current_time - fighter.last_press_time <= fighter.double_press_window:
            fighter.start_dash(direction)
            self.settings.sound_manager.play_fighter_sound(fighter.fighter_name, 'dash')
        fighter.last_press_time = current_time

    def _handle_joystick_events(self, event):
        """Handle joystick button events."""
        # Implement joystick controls here
        pass

    def _handle_pause_events(self, event):
        """Handle events while paused."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._toggle_pause()
            elif event.key == pygame.K_r:
                self._restart_round()

    def _update_menu(self, dt):
        """Update menu state."""
        self.menu.update(dt)

    def _update_game(self, dt):
        """Update game state."""
        if not self.fighter or not self.dummy:
            return
            
        # Update game time
        self.game_time += dt
        self.round_time += dt
        
        # Update fighters
        self.fighter.update()
        self.dummy.update()
        
        # Check collisions
        self._check_collisions()
        
        # Check win conditions
        self._check_win_conditions()
        
        # Update statistics
        self._update_statistics(dt)

    def _update_pause(self, dt):
        """Update pause state."""
        pass  # Pause doesn't need updates

    def _update_game_over(self, dt):
        """Update game over state."""
        # Auto return to menu after some time
        if self.game_time > 5.0:  # 5 seconds
            self.game_state = GameState.MENU

    def _check_collisions(self):
        """Check for collisions between fighters."""
        if not self.fighter or not self.dummy:
            return
            
        # Check attack collisions
        if self.fighter.is_attacking_1 and self.fighter.attack_1_hitbox_rect.colliderect(self.dummy.rect):
            if not self.dummy.blocking:
                damage = self.fighter.attack_damage
                self.dummy.take_damage(damage)
                self.settings.sound_manager.play_hit_sound('hit')
                self._update_combat_stats('player1', damage)
                
        if self.fighter.is_attacking_2 and self.fighter.attack_2_hitbox_rect.colliderect(self.dummy.rect):
            if not self.dummy.blocking:
                damage = self.fighter.attack_damage * 1.5  # Stronger attack
                self.dummy.take_damage(damage)
                self.settings.sound_manager.play_hit_sound('heavy_hit')
                self._update_combat_stats('player1', damage)
                
        # Same for dummy attacks
        if self.dummy.is_attacking_1 and self.dummy.attack_1_hitbox_rect.colliderect(self.fighter.rect):
            if not self.fighter.blocking:
                damage = self.dummy.attack_damage
                self.fighter.take_damage(damage)
                self.settings.sound_manager.play_hit_sound('hit')
                self._update_combat_stats('player2', damage)
                
        if self.dummy.is_attacking_2 and self.dummy.attack_2_hitbox_rect.colliderect(self.fighter.rect):
            if not self.fighter.blocking:
                damage = self.dummy.attack_damage * 1.5
                self.fighter.take_damage(damage)
                self.settings.sound_manager.play_hit_sound('heavy_hit')
                self._update_combat_stats('player2', damage)

    def _check_win_conditions(self):
        """Check for win/lose conditions."""
        if not self.fighter or not self.dummy:
            return
            
        # Check if either fighter is dead
        if self.fighter.is_dead:
            self._end_round('player2')
        elif self.dummy.is_dead:
            self._end_round('player1')
        elif self.round_time >= self.max_round_time:
            # Time out - determine winner by health
            if self.fighter.current_health > self.dummy.current_health:
                self._end_round('player1')
            elif self.dummy.current_health > self.fighter.current_health:
                self._end_round('player2')
            else:
                self._end_round('draw')

    def _start_new_game(self):
        """Start a new game."""
        self.game_state = GameState.PLAYING
        
        # Create fighters with scaled positions
        p1_x = int(self.settings.scale_value(150))
        p1_y = int(self.settings.scale_value(210))
        p2_x = int(self.settings.scale_value(890))
        p2_y = int(self.settings.scale_value(210))
        
        self.fighter = create_player_fighter(p1_x, p1_y, 'Kevin', True, self.settings)
        self.dummy = create_player_fighter(p2_x, p2_y, 'Fire Girl', False, self.settings)
        
        # Reset game timers
        self.game_time = 0
        self.round_time = 0
        
        # Update statistics
        self.settings.increment_stat('session', 'session', 'games_played')
        self.settings.increment_stat('fighters', 'Kevin', 'times_played')
        self.settings.increment_stat('fighters', 'Fire Girl', 'times_played')
        
        # Change background music
        self.settings.sound_manager.play_music("battle_music.ogg", loop=True)

    def _end_round(self, winner):
        """End the current round."""
        self.game_state = GameState.GAME_OVER
        
        if winner == 'player1':
            self.settings.increment_stat('players', 'player1', 'wins')
            self.settings.increment_stat('players', 'player2', 'losses')
            self.settings.increment_stat('fighters', 'Kevin', 'wins')
            self.settings.increment_stat('fighters', 'Fire Girl', 'losses')
        elif winner == 'player2':
            self.settings.increment_stat('players', 'player2', 'wins')
            self.settings.increment_stat('players', 'player1', 'losses')
            self.settings.increment_stat('fighters', 'Fire Girl', 'wins')
            self.settings.increment_stat('fighters', 'Kevin', 'losses')
            
        # Save statistics
        self.settings.save_stats()
        
        # Play victory sound
        self.settings.sound_manager.play_sound('sfx/victory.wav')

    def _toggle_pause(self):
        """Toggle pause state."""
        if self.game_state == GameState.PLAYING:
            self.game_state = GameState.PAUSED
            self.settings.sound_manager.pause_music()
        elif self.game_state == GameState.PAUSED:
            self.game_state = GameState.PLAYING
            self.settings.sound_manager.resume_music()

    def _restart_round(self):
        """Restart the current round."""
        self.game_state = GameState.PLAYING
        if self.fighter:
            self.fighter.current_health = self.fighter.max_health
            self.fighter.is_dead = False
        if self.dummy:
            self.dummy.current_health = self.dummy.max_health
            self.dummy.is_dead = False
        self.round_time = 0

    def _update_statistics(self, dt):
        """Update game statistics."""
        # Update playtime
        current_playtime = self.settings.get_stat('session', 'session', 'total_playtime', 0)
        self.settings.update_stat('session', 'session', 'total_playtime', current_playtime + dt)

    def _update_combat_stats(self, player, damage):
        """Update combat statistics."""
        # Update damage dealt/taken
        if player == 'player1':
            current_dealt = self.settings.get_stat('players', 'player1', 'total_damage_dealt', 0)
            current_taken = self.settings.get_stat('players', 'player2', 'total_damage_taken', 0)
            self.settings.update_stat('players', 'player1', 'total_damage_dealt', current_dealt + damage)
            self.settings.update_stat('players', 'player2', 'total_damage_taken', current_taken + damage)
        else:
            current_dealt = self.settings.get_stat('players', 'player2', 'total_damage_dealt', 0)
            current_taken = self.settings.get_stat('players', 'player1', 'total_damage_taken', 0)
            self.settings.update_stat('players', 'player2', 'total_damage_dealt', current_dealt + damage)
            self.settings.update_stat('players', 'player1', 'total_damage_taken', current_taken + damage)

    def _render(self):
        """Render the current game state."""
        if self.game_state == GameState.MENU:
            self.menu.draw()
        else:
            self._render_game()
            
        pygame.display.flip()

    def _render_game(self):
        """Render the game screen."""
        # Draw background
        bg_image = self.settings.get_background_image('stage1.bmp')
        self.screen.blit(bg_image, (0, 0))
        
        # Draw fighters
        if self.fighter:
            self.fighter.draw(self.screen)
        if self.dummy:
            self.dummy.draw(self.screen)
            
        # Draw UI
        self._draw_ui()
        
        # Draw pause overlay
        if self.game_state == GameState.PAUSED:
            self._draw_pause_overlay()
        elif self.game_state == GameState.GAME_OVER:
            self._draw_game_over_overlay()

    def _draw_ui(self):
        """Draw game UI elements."""
        if not self.fighter or not self.dummy:
            return
            
        # Draw health bars
        self._draw_health_bar(self.fighter, 50, 50, True)
        self._draw_health_bar(self.dummy, self.settings.screen_width - 350, 50, False)
        
        # Draw timer
        time_left = max(0, self.max_round_time - self.round_time)
        timer_font = self.settings.asset_manager.load_font(None, self.settings.get_scaled_font_size(48))
        timer_text = timer_font.render(f"{int(time_left)}", True, (255, 255, 255))
        timer_rect = timer_text.get_rect(center=(self.settings.screen_width // 2, 50))
        self.screen.blit(timer_text, timer_rect)

    def _draw_health_bar(self, fighter, x, y, flip):
        """Draw health bar for a fighter."""
        bar_width = 300
        bar_height = 20
        health_ratio = fighter.current_health / fighter.max_health
        
        # Background
        pygame.draw.rect(self.screen, (255, 0, 0), (x, y, bar_width, bar_height))
        
        # Health
        if flip:
            health_width = int(bar_width * health_ratio)
            pygame.draw.rect(self.screen, (0, 255, 0), (x, y, health_width, bar_height))
        else:
            health_width = int(bar_width * health_ratio)
            health_x = x + bar_width - health_width
            pygame.draw.rect(self.screen, (0, 255, 0), (health_x, y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(self.screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Fighter name
        name_font = self.settings.asset_manager.load_font(None, self.settings.get_scaled_font_size(24))
        name_text = name_font.render(fighter.fighter_name, True, (255, 255, 255))
        if flip:
            self.screen.blit(name_text, (x, y - 30))
        else:
            name_rect = name_text.get_rect()
            name_rect.right = x + bar_width
            name_rect.bottom = y - 10
            self.screen.blit(name_text, name_rect)

    def _draw_pause_overlay(self):
        """Draw pause overlay."""
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        pause_font = self.settings.asset_manager.load_font(None, self.settings.get_scaled_font_size(72))
        pause_text = pause_font.render("PAUSED", True, (255, 255, 255))
        pause_rect = pause_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(pause_text, pause_rect)
        
        instruction_font = self.settings.asset_manager.load_font(None, self.settings.get_scaled_font_size(24))
        instruction_text = instruction_font.render("Press ESC to resume, R to restart", True, (255, 255, 255))
        instruction_rect = instruction_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2 + 100))
        self.screen.blit(instruction_text, instruction_rect)

    def _draw_game_over_overlay(self):
        """Draw game over overlay."""
        overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Determine winner
        if self.fighter and self.dummy:
            if self.fighter.is_dead:
                winner_text = f"{self.dummy.fighter_name} Wins!"
            elif self.dummy.is_dead:
                winner_text = f"{self.fighter.fighter_name} Wins!"
            else:
                winner_text = "Draw!"
        else:
            winner_text = "Game Over"
        
        game_over_font = self.settings.asset_manager.load_font(None, self.settings.get_scaled_font_size(72))
        game_over_surface = game_over_font.render(winner_text, True, (255, 255, 255))
        game_over_rect = game_over_surface.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(game_over_surface, game_over_rect)

    def _cleanup(self):
        """Cleanup resources before exiting."""
        # Save final statistics
        self.settings.save_config()
        self.settings.save_stats()
        
        # Cleanup pygame
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # Create game instance and run
    game = FiGHTPuNKS()
    game.run_game()
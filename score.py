import pygame
import pygame.font
import json
import os
from datetime import datetime

"""This module contains the Scoreboard class, which manages the scoring, round information, etc.
It also includes the GameStats class for tracking game statistics."""

class Scoreboard:
    """Class to report and display scoring information."""
    
    def __init__(self, settings):
        """Initialize scorekeeping attributes."""
        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()
        
        # Font settings for scoring information
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 24)
        self.large_font = pygame.font.SysFont(None, 72)
        
        # Game statistics handler
        self.game_stats = GameStats()
        
        # Current match data
        self.player1_score = 0
        self.player2_score = 0
        self.player1_health = 100
        self.player2_health = 100
        self.current_round = 1
        self.time_remaining = 99
        self.player1_combo = 0
        self.player2_combo = 0
        
        # Display elements
        self.score_images = {}
        self.health_bars = {}
        
        # Prepare initial display elements
        self.prep_all_elements()
    
    def prep_all_elements(self):
        """Prepare all display elements."""
        self.prep_scores()
        self.prep_health_bars()
        self.prep_round_info()
        self.prep_timer()
        self.prep_combos()
    
    def prep_scores(self):
        """Prepare score images."""
        # Player 1 score
        p1_score_str = f"P1: {self.player1_score}"
        self.score_images["p1"] = self.font.render(
            p1_score_str, True, self.text_color, None
        )
        
        # Player 2 score
        p2_score_str = f"P2: {self.player2_score}"
        self.score_images["p2"] = self.font.render(
            p2_score_str, True, self.text_color, None
        )
        
        # Position scores
        self.score_images["p1_rect"] = self.score_images["p1"].get_rect()
        self.score_images["p1_rect"].left = 20
        self.score_images["p1_rect"].top = 20
        
        self.score_images["p2_rect"] = self.score_images["p2"].get_rect()
        self.score_images["p2_rect"].right = self.screen_rect.right - 20
        self.score_images["p2_rect"].top = 20
    
    def prep_health_bars(self):
        """Prepare health bar displays."""
        bar_width = 300
        bar_height = 20
        
        # Player 1 health bar
        p1_health_ratio = self.player1_health / 100
        p1_health_width = int(bar_width * p1_health_ratio)
        
        self.health_bars["p1_bg"] = pygame.Rect(50, 70, bar_width, bar_height)
        self.health_bars["p1_fill"] = pygame.Rect(50, 70, p1_health_width, bar_height)
        
        # Player 2 health bar
        p2_health_ratio = self.player2_health / 100
        p2_health_width = int(bar_width * p2_health_ratio)
        p2_x = self.screen_rect.right - 350
        
        self.health_bars["p2_bg"] = pygame.Rect(p2_x, 70, bar_width, bar_height)
        self.health_bars["p2_fill"] = pygame.Rect(p2_x, 70, p2_health_width, bar_height)
        
        # Health text
        p1_health_text = f"{int(self.player1_health)}%"
        p2_health_text = f"{int(self.player2_health)}%"
        
        self.health_bars["p1_text"] = self.small_font.render(
            p1_health_text, True, self.text_color
        )
        self.health_bars["p2_text"] = self.small_font.render(
            p2_health_text, True, self.text_color
        )
        
        self.health_bars["p1_text_rect"] = self.health_bars["p1_text"].get_rect()
        self.health_bars["p1_text_rect"].center = self.health_bars["p1_bg"].center
        
        self.health_bars["p2_text_rect"] = self.health_bars["p2_text"].get_rect()
        self.health_bars["p2_text_rect"].center = self.health_bars["p2_bg"].center
    
    def prep_round_info(self):
        """Prepare round information display."""
        round_text = f"Round {self.current_round}"
        self.round_image = self.font.render(round_text, True, self.text_color)
        self.round_rect = self.round_image.get_rect()
        self.round_rect.centerx = self.screen_rect.centerx
        self.round_rect.top = 20
    
    def prep_timer(self):
        """Prepare timer display."""
        timer_text = f"{int(self.time_remaining):02d}"
        self.timer_image = self.large_font.render(timer_text, True, self.text_color)
        self.timer_rect = self.timer_image.get_rect()
        self.timer_rect.centerx = self.screen_rect.centerx
        self.timer_rect.top = 100
    
    def prep_combos(self):
        """Prepare combo displays."""
        if self.player1_combo > 1:
            combo_text = f"Combo: {self.player1_combo}"
            self.combo_images["p1"] = self.small_font.render(
                combo_text, True, (255, 255, 0)
            )
            self.combo_images["p1_rect"] = self.combo_images["p1"].get_rect()
            self.combo_images["p1_rect"].left = 50
            self.combo_images["p1_rect"].top = 100
        else:
            self.combo_images["p1"] = None
        
        if self.player2_combo > 1:
            combo_text = f"Combo: {self.player2_combo}"
            self.combo_images["p2"] = self.small_font.render(
                combo_text, True, (255, 255, 0)
            )
            self.combo_images["p2_rect"] = self.combo_images["p2"].get_rect()
            self.combo_images["p2_rect"].right = self.screen_rect.right - 50
            self.combo_images["p2_rect"].top = 100
        else:
            self.combo_images["p2"] = None
    
    def update_scores(self, p1_score, p2_score):
        """Update player scores."""
        self.player1_score = p1_score
        self.player2_score = p2_score
        self.prep_scores()
    
    def update_health(self, p1_health, p2_health):
        """Update player health."""
        self.player1_health = max(0, min(100, p1_health))
        self.player2_health = max(0, min(100, p2_health))
        self.prep_health_bars()
    
    def update_round(self, round_num):
        """Update round information."""
        self.current_round = round_num
        self.prep_round_info()
    
    def update_timer(self, time_remaining):
        """Update timer display."""
        self.time_remaining = max(0, time_remaining)
        self.prep_timer()
    
    def update_combos(self, p1_combo, p2_combo):
        """Update combo displays."""
        self.player1_combo = p1_combo
        self.player2_combo = p2_combo
        
        # Record combo achievements
        if p1_combo > 1:
            self.game_stats.record_combo(p1_combo)
        if p2_combo > 1:
            self.game_stats.record_combo(p2_combo)
        
        # Initialize combo_images if not exists
        if not hasattr(self, 'combo_images'):
            self.combo_images = {}
        
        self.prep_combos()
    
    def record_damage(self, damage):
        """Record damage dealt for statistics."""
        self.game_stats.record_damage(damage)
    
    def record_match_end(self, winner, rounds_played, p1_rounds, p2_rounds):
        """Record match completion."""
        self.game_stats.record_match_result(winner, rounds_played, p1_rounds, p2_rounds)
    
    def show_scoreboard(self):
        """Display all scoreboard elements."""
        # Draw scores
        self.screen.blit(self.score_images["p1"], self.score_images["p1_rect"])
        self.screen.blit(self.score_images["p2"], self.score_images["p2_rect"])
        
        # Draw health bars
        # Background (dark red)
        pygame.draw.rect(self.screen, (100, 0, 0), self.health_bars["p1_bg"])
        pygame.draw.rect(self.screen, (100, 0, 0), self.health_bars["p2_bg"])
        
        # Health fill (green to red gradient based on health)
        p1_color = self._get_health_color(self.player1_health)
        p2_color = self._get_health_color(self.player2_health)
        
        pygame.draw.rect(self.screen, p1_color, self.health_bars["p1_fill"])
        pygame.draw.rect(self.screen, p2_color, self.health_bars["p2_fill"])
        
        # Health text
        self.screen.blit(self.health_bars["p1_text"], self.health_bars["p1_text_rect"])
        self.screen.blit(self.health_bars["p2_text"], self.health_bars["p2_text_rect"])
        
        # Draw round info
        self.screen.blit(self.round_image, self.round_rect)
        
        # Draw timer
        # Change color if time is running low
        if self.time_remaining <= 10:
            timer_color = (255, 0, 0)  # Red
        elif self.time_remaining <= 30:
            timer_color = (255, 255, 0)  # Yellow
        else:
            timer_color = self.text_color  # White
        
        timer_text = f"{int(self.time_remaining):02d}"
        timer_image = self.large_font.render(timer_text, True, timer_color)
        self.screen.blit(timer_image, self.timer_rect)
        
        # Draw combos
        if hasattr(self, 'combo_images'):
            if self.combo_images.get("p1"):
                self.screen.blit(self.combo_images["p1"], self.combo_images["p1_rect"])
            if self.combo_images.get("p2"):
                self.screen.blit(self.combo_images["p2"], self.combo_images["p2_rect"])
    
    def _get_health_color(self, health_percent):
        """Get color based on health percentage."""
        if health_percent > 60:
            return (0, 255, 0)  # Green
        elif health_percent > 30:
            return (255, 255, 0)  # Yellow
        else:
            return (255, 0, 0)  # Red
    
    def show_match_end_screen(self, winner):
        """Display match end information."""
        # Winner announcement
        if winner == 1:
            winner_text = "Player 1 Wins!"
        elif winner == 2:
            winner_text = "Player 2 Wins!"
        else:
            winner_text = "Draw!"
        
        winner_image = self.large_font.render(winner_text, True, (255, 255, 0))
        winner_rect = winner_image.get_rect()
        winner_rect.center = self.screen_rect.center
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.screen_rect.width, self.screen_rect.height))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(winner_image, winner_rect)
        
        # Show session stats
        stats = self.game_stats.get_session_stats()
        stats_y = winner_rect.bottom + 50
        
        stats_text = [
            f"Matches Played: {stats['matches_played']}",
            f"P1 Wins: {stats['player1_wins']}",
            f"P2 Wins: {stats['player2_wins']}",
            f"Longest Combo: {stats['longest_combo']}"
        ]
        
        for i, text in enumerate(stats_text):
            stat_image = self.font.render(text, True, self.text_color)
            stat_rect = stat_image.get_rect()
            stat_rect.centerx = self.screen_rect.centerx
            stat_rect.y = stats_y + (i * 40)
            self.screen.blit(stat_image, stat_rect)
    
    def get_session_stats(self):
        """Get current session statistics."""
        return self.game_stats.get_session_stats()
    
    def get_all_time_stats(self):
        """Get all-time statistics."""
        return self.game_stats.get_all_time_stats()
    
    def reset_session_stats(self):
        """Reset session statistics."""
        self.game_stats.reset_session()
        
class GameStats:
    """Handles game statistics tracking and persistence."""
    
    def __init__(self, stats_file="game_stats.json"):
        self.stats_file = stats_file
        self.current_session = {
            "matches_played": 0,
            "player1_wins": 0,
            "player2_wins": 0,
            "total_rounds": 0,
            "session_start": datetime.now().isoformat(),
            "longest_combo": 0,
            "total_damage_dealt": 0
        }
        self.all_time_stats = self.load_stats()
    
    def load_stats(self):
        """Load statistics from file."""
        if os.path.exists(self.stats_file):
            try:
                with open(self.stats_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return self._get_default_stats()
        return self._get_default_stats()
    
    def save_stats(self):
        """Save statistics to file."""
        try:
            with open(self.stats_file, 'w') as f:
                json.dump(self.all_time_stats, f, indent=2)
        except Exception as e:
            print(f"Error saving stats: {e}")
    
    def _get_default_stats(self):
        """Get default statistics structure."""
        return {
            "total_matches": 0,
            "total_player1_wins": 0,
            "total_player2_wins": 0,
            "total_rounds_played": 0,
            "highest_combo": 0,
            "total_damage_all_time": 0,
            "play_time_seconds": 0,
            "first_played": datetime.now().isoformat(),
            "last_played": datetime.now().isoformat()
        }
    
    def record_match_result(self, winner, rounds_played, player1_rounds, player2_rounds):
        """Record the result of a completed match."""
        # Update session stats
        self.current_session["matches_played"] += 1
        self.current_session["total_rounds"] += rounds_played
        
        if winner == 1:
            self.current_session["player1_wins"] += 1
        elif winner == 2:
            self.current_session["player2_wins"] += 1
        
        # Update all-time stats
        self.all_time_stats["total_matches"] += 1
        self.all_time_stats["total_rounds_played"] += rounds_played
        self.all_time_stats["last_played"] = datetime.now().isoformat()
        
        if winner == 1:
            self.all_time_stats["total_player1_wins"] += 1
        elif winner == 2:
            self.all_time_stats["total_player2_wins"] += 1
        
        self.save_stats()
    
    def record_combo(self, combo_count):
        """Record a combo achievement."""
        self.current_session["longest_combo"] = max(
            self.current_session["longest_combo"], combo_count
        )
        self.all_time_stats["highest_combo"] = max(
            self.all_time_stats["highest_combo"], combo_count
        )
    
    def record_damage(self, damage):
        """Record damage dealt."""
        self.current_session["total_damage_dealt"] += damage
        self.all_time_stats["total_damage_all_time"] += damage
    
    def get_session_stats(self):
        """Get current session statistics."""
        return self.current_session.copy()
    
    def get_all_time_stats(self):
        """Get all-time statistics."""
        return self.all_time_stats.copy()
    
    def reset_session(self):
        """Reset current session statistics."""
        self.current_session = {
            "matches_played": 0,
            "player1_wins": 0,
            "player2_wins": 0,
            "total_rounds": 0,
            "session_start": datetime.now().isoformat(),
            "longest_combo": 0,
            "total_damage_dealt": 0
        }
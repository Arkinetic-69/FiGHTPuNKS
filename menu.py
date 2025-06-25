import pygame
from settings import get_settings
from typing import List, Tuple, Callable, Optional

"""This module contains the Menu class, which is responsible for displaying
the main menu, options, and other UI elements in the game."""

class Menu:
    """Class to handle the game menu and UI."""
    
    def __init__(self, screen):
        """Initialize the menu with a screen."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.settings = get_settings()
        
        # Initialize assets
        self._setup_fonts()
        self._setup_colors()
        self._setup_menu_items()
        
        # Menu state
        self.current_state = MenuState.MAIN
        self.selected_item = 0
        self.background_image = None
        self.logo_image = None
        
        # Load menu assets
        self._load_menu_assets()
        
        # Animation variables
        self.menu_alpha = 0
        self.fade_in = True
        self.animation_speed = 5
        
    def _setup_fonts(self):
        """Setup fonts with scaling."""
        base_title_size = 72
        base_menu_size = 36
        base_small_size = 24
        
        # Scale fonts based on resolution
        title_size = self.settings.get_scaled_font_size(base_title_size)
        menu_size = self.settings.get_scaled_font_size(base_menu_size)
        small_size = self.settings.get_scaled_font_size(base_small_size)
        
        self.title_font = self.settings.asset_manager.load_font(None, title_size)
        self.menu_font = self.settings.asset_manager.load_font(None, menu_size)
        self.small_font = self.settings.asset_manager.load_font(None, small_size)
        
    def _setup_colors(self):
        """Setup color scheme."""
        self.colors = {
            'background': (20, 25, 40),
            'text_normal': (200, 200, 200),
            'text_selected': (255, 255, 255),
            'text_disabled': (100, 100, 100),
            'accent': (255, 100, 50),
            'title': (255, 255, 255),
            'overlay': (0, 0, 0, 128)
        }
        
    def _load_menu_assets(self):
        """Load menu-specific assets."""
        try:
            # Try to load background image
            self.background_image = self.settings.get_background_image('menu_bg.png')
        except:
            # Create gradient background if no image
            self.background_image = self._create_gradient_background()
            
        try:
            # Try to load logo
            self.logo_image = self.settings.asset_manager.load_image('ui/logo.png')
            # Scale logo
            logo_width = int(self.settings.scale_value(400))
            logo_height = int(self.settings.scale_value(200))
            self.logo_image = pygame.transform.scale(self.logo_image, (logo_width, logo_height))
        except:
            self.logo_image = None
            
    def _create_gradient_background(self) -> pygame.Surface:
        """Create a gradient background."""
        surface = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
        
        # Create vertical gradient
        for y in range(self.settings.screen_height):
            ratio = y / self.settings.screen_height
            color = (
                int(20 + ratio * 40),
                int(25 + ratio * 50),
                int(40 + ratio * 80)
            )
            pygame.draw.line(surface, color, (0, y), (self.settings.screen_width, y))
            
        return surface
        
    def _setup_menu_items(self):
        """Setup menu items for different states."""
        self.menu_structure = {
            MenuState.MAIN: [
                MenuItem("Start Game", self._start_game),
                MenuItem("Options", lambda: self._change_state(MenuState.OPTIONS)),
                MenuItem("Exit", lambda: self._change_state(MenuState.QUIT))
            ],
            MenuState.OPTIONS: [
                MenuItem("Graphics", lambda: self._change_state(MenuState.GRAPHICS)),
                MenuItem("Audio", lambda: self._change_state(MenuState.AUDIO)),
                MenuItem("Controls", lambda: self._change_state(MenuState.CONTROLS)),
                MenuItem("Back", lambda: self._change_state(MenuState.MAIN))
            ],
            MenuState.GRAPHICS: [
                MenuItem(f"Resolution: {self.settings.screen_width}x{self.settings.screen_height}", 
                        self._cycle_resolution),
                MenuItem(f"Fullscreen: {'On' if self.settings.fullscreen else 'Off'}", 
                        self._toggle_fullscreen),
                MenuItem("Back", lambda: self._change_state(MenuState.OPTIONS))
            ],
            MenuState.AUDIO: [
                MenuItem(f"Master Volume: {int(self.settings.sound_manager.master_volume * 100)}%", 
                        lambda: self._adjust_volume('master')),
                MenuItem(f"Music Volume: {int(self.settings.sound_manager.music_volume * 100)}%", 
                        lambda: self._adjust_volume('music')),
                MenuItem(f"SFX Volume: {int(self.settings.sound_manager.sfx_volume * 100)}%", 
                        lambda: self._adjust_volume('sfx')),
                MenuItem(f"Audio: {'On' if self.settings.sound_manager.enabled else 'Off'}", 
                        self._toggle_audio),
                MenuItem("Back", lambda: self._change_state(MenuState.OPTIONS))
            ],
            MenuState.CONTROLS: [
                MenuItem("Player 1 Controls", self._show_controls_p1),
                MenuItem("Player 2 Controls", self._show_controls_p2),
                MenuItem("Reset to Defaults", self._reset_controls),
                MenuItem("Back", lambda: self._change_state(MenuState.OPTIONS))
            ]
        }
        
    def update(self, dt: float):
        """Update menu animations and state."""
        # Handle fade in animation
        if self.fade_in and self.menu_alpha < 255:
            self.menu_alpha += self.animation_speed * dt * 60
            if self.menu_alpha >= 255:
                self.menu_alpha = 255
                self.fade_in = False
                
    def handle_input(self, event):
        """Handle input events."""
        if event.type == pygame.KEYDOWN:
            # Play navigation sound
            self.settings.sound_manager.play_ui_sound('navigate', 0.5)
            
            if event.key == pygame.K_UP:
                self._navigate_up()
            elif event.key == pygame.K_DOWN:
                self._navigate_down()
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._select_item()
            elif event.key == pygame.K_ESCAPE:
                self._handle_back()
            elif event.key == pygame.K_LEFT:
                self._handle_left()
            elif event.key == pygame.K_RIGHT:
                self._handle_right()
                
    def _navigate_up(self):
        """Navigate up in menu."""
        current_items = self.menu_structure[self.current_state]
        if current_items:
            self.selected_item = (self.selected_item - 1) % len(current_items)
            
    def _navigate_down(self):
        """Navigate down in menu."""
        current_items = self.menu_structure[self.current_state]
        if current_items:
            self.selected_item = (self.selected_item + 1) % len(current_items)
            
    def _select_item(self):
        """Select current menu item."""
        current_items = self.menu_structure[self.current_state]
        if current_items and self.selected_item < len(current_items):
            item = current_items[self.selected_item]
            if item.enabled and item.action:
                # Play selection sound
                self.settings.sound_manager.play_ui_sound('select', 0.7)
                item.action()
                
    def _handle_back(self):
        """Handle back/escape action."""
        if self.current_state == MenuState.MAIN:
            self._change_state(MenuState.QUIT)
        else:
            self._change_state(MenuState.MAIN)
            
    def _handle_left(self):
        """Handle left arrow for value adjustment."""
        if self.current_state == MenuState.AUDIO:
            self._adjust_volume_direction(-0.1)
        elif self.current_state == MenuState.GRAPHICS:
            self._adjust_graphics_setting(-1)
            
    def _handle_right(self):
        """Handle right arrow for value adjustment."""
        if self.current_state == MenuState.AUDIO:
            self._adjust_volume_direction(0.1)
        elif self.current_state == MenuState.GRAPHICS:
            self._adjust_graphics_setting(1)
            
    def _change_state(self, new_state: str):
        """Change menu state."""
        self.current_state = new_state
        self.selected_item = 0
        self._refresh_menu_items()
        
    def _refresh_menu_items(self):
        """Refresh menu items with current values."""
        if self.current_state == MenuState.GRAPHICS:
            items = self.menu_structure[MenuState.GRAPHICS]
            items[0].text = f"Resolution: {self.settings.screen_width}x{self.settings.screen_height}"
            items[1].text = f"Fullscreen: {'On' if self.settings.fullscreen else 'Off'}"
            
        elif self.current_state == MenuState.AUDIO:
            items = self.menu_structure[MenuState.AUDIO]
            items[0].text = f"Master Volume: {int(self.settings.sound_manager.master_volume * 100)}%"
            items[1].text = f"Music Volume: {int(self.settings.sound_manager.music_volume * 100)}%"
            items[2].text = f"SFX Volume: {int(self.settings.sound_manager.sfx_volume * 100)}%"
            items[3].text = f"Audio: {'On' if self.settings.sound_manager.enabled else 'Off'}"
            
    def _start_game(self):
        """Start the game."""
        self.settings.sound_manager.play_ui_sound('start_game', 1.0)
        # Signal to main game loop to start
        self.current_state = "start_game"
        
    def _cycle_resolution(self):
        """Cycle through supported resolutions."""
        resolutions = self.settings.get_supported_resolutions()
        current = (self.settings.screen_width, self.settings.screen_height)
        
        try:
            current_index = resolutions.index(current)
            next_index = (current_index + 1) % len(resolutions)
        except ValueError:
            next_index = 0
            
        new_res = resolutions[next_index]
        if self.settings.set_resolution(new_res[0], new_res[1]):
            self._refresh_menu_items()
            
    def _toggle_fullscreen(self):
        """Toggle fullscreen mode."""
        self.settings.fullscreen = not self.settings.fullscreen
        self.settings.config["display"]["fullscreen"] = self.settings.fullscreen
        self._refresh_menu_items()
        
    def _adjust_volume(self, volume_type: str):
        """Adjust volume for specific type."""
        pass  # This will be handled by left/right arrows
        
    def _adjust_volume_direction(self, direction: float):
        """Adjust volume in specified direction."""
        current_items = self.menu_structure[MenuState.AUDIO]
        selected_text = current_items[self.selected_item].text.lower()
        
        if 'master' in selected_text:
            new_volume = max(0.0, min(1.0, self.settings.sound_manager.master_volume + direction))
            self.settings.sound_manager.set_master_volume(new_volume)
        elif 'music' in selected_text:
            new_volume = max(0.0, min(1.0, self.settings.sound_manager.music_volume + direction))
            self.settings.sound_manager.set_music_volume(new_volume)
        elif 'sfx' in selected_text:
            new_volume = max(0.0, min(1.0, self.settings.sound_manager.sfx_volume + direction))
            self.settings.sound_manager.set_sfx_volume(new_volume)
            
        self._refresh_menu_items()
        
    def _toggle_audio(self):
        """Toggle audio on/off."""
        if self.settings.sound_manager.enabled:
            self.settings.sound_manager.disable_audio()
        else:
            self.settings.sound_manager.enable_audio()
        self._refresh_menu_items()
        
    def _adjust_graphics_setting(self, direction: int):
        """Adjust graphics settings with left/right arrows."""
        # This could be expanded for more graphics options
        pass
        
    def _show_controls_p1(self):
        """Show Player 1 controls."""
        # Implementation for showing controls
        pass
        
    def _show_controls_p2(self):
        """Show Player 2 controls."""
        # Implementation for showing controls
        pass
        
    def _reset_controls(self):
        """Reset controls to defaults."""
        # Implementation for resetting controls
        pass
        
    def draw(self):
        """Draw the menu on the screen."""
        # Draw background
        if self.background_image:
            self.screen.blit(self.background_image, (0, 0))
        else:
            self.screen.fill(self.colors['background'])
            
        # Draw logo if available and on main menu
        if self.logo_image and self.current_state == MenuState.MAIN:
            logo_rect = self.logo_image.get_rect()
            logo_rect.centerx = self.screen_rect.centerx
            logo_rect.y = int(self.settings.scale_value(50))
            self.screen.blit(self.logo_image, logo_rect)
            
        # Draw title
        self._draw_title()
        
        # Draw menu items
        self._draw_menu_items()
        
        # Draw instructions
        self._draw_instructions()
        
        # Apply fade effect if needed
        if self.menu_alpha < 255:
            overlay = pygame.Surface((self.settings.screen_width, self.settings.screen_height))
            overlay.set_alpha(255 - self.menu_alpha)
            overlay.fill((0, 0, 0))
            self.screen.blit(overlay, (0, 0))
            
    def _draw_title(self):
        """Draw menu title."""
        if self.current_state == MenuState.MAIN and self.logo_image:
            return  # Logo serves as title
            
        title_text = self._get_title_text()
        title_surface = self.title_font.render(title_text, True, self.colors['title'])
        title_rect = title_surface.get_rect()
        title_rect.centerx = self.screen_rect.centerx
        title_rect.y = int(self.settings.scale_value(100))
        self.screen.blit(title_surface, title_rect)
        
    def _get_title_text(self) -> str:
        """Get title text for current state."""
        titles = {
            MenuState.MAIN: "FiGHTPuNKS",
            MenuState.OPTIONS: "Options",
            MenuState.GRAPHICS: "Graphics Settings",
            MenuState.AUDIO: "Audio Settings",
            MenuState.CONTROLS: "Controls"
        }
        return titles.get(self.current_state, "Menu")
        
    def _draw_menu_items(self):
        """Draw menu items."""
        current_items = self.menu_structure.get(self.current_state, [])
        
        # Calculate starting position
        total_height = len(current_items) * int(self.settings.scale_value(60))
        start_y = (self.screen_rect.centery - total_height // 2) + int(self.settings.scale_value(100))
        
        for index, item in enumerate(current_items):
            # Determine color
            if index == self.selected_item:
                color = self.colors['text_selected']
                # Draw selection indicator
                indicator_size = int(self.settings.scale_value(20))
                indicator_x = self.screen_rect.centerx - int(self.settings.scale_value(200))
                indicator_y = start_y + index * int(self.settings.scale_value(60)) + indicator_size // 2
                pygame.draw.polygon(self.screen, self.colors['accent'], [
                    (indicator_x, indicator_y),
                    (indicator_x + indicator_size, indicator_y + indicator_size // 2),
                    (indicator_x, indicator_y + indicator_size)
                ])
            elif not item.enabled:
                color = self.colors['text_disabled']
            else:
                color = self.colors['text_normal']
                
            # Render text
            text_surface = self.menu_font.render(item.text, True, color)
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.screen_rect.centerx
            text_rect.y = start_y + index * int(self.settings.scale_value(60))
            self.screen.blit(text_surface, text_rect)
            
    def _draw_instructions(self):
        """Draw control instructions."""
        instructions = [
            "↑↓ Navigate",
            "← → Adjust Values",
            "Enter Select",
            "Esc Back"
        ]
        
        instruction_text = " | ".join(instructions)
        instruction_surface = self.small_font.render(instruction_text, True, self.colors['text_normal'])
        instruction_rect = instruction_surface.get_rect()
        instruction_rect.centerx = self.screen_rect.centerx
        instruction_rect.bottom = self.screen_rect.bottom - int(self.settings.scale_value(20))
        self.screen.blit(instruction_surface, instruction_rect)
        
    def should_quit(self) -> bool:
        """Check if user wants to quit."""
        return self.current_state == MenuState.QUIT
        
    def should_start_game(self) -> bool:
        """Check if user wants to start game."""
        return self.current_state == "start_game"
        
    def cleanup(self):
        """Cleanup menu resources."""
        # Save any changed settings
        self.settings.save_config()
        
class MenuState:
    """Enum-like class for menu states."""
    MAIN = "main"
    OPTIONS = "options"
    CONTROLS = "controls"
    AUDIO = "audio"
    GRAPHICS = "graphics"
    QUIT = "quit"

class MenuItem:
    """Represents a menu item with action and state."""
    
    def __init__(self, text: str, action: Callable = None, value: str = None):
        """Initialize menu item."""
        self.text = text
        self.action = action
        self.value = value
        self.enabled = True
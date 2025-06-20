import pygame

"""Handles displaying the ui.
This module contains the Menu class, which is responsible for displaying
the main menu, options, and other UI elements in the game."""

class Menu:
    """Class to handle the game menu and UI."""
    
    def __init__(self, screen):
        """Initialize the menu with a screen."""
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.font = pygame.font.SysFont(None, 48)
        self.menu_items = ["Start Game", "Options", "Exit"]
        self.selected_item = 0

    def draw_menu(self):
        """Draw the menu on the screen."""
        self.screen.fill((0, 0, 0))  # Clear the screen with black
        for index, item in enumerate(self.menu_items):
            color = (255, 255, 255) if index == self.selected_item else (200, 200, 200)
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(self.screen_rect.centerx, 
                                                      self.screen_rect.centery + index * 50))
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()
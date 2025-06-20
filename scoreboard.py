import pygame.font

"""Scoreboard module.
This module contains the Scoreboard class, which is responsible for displaying
scoring information on the screen, such as the player's score."""

class Scoreboard:
    """Class to report scoring information."""
    
    def __init__ (self, settings):
        # not final!!!! <placeholder code block>
        """Initializes scorekeeping attributes."""
        self.settings = settings
        self.screen = settings.screen
        self.screen_rect = self.screen.get_rect()
        
        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Initialize the score
        self.score = 0

        # Prepare the initial score image
        self.prep_score()
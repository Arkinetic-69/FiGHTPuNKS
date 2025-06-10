import pygame

class Settings:
    """Class for settings of the game."""

    def __init__(self):
        """Initializes game settings."""

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (128, 128, 128)
        self.bg_image = pygame.image.load('assets/images/stages/stage1.bmp')

        # Kevin's Settings
        self.fighter_speed = 13
        self.fighter_vel_y = 40
        self.fighter_gravity = 5
        self.fighter_jump = 40
        self.fighter_dash = 70

        self.fighter_atk = 0
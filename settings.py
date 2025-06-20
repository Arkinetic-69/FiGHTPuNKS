import pygame

"""Handles game settings.
Appropriate description will be added later."""

class Settings:
    """Class for settings of the game."""

    def __init__(self):
        """Initializes game settings."""
        pygame.display.init()
        pygame.display.set_mode((1200, 700))
        pygame.display.set_caption("FiGHTPuNKS")

        # Screen Settings
        self.screen_width = 1200
        self.screen_height = 700
        self.bg_color = (128, 128, 128)
        self.bg_image = pygame.image.load('assets/images/stages/stage1.bmp').convert_alpha()

        # Kevin's Settings
        self.fighter_speed = 15.0
        self.fighter_vel_y = 40.0
        self.fighter_gravity = 5.0
        self.fighter_jump = 40.0
        self.fighter_dash = 50.0

        self.fighter_atk = 0

        self.fighter_idle = [pygame.image.load('assets/images/fighters/kevin/idle/k_idle1.bmp').convert_alpha(), 
                             pygame.image.load('assets/images/fighters/kevin/idle/k_idle2.bmp').convert_alpha(),
                             pygame.image.load('assets/images/fighters/kevin/idle/k_idle3.bmp').convert_alpha(),
                             pygame.image.load('assets/images/fighters/kevin/idle/k_idle4.bmp').convert_alpha(),
                             pygame.image.load('assets/images/fighters/kevin/idle/k_idle5.bmp').convert_alpha()]
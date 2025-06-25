import pygame, os

"""Handles game settings.
Appropriate description will be added later."""

class Settings:
    """Class for settings of the game."""

    def __init__(self):
        """Initializes game settings."""
        # Screen Settings
        pygame.display.init()
        self.screen_width = 1200
        self.screen_height = 700
        pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("FiGHTPuNKS")

        self.bg_color = (128, 128, 128)
        self.bg_image = pygame.image.load('assets/images/stages/stage1.bmp').convert_alpha()

        # Kevin's Settings
        self.fighter_speed = 15.0
        self.fighter_vel_y = 40.0
        self.fighter_gravity = 5.0
        self.fighter_jump = 40.0
        self.fighter_dash = 50.0

        self.fighter_atk = 0

        # self.fighter_idle = [pygame.image.load('assets/images/fighters/kevin/idle/k_idle1.bmp').convert_alpha(), 
        #                      pygame.image.load('assets/images/fighters/kevin/idle/k_idle2.bmp').convert_alpha(),
        #                      pygame.image.load('assets/images/fighters/kevin/idle/k_idle3.bmp').convert_alpha(),
        #                      pygame.image.load('assets/images/fighters/kevin/idle/k_idle4.bmp').convert_alpha(),
        #                      pygame.image.load('assets/images/fighters/kevin/idle/k_idle5.bmp').convert_alpha()]
        
        # load fighter animations
        self.fighters = self.load_fighters()
        
    def load_fighters(self):
        path = os.path.join('assets', 'images', 'fighters')
        data = os.walk(path)
        fighter_animations = {}
        
        # Get fighter names
        for dirpath, dirname, filenames in data:
            fighters = dirname
            break
        
        # Load fighter animations
        for fighter in fighters:
            fighter_animations[fighter] = self.load_fighter_anim(fighter)
        
        return fighter_animations

    def load_fighter_anim(self, name):
        path = os.path.join('assets', 'images', 'fighters', name)
        animations = {}
        
        # Get fighter actions
        for _, dirname, _ in os.walk(path):
            actions = dirname
            break
        
        for action in actions:
            animations[action] = []
            for dirpath, dirname, filenames in os.walk(f"{path}/{action}"):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    frame = pygame.image.load(filepath).convert_alpha()
                    animations[action].append(frame)

        return animations
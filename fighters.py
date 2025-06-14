import pygame
from settings import Settings

class Kevin():
    """Initializes Kevin (Default Character)"""
    def __init__(self, x, y):

        """Initializes Kevin's behaviour"""
        self.settings = Settings() # Calls Settings

        # Load both Kevin and his rect
        self.rect = pygame.Rect((x, y, 125, 320))

        
          
        # Start with Kevin not moving
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.dash_right = False
        self.dash_left = False
        self.blocking = False
        self.attack_1 = False
        self.attack_2 = False

        # Dash variables
        self.last_press_time = 0
        self.double_press_window = 200 # milliseconds

        # Dash state
        self.is_dashing = False #Dash state indicator
        self.dash_start_time = 0 
        self.dash_duration = 100 

        # Updates player position
        self.x = float(self.rect.x)
        #self.y = float(self.rect.y)

    def update(self):
        """Updates Kevin based on movement flag"""
          # Movement
        if self.moving_right:
            self.rect.x += self.settings.fighter_speed
        if self.moving_left:
            self.rect.x -= self.settings.fighter_speed

        # Dashing
        if self.is_dashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.dash_start_time < self.dash_duration:
                # Apply dash movement
                if self.dash_right:
                    self.rect.x += self.settings.fighter_dash
                elif self.dash_left: 
                    self.rect.x -= self.settings.fighter_dash
            else:
                # Dash duration has ended, back to default
                self.is_dashing = False
                self.dash_right = False
                self.dash_left = False 

        # Jumping
        if self.jumping:
            self.rect.y -= self.settings.fighter_vel_y
            self.settings.fighter_vel_y -= self.settings.fighter_gravity

            if self.settings.fighter_vel_y < -self.settings.fighter_jump:
                self.jumping = False
                self.settings.fighter_vel_y = self.settings.fighter_jump
              
        # Sets Kevin's range
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
          
    def attack(self, surface):
        """Kevin's attacks"""
        # Kevin's attack hitboxes
        self.hitbox = pygame.Rect((self.rect.centerx, self.rect.y,
                                  2 * self.rect.width, self.rect.height))

        if self.attack_1:
            pygame.draw.rect(surface, (255, 0, 24), self.hitbox)
        
    def draw(self, surface):
        """Draws Kevin into the screen"""
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
        
        
        
          
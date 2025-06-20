import pygame
from settings import Settings

"""Will organize the Dummy class here.
Which is the Test Dummy that will be used for training purposes.
Includes attributes same as the fighters."""

class Dummy():
    """Initializes Dredmoore (Default Character)"""
    def __init__(self, x, y):
      """Initializes Dredmoore's behaviour"""
      self.settings = Settings() # Calls Settings

      # Load both Dredmoore and his rect
      self.rect = pygame.Rect((x, y, 125, 320))
          
      # Start with Dredmoore not moving
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
      """Updates Dredmoore based on movement flag"""
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
              
      # Sets Dredmoore's range
      if self.rect.left < 0:
        self.rect.left = 0
      if self.rect.right > self.settings.screen_width:
        self.rect.right = self.settings.screen_width
          
    def draw(self, surface):
        """Draws Dredmoore into the screen"""
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
          
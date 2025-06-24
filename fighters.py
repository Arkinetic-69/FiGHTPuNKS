import pygame
from settings import Settings
from pygame.sprite import Sprite

"""I will organize out-of-game attributes here.
This includes the fighter's attributes, such as speed, gravity, etc.
Subject to change."""

class Fighter(Sprite):
    """Initializes Kevin (Default Character)"""
    def __init__(self, x, y, fighter, is_player_1):
        """Initializes Kevin's behaviour"""

        super().__init__()
        self.settings = Settings() # Calls Settings
        self.is_player_1 = is_player_1
        self.screen = pygame.display.get_surface()

        # Load Kevin's sprite and attributes
        self.idle = self.settings.fighters[fighter]
        self.index_count = len(self.idle)
        self.current_index = 0
        self.anim_speed = .2

        # Load both Kevin and his rect
        self.image = self.idle[0]
        self.rect = pygame.Rect((x, y, 125, 320))

         # Kevin's attack hitboxes
        #self.attack_hitbox = pygame.Rect((self.rect.centerx, self.rect.y,
        #                          2 * self.rect.width, self.rect.height))
          
        # Start with Kevin not moving
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.dash_right = False
        self.dash_left = False
        self.blocking = False
        self.attack_1 = False
        self.attack_2 = False
        self.is_attacking_1 = False
        self.is_attacking_2 = False

        # Attack 1 hitbox properties
        self.attack_1_start_time = 0
        self.attack_1_duration = 200 # milliseconds

        self.attack_1_hitbox_width = 125 #customize to your own liking
        self.attack_1_hitbox_height = 320 #customize to your own liking
        self.attack_1_hitbox_offset_x_right = self.rect.x - 50 #customize to your own liking
        self.attack_1_hitbox_offset_x_left = -self.attack_1_hitbox_width + 5 #customize to your own liking
        self.attack_1_hitbox_offset_y = 0
        self.attack_1_hitbox_rect = pygame.Rect(0, 0, 0, 0)

        # Attack 2 hitbox properties
        self.attack_2_start_time = 0
        self.attack_2_duration = 400 # milliseconds

        self.attack_2_hitbox_width = 125 #customize to your own liking
        self.attack_2_hitbox_height = 320 #customize to your own liking
        self.attack_2_hitbox_offset_x_right = self.rect.x - 50 #customize to your own liking
        self.attack_2_hitbox_offset_x_left = -self.attack_2_hitbox_width + 5 #customize to your own liking
        self.attack_2_hitbox_offset_y = 0
        self.attack_2_hitbox_rect = pygame.Rect(0, 0, 0, 0)

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

        # attack states
        if self.is_attacking_1:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_1_start_time < self.attack_1_duration:
                hitbox_x = self.rect.x + self.attack_1_hitbox_offset_x_right
                
                hitbox_y = self.rect.y + self.attack_1_hitbox_offset_y
                self.attack_1_hitbox_rect.topleft = (hitbox_x, hitbox_y)
                self.attack_1_hitbox_rect.width = self.attack_1_hitbox_width
                self.attack_1_hitbox_rect.height = self.attack_1_hitbox_height
            else:
                # Attack 1 duration ended
                self.is_attacking_1 = False
                self.attack_1_hitbox_rect.size = (0, 0) # Hide hitbox

        # === Handle Attack 2 state and hitbox ===
        if self.is_attacking_2:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_2_start_time < self.attack_2_duration:
                hitbox_x = self.rect.x + self.attack_2_hitbox_offset_x_right
                
                hitbox_y = self.rect.y + self.attack_2_hitbox_offset_y
                self.attack_2_hitbox_rect.topleft = (hitbox_x, hitbox_y)
                self.attack_2_hitbox_rect.width = self.attack_2_hitbox_width
                self.attack_2_hitbox_rect.height = self.attack_2_hitbox_height
            else:
                # Attack 2 duration ended
                self.is_attacking_2 = False
                self.attack_2_hitbox_rect.size = (0, 0) # Hide hitbox
              
        # Sets Kevin's range
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > self.settings.screen_width:
            self.rect.right = self.settings.screen_width
            
        self.current_index += self.anim_speed
        self.image = self.idle[int(self.current_index) % self.index_count]
        if not self.is_player_1:
            self.image = pygame.transform.flip(self.image, True, False)
        

        # Sprite function
        # if self.current_index < self.max_index:
        #     self.current_index += 1
        # else:
        #     self.current_index = 0
   
          
    #def attack(self, surface):
    #   """Kevin's attacks"""
    #    pygame.draw.rect(surface, (255, 201, 24), self.attack_hitbox)
        
    def draw(self, surface):
        """Draws Kevin into the screen"""
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

        # Draw Attack 1 hitbox (for debugging)
        if self.is_attacking_1 and self.attack_1_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (255, 0, 0), self.attack_1_hitbox_rect, 2) # Red outline

        # Draw Attack 2 hitbox (for debugging)
        if self.is_attacking_2 and self.attack_2_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (0, 255, 0), self.attack_2_hitbox_rect, 2) # Green outline for attack 2

        # draw the frame
        self.screen.blit(self.image, self.rect)
        
    def animate(self):
        """ sprite animation """
        pass

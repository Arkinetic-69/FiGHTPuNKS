import pygame, random
from settings import Settings


"""I will organize out-of-game attributes here.
This includes the fighter's attributes, such as speed, gravity, etc.
Subject to change."""

class Fighter(pygame.sprite.Sprite):
    """Initializes Kevin (Default Character)"""
    def __init__(self, game_instance, x, y, fighter, is_player_1, select = -1, is_inverted = False):
        """Initializes Kevin's behaviour"""
        super().__init__()
        self.game = game_instance
        self.settings = self.game.settings # Calls Settings
        self.screen = pygame.display.get_surface()
        self.name = fighter
        self.inverted = is_inverted
        self.hp = 100
        
        # For menu purposes
        self.selector = select

        # Load Kevin's sprite and attributes
        self.action = 'idle'
        self.current_anim_index = 0
        self.is_player_1 = is_player_1
        self.anim = self.settings.fighters[fighter]['idle']
        self.index_count = len(self.anim)
        self.anim_speed = .2

        # Load both Kevin and his rect
        self.image = self.anim[0]
        self.rect = self.image.get_frect(midbottom = (x, y))

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
        action = 'idle'
        
        if self.moving_right:
            action = 'walkr'
            self.rect.x += self.settings.fighter_speed
        if self.moving_left:
            action = 'walkl'
            self.rect.x -= self.settings.fighter_speed

        # Jumping
        if self.jumping:
            action = 'jump'
            self.rect.y -= self.settings.fighter_vel_y
            self.settings.fighter_vel_y -= self.settings.fighter_gravity

            if self.settings.fighter_vel_y < -self.settings.fighter_jump:
                self.jumping = False
                self.settings.fighter_vel_y = self.settings.fighter_jump

        # Dashing
        if self.is_dashing:
            action = 'dash'
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

        # attack states
        if self.is_attacking_1:
            action = 'attack1'
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
            action = 'attack2'
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
        
        # falling
        if self.rect.bottom < 650:
            self.rect.y -= -5
        if self.rect.bottom > 650:
            self.rect.bottom = 650
        
        self.animate(action)
        # self.hp -= random.uniform(0,1)


    def menu_update(self, mouse_pos, animation_speed_scale, selected):
        """Update method used when using it in the character select"""
        # Animates the idle animation
        self.animate('idle', animation_speed_scale)
        
        image = self.image
        
        # Detects if the cursor is hovering on it
        if self.rect.collidepoint(mouse_pos) or selected == self.name:
            image = pygame.transform.rotozoom(self.image, 0, 1.2)
            
        self.screen.blit(image, self.rect)

    def on_click(self, mouse_pos):
        """For when the fighter is clicked on the menu"""
        if self.rect.collidepoint(mouse_pos):
            return self.name
        
    def draw(self, surface):
        """Draws Kevin into the screen"""
        # pygame.draw.rect(surface, (255, 0, 0), self.rect)

        # Draw Attack 1 hitbox (for debugging)
        if self.is_attacking_1 and self.attack_1_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (255, 0, 0), self.attack_1_hitbox_rect, 2) # Red outline

        # Draw Attack 2 hitbox (for debugging)
        if self.is_attacking_2 and self.attack_2_hitbox_rect.width > 0:
            pygame.draw.rect(surface, (0, 255, 0), self.attack_2_hitbox_rect, 2) # Green outline for attack 2

        # draw the frame
        if self.inverted:
            self.image = pygame.transform.invert(self.image)
        self.screen.blit(self.image, self.rect)
        
    def animate(self, action, animation_speed_scale = 1):
        """ sprite animation """
        # Continue animation if action is still the same
        if action == self.action:
            self.current_anim_index += self.anim_speed * animation_speed_scale
            self.image = self.anim[int(self.current_anim_index) % self.index_count]
            if not self.is_player_1:
                self.image = pygame.transform.flip(self.image, True, False)
        # Reset animation value and replace action
        else:
            self.action = action
            self.anim = self.settings.fighters[self.name][action]
            self.current_anim_index = 0
            self.index_count = len(self.settings.fighters[self.name][action])
            self.image = self.anim[int(self.current_anim_index) % self.index_count]
            if not self.is_player_1:
                self.image = pygame.transform.flip(self.image, True, False)
        self.current_index += self.anim_speed * animation_speed_scale
        self.image = self.idle[int(self.current_index) % self.index_count]
        if not self.is_player_1:
            self.image = pygame.transform.flip(self.image, True, False)
    
    def attack_1_method(self):
        """Handle attack 1 logic."""
        # Play attack sound effect
        self.game.sounds.play_sound_effect('atk 1')
        # ...existing attack code...
    
    def attack_2_method(self):
        """Handle attack 2 logic."""
        # Play attack sound effect
        self.game.sounds.play_sound_effect('atk 2')
        # ...existing attack code...
    
    def jump_method(self):
        """Handle jump logic."""
        # Play jump sound effect
        self.game.sounds.play_sound_effect('jump')
        # ...existing jump code...
    
    def take_damage(self):
        """Handle taking damage."""
        # Play hit sound effect
        self.game.sounds.play_sound_effect('hit')
        # ...existing damage code...


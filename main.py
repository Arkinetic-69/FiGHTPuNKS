import sys
import pygame

from settings import Settings
from fighters import Kevin
from dummy import Dummy

"""Main file to run the FiGHTPuNKS game."""

class FiGHTPuNKS:
    """Class to manage game assets and behaviour."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings() # Calls settings.py

        self.fighter = Kevin(150, 210) # Calls Kevin in fighter.py
        self.dummy = Dummy(890, 210) # Calls Test Dummy

        # Set up the display
        self.screen = pygame.display.get_surface()

        # set the background color of the screen
        self.bg_color = (self.settings.bg_color)

        # Initializes joystick support
        #pygame.joystick.init() 
        #self.joystick = []

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self.check_events()
            self.fighter.update()
            self.dummy.update()
            self.update_screen()
            self.clock.tick(60)

    def check_events(self):
        """Responds to keyboard, mouse, and joystick events"""
        for event in pygame.event.get():
            # Closes the game when you press X
            if event.type == pygame.QUIT:
                sys.exit()
                
            #Joystick events
            #elif event.type == pygame.JOYDEVICEADDED:
                #self.joy = pygame.joystick.Joystick(event.device_index)
                #self.joystick.append(self.joy)

            # Keyboard events
            elif event.type == pygame.KEYDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self.check_keyup_events(event)

            # Joystick events
            elif event.type == pygame.JOYBUTTONDOWN:
                self.check_keydown_events(event)
            elif event.type == pygame.JOYBUTTONUP:
                self.check_keyup_events(event)
            
    def check_keydown_events(self, event):
        """Responds to keys being pressed"""
        # Player 1 Movement
        if event.key == pygame.K_d:
            self.fighter.moving_right = True
            # Dash controls
            current_time = pygame.time.get_ticks()
            if current_time - self.fighter.last_press_time <= self.fighter.double_press_window:
                if not self.fighter.is_dashing:
                    self.fighter.dash_right = True
                    self.fighter.is_dashing = True
                    self.fighter.dash_start_time = current_time
                self.fighter.last_press_time = 0
                
            self.fighter.last_press_time = current_time

        elif event.key == pygame.K_a:
            self.fighter.moving_left = True
            # Dash controls
            current_time = pygame.time.get_ticks()
            if current_time - self.fighter.last_press_time <= self.fighter.double_press_window:
                if not self.fighter.is_dashing:
                    self.fighter.dash_left = True
                    self.fighter.is_dashing = True
                    self.fighter.dash_start_time = current_time
                self.fighter.last_press_time = 0
                    
            self.fighter.last_press_time = current_time

        elif event.key == pygame.K_w: # Jump control
            self.fighter.jumping = True

        # Player 1 attack
        elif event.key == pygame.K_x:
            if not self.fighter.is_attacking_1:
                self.fighter.attack_1 = True
                self.fighter.is_attacking_1 = True
                self.fighter.attack_1_start_time = pygame.time.get_ticks()

        elif event.key == pygame.K_c:
            if not self.fighter.is_attacking_2:
                self.fighter.attack_2 = True
                self.fighter.is_attacking_2 = True
                self.fighter.attack_2_start_time = pygame.time.get_ticks()
                

        # Player 2 Movement
        elif event.key == pygame.K_l:
            self.dummy.moving_right = True
        elif event.key == pygame.K_j:
            self.dummy.moving_left = True
        elif event.key == pygame.K_i: # Jump control
            self.dummy.jumping = True

        # Player 2 Dash
        elif event.key == pygame.K_l:
            self.dummy.moving_right = True
            # Dash controls
            current_time = pygame.time.get_ticks()
            if current_time - self.dummy.last_press_time <= self.dummy.double_press_window:
                if not self.dummy.is_dashing:
                    self.dummy.dash_right = True
                    self.dummy.is_dashing = True
                    self.dummy.dash_start_time = current_time
                self.dummy.last_press_time = 0
                
            self.dummy.last_press_time = current_time

        elif event.key == pygame.K_j:
            self.dummy.moving_left = True
            # Dash controls
            current_time = pygame.time.get_ticks()
            if current_time - self.dummy.last_press_time <= self.dummy.double_press_window:
                if not self.dummy.is_dashing:
                    self.dummy.dash_left = True
                    self.dummy.is_dashing = True
                    self.dummy.dash_start_time = current_time
                self.dummy.last_press_time = 0
                    
            self.dummy.last_press_time = current_time
        
        # Escape to close
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
    
    def check_keyup_events(self,event):
        """Responds to keys being released"""
        # Player 1 movement
        if event.key == pygame.K_d:
            self.fighter.moving_right = False
        elif event.key == pygame.K_a:
            self.fighter.moving_left = False
        # Player 1 attack
        elif event.key == pygame.K_x:
            self.fighter.attack_1 = False
        elif event.key == pygame.K_c:
            self.fighter.attack_2 = False

        # Player 2 movement
        elif event.key == pygame.K_l:
            self.dummy.moving_right = False
        elif event.key == pygame.K_j:
            self.dummy.moving_left = False

    def update_screen(self):
        """Updates images on the screen and flip to new screen"""
        # Sets the background to default stage.
        self.screen.blit(self.settings.bg_image, (0,0))
        self.settings.bg_image = pygame.transform.scale(self.settings.bg_image,
                                                        (self.settings.screen_width, 
                                                         self.settings.screen_height))
        # Draws the fighter on the screen
        self.fighter.draw(self.screen)
        self.dummy.draw(self.screen)

        self.screen.blit(self.fighter.idle[self.fighter.current_index], (150, 210))
        
        pygame.display.flip()

if __name__ == '__main__':
    # Make game instance and run the game
    fp = FiGHTPuNKS()
    fp.run_game()

# test msg
#lalalalala
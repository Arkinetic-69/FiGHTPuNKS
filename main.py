import pygame, sys, random

from settings import Settings
from fighters import Fighter
from sounds import Sounds
from menu import Menus
from debug import PgDebug

"""Main file to run the FiGHTPuNKS game."""

class FiGHTPuNKS:
    """Class to manage game assets and behaviour."""

    def __init__(self):
        """Initializes the game and creates game resources."""
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings() # Calls settings.py
        self.timer_font = pygame.Font('assets/fonts/NIRVANA.TTF', 100)
        
        # For debugging
        self.debug = PgDebug()
        self.debug.debugging = True

        # Set up the display
        self.screen = pygame.display.get_surface()

        # Initialize sound
        self.sound = Sounds() 
        
        # Set the background color of the screen
        self.bg_color = self.settings.bg_color
        
        # Start Menu
        self.menus = Menus(self)
        self.menus.start_menu()

        # Initializes joystick support
        #pygame.joystick.init() 
        #self.joystick = []

    def load_fighters(self, name1, name2, invert):
        self.fighter = Fighter(self, (self.screen.width / 5) * 1, 650,
                               name1, True, ) # Calls Kevin in fighter.py
        self.dummy = Fighter(self, (self.screen.width / 5) * 4, 650,
                             name2, False, is_inverted=invert) # Calls Test Dummy
        
    def show_hp(self, fighter, pos, is_player_1):
        surf = pygame.Surface((fighter.hp * 5 or 1, 50))
        if is_player_1:
            surf_rect = surf.get_frect(topleft = pos)
        else:
            surf_rect = surf.get_frect(topright = pos)
            
        surf.fill('red')
        self.screen.blit(surf, surf_rect)
        
    def timer(self, pos):
        current_time = pygame.time.get_ticks()
        timer = (self.time - (current_time - self.start_time)) / 1000
        timer = int(timer)
        surf = self.timer_font.render(str(timer), True, 'silver')
        rect = surf.get_frect(center = pos)
        
        self.screen.blit(surf, rect)

        if timer <= 0:
            self.running = False
        
    def run_game(self):
        """Start the main loop for the game"""
        self.stage = self.settings.stages[random.randint(1, len(self.settings.stages) - 1)]
        self.running = True
        self.start_time = pygame.time.get_ticks()
        self.time = 60000
        self.death_time = 500
        self.sound.play_stage_music(random.choice(list(self.sound.stage_music.keys())))
        # self.sound.play_combat_sound()
        
        while self.running:
            self.check_events()
            self.fighter.update()
            self.dummy.update()
            self.update_screen()
            self.clock.tick(60)

        pygame.mixer.music.stop()
        self.sound.play_menu_music()


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
            self.sound.play_combat_sound('jump')

        # Player 1 attack
        elif event.key == pygame.K_x:
            if not self.fighter.is_attacking_1:
                self.fighter.attack_1 = True
                self.fighter.is_attacking_1 = True
                self.fighter.attack_1_start_time = pygame.time.get_ticks()
                self.sound.play_combat_sound('atk 1')

        elif event.key == pygame.K_c:
            if not self.fighter.is_attacking_2:
                self.fighter.attack_2 = True
                self.fighter.is_attacking_2 = True
                self.fighter.attack_2_start_time = pygame.time.get_ticks()
                self.sound.play_combat_sound('atk 2')
                
        elif event.key == pygame.K_m:
            if not self.dummy.is_attacking_1:
                self.dummy.attack_1 = True
                self.dummy.is_attacking_1 = True
                self.dummy.attack_1_start_time = pygame.time.get_ticks()

        elif event.key == pygame.K_n:
            if not self.dummy.is_attacking_2:
                self.dummy.attack_2 = True
                self.dummy.is_attacking_2 = True
                self.dummy.attack_2_start_time = pygame.time.get_ticks()
                
        # Player 2 Movement
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
            
        elif event.key == pygame.K_i: # Jump control
            self.dummy.jumping = True
            
        elif event.key == pygame.K_m:
            if not self.dummy.is_attacking_1:
                self.dummy.attack_1 = True
                self.dummy.is_attacking_1 = True
                self.dummy.attack_1_start_time = pygame.time.get_ticks()

        elif event.key == pygame.K_n:
            if not self.dummy.is_attacking_2:
                self.dummy.attack_2 = True
                self.dummy.is_attacking_2 = True
                self.dummy.attack_2_start_time = pygame.time.get_ticks()
        # Escape to close
        elif event.key == pygame.K_ESCAPE:
            self.menus.pause_menu()
    
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
        elif event.key == pygame.K_m:
            self.dummy.attack_1 = False
        elif event.key == pygame.K_n:
            self.dummy.attack_2 = False

    def update_screen(self):
        """Updates images on the screen and flip to new screen"""
        # Sets the background to default stage.
        self.screen.blit(self.stage, (0,0))
        self.settings.bg_image = pygame.transform.scale(self.settings.bg_image,
                                                        (self.settings.screen_width, 
                                                         self.settings.screen_height))
        # Draws the fighter on the screen
        self.fighter.draw(self.screen)
        self.dummy.draw(self.screen)
        
        self.show_hp(self.fighter, (50,50), True)
        self.show_hp(self.dummy, (self.screen.width - 50,50), False)
        
        self.timer((self.screen.width/2, 75))
        
        if self.dummy.death > 0:
            current_time = pygame.time.get_ticks()
            if current_time - self.dummy.death >= self.death_time:
                self.running = False

        # self.screen.blit(self.fighter.idle[self.fighter.current_index], self.fighter.rect)
        
        pygame.display.flip()

if __name__ == '__main__':
    # Make game instance and run the game
    fp = FiGHTPuNKS()
    fp.run_game()

# test msg
#lalalalalaa
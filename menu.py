import pygame, sys
from button import Button
from fighters import Fighter

"""Handles displaying the ui.
This module contains the Menu class, which is responsible for displaying
the main menu, options, and other UI elements in the game."""

class Menus:
    """Class to handle the game menu and UI."""
    
    def __init__(self, game_instance):
        # pygame.init()
        # pygame.display.set_mode((1200, 700))
        self.game = game_instance
        self.screen = pygame.display.get_surface()
        self.screen_rect = self.screen.get_frect()
        self.font = pygame.Font('assets/fonts/NIRVANA.TTF', 60)
        self.clock = pygame.Clock()
        
        self.logo = pygame.image.load('assets/images/menu/logo.png').convert_alpha()
        

    def start_menu(self):
        """Display and handle the start menu."""
        # Start playing menu music when entering the menu
        self.game.sounds.play_menu_music()
        
        # Buttons
        START = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 25), 'START', self.font, 'black', 'red')
        SETTINGS = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 100), 'SETTINGS', self.font, 'black', 'red')
        CREDITS = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 175), 'CREDITS', self.font, 'black', 'red')
        QUIT = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 250), 'QUIT', self.font, 'black', 'red')
        
        bg_image = pygame.image.load('assets/images/menu/start_menu.2.png').convert()
        bg_image = pygame.transform.scale(bg_image, (self.screen.width, self.screen.height))
        logo = pygame.transform.rotozoom(self.logo, 0, .8)
        logo_rect = logo.get_frect(center = (self.screen_rect.centerx, self.screen_rect.centery - 175))
        running = True
        
        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if START.is_clicked():
                        self.character_select_menu()
                    elif SETTINGS.is_clicked():
                        self.settings_menu()
                    elif CREDITS.is_clicked():
                        self.credits_menu()
                    elif QUIT.is_clicked():
                        sys.exit()
            
            self.screen.blit(bg_image, (0,0))
            self.screen.blit(logo, logo_rect)
            for button in [START, SETTINGS, CREDITS, QUIT]:
                button.update(self.screen)
            
            pygame.display.flip()
    
    def settings_menu(self):
        pass
    
    def credits_menu(self):
        # Buttons
        EXIT = Button(None, (self.screen_rect.centerx, self.screen_rect.centery), 'EXIT', self.font, 'black', 'red')
        
        bg_image = pygame.image.load('assets/images/menu/start_menu.png').convert()
        bg_image = pygame.transform.scale(bg_image, (self.screen.width, self.screen.height))
        running = True

        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if EXIT.is_clicked():
                        self.start_menu()
            
            self.screen.blit(bg_image, (0,0))
            for button in [EXIT]:
                button.update(self.screen)
            
            pygame.display.flip()
    
    def character_select_menu(self):
        self._load_fighters()
        
        # Buttons
        PLAY = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 300), 'PLAY', self.font, 'white', 'red')
        
        # Background Image
        bg_image = pygame.image.load('assets/images/menu/character_select_no_char.png').convert()
        bg_image = pygame.transform.scale(bg_image, (self.screen.width, self.screen.height))
        selected1 = selected2 = ''
        running = True
        
        while running:
            # For debugging
            print(selected1, selected2)
            self.game.debug.debug(str(pygame.mouse.get_pos()))
            
            mouse_pos = pygame.mouse.get_pos()
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Determine which fighter is selected
                    for fighter in [self.fighter1, self.fighter2, self.fighter3]:
                        clicked = fighter.on_click(mouse_pos)
                        selected1 =  clicked if clicked else selected1
                    for fighter in [self.fighter4, self.fighter5, self.fighter6]:
                        clicked = fighter.on_click(mouse_pos)
                        selected2 =  clicked if clicked else selected2
                    
                    if PLAY.is_clicked():
                        try:
                            duplicate = selected1 == selected2
                            self.game.load_fighters(selected1, selected2, duplicate)
                            self.game.run_game()
                        except:
                            pass
              
            self.screen.blit(bg_image, (0,0))

            # update and draw buttons
            for button in [PLAY]:
                button.update(self.screen)
            
            # animate and draw fighters
            for fighter in [self.fighter1, self.fighter2, self.fighter3]:
                fighter.menu_update(mouse_pos, 0.5, selected1)
            for fighter in [self.fighter4, self.fighter5, self.fighter6]:
                fighter.menu_update(mouse_pos, 0.5, selected2)

            pygame.display.flip()
    
    def _load_fighters(self):
        """Loads the fighters for character select"""
        self.fighter1 = Fighter(self.game, 130, 400, 'Xiuhcoatl', True, 1)
        self.fighter2 = Fighter(self.game, 271, 465, 'Dredmoore', True, 2)
        self.fighter3 = Fighter(self.game, 404, 530, 'kevin', True, 3)
        
        self.fighter4 = Fighter(self.game, 794, 530, 'kevin', False, 3)
        self.fighter5 = Fighter(self.game, 931, 465, 'Dredmoore', False, 2)
        self.fighter6 = Fighter(self.game, 1078, 400, 'Xiuhcoatl', False, 1)

    def pause_menu(self):
        CONTINUE = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 100), 'CONTINUE', self.font, 'white', 'red')
        SETTINGS = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 175), 'SETTINGS', self.font, 'white', 'red')
        QUIT = Button(None, (self.screen_rect.centerx, self.screen_rect.centery + 250), 'EXIT', self.font, 'white', 'red')
        
        bg_image = pygame.image.load('assets/images/menu/Matrix_Main_bg.png').convert()
        bg_image = pygame.transform.scale(bg_image, (self.screen.width, self.screen.height))
        logo = pygame.transform.rotozoom(self.logo, 0, 1)
        logo_rect = logo.get_frect(center = (self.screen_rect.centerx, self.screen_rect.centery - 150))
        
        running = True

        while running:
            self.clock.tick(60)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if CONTINUE.is_clicked():
                        running = False
                    elif SETTINGS.is_clicked():
                        self.settings_menu()
                    elif QUIT:
                        sys.exit()
            
            self.screen.blit(bg_image, (0,0))
            self.screen.blit(logo, logo_rect)
            for button in [CONTINUE, SETTINGS, QUIT]:
                button.update(self.screen)
            
            pygame.display.flip()
    
    def post_game_menu(self):
        pass

# menu = Menus()
# menu.start_menu()
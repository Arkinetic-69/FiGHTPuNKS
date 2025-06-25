import pygame

class PgDebug:
    def __init__(self):
        pygame.init()
        self.debugging = False
        self.display = pygame.display.get_surface()
        self.font = pygame.font.Font(None, 30)
        
    def debug(self, info, y = 10, x = 10):
        if self.debugging:
            debug_surf = self.font.render(info, True, 'white', 'black')
            debug_rect = debug_surf.get_frect(topleft = (x, y))
            self.display.blit(debug_surf, debug_rect)
        
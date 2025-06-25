import pygame

class Button:
    def __init__(self, image, pos, text_input, font, base_color, hovering_color):
        self.image = image
        self.font = font
        self.base_color, self.hovering_color = base_color, hovering_color

        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)

        if self.image is None:
            self.image = self.text

        self.rect = self.image.get_frect(center=(pos))
        self.text_rect = self.text.get_frect(center=(pos))

    def update(self, screen):
        self.change_color()
        self.draw(screen)
        
    def draw(self, screen):
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    # for detecting mouse presses
    def is_clicked(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            return True
        return False

    def change_color(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

        
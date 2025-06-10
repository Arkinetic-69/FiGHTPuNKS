import pygame

class Actor(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        super().__init__()
        self.image = image
        self.pos = pygame.Vector2(pos)
        self.rect = self.image.get_rect(center=self.pos)

    def update(self, events, dt):
        pass

# just for the cheap motion effect....
class Shadow(Actor):
    def __init__(self, image, pos):
        # new surface to allow surface level alpha value
        # with per-pixel alpha surface
        tmp = pygame.Surface(image.get_rect().size)
        tmp.set_colorkey((1,2,3))
        tmp.fill((1,2,3))
        tmp.blit(image, (0,0))
        super().__init__(tmp, pos)
        self.time = 0
        self.alpha = 255
        self.image.set_alpha(self.alpha)

    def update(self, events, dt):
        self.time += dt
        if self.time > 50:
            self.time = 0
            self.alpha -= 50
            if self.alpha < 50:
                self.kill()
            else:
                self.image.set_alpha(self.alpha)

class Player(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)

        # since we want to know if there's a double key press
        # we need to keep track of the last button pressed
        self.last_move_button = None

        # a flag that indicates that we're running
        self.running = False

        self.run_counter = 0

    def update(self, events, dt):

        # this is the part that checks for the double key press
        for e in events:
            if e.type == pygame.KEYDOWN:
                ticks = pygame.time.get_ticks()

                #we check if we pressed the same key in the last 500ms before
                self.running = self.last_move_button and self.last_move_button[0] == e.key and ticks - self.last_move_button[1] < 500

                # keep track of the last button pressed and the time of the key press
                self.last_move_button = (e.key, ticks)

        # this is the "regular" movement code
        pressed = pygame.key.get_pressed()
        move = pygame.Vector2((0, 0))
        if pressed[pygame.K_w]: move += (0, -1)
        if pressed[pygame.K_a]: move += (-1, 0)
        if pressed[pygame.K_s]: move += (0, 1)
        if pressed[pygame.K_d]: move += (1, 0)
        if move.length() > 0: 
            move.normalize_ip()
        else:
            # if we're not moving we're not running
            self.running = False

        # if the running flag is set, we move at double speed
        speed = 2 if self.running else 1

        self.pos += move * (dt/5) * speed
        self.rect.center = self.pos

        # just for the cheap motion effect....
        self.run_counter = (self.run_counter + dt) if self.running else 0
        if self.running and self.run_counter > 25:
            self.run_counter = 0
            self.groups()[0].add(Shadow(self.image, self.rect.center))


def main():
    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()
    dt = 0

    sprites = pygame.sprite.Group(Player(pygame.image.load('assets/images/fighters/luffy.bmp'), (100, 200)))

    while True:
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                return

        sprites.update(events, dt)
        screen.fill((30, 30, 30))
        sprites.draw(screen)

        pygame.display.update()
        dt = clock.tick(60)

if __name__ == '__main__':
    main()
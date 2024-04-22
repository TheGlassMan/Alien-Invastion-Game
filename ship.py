import pygame
class Ship:

    def __init__(self):
        #Init Ship POS

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen_get_rect()

        #Load ship imag
        self.image = pygame.image.load('/Users/ernestomartinez/Documents/GitHub/Alien-Invastion-Game/ship.png')
        self.rect = self.image.get_rect()

        #Start each new ship at bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship pos
        self.x = float(self.rect.x)

        #Movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.moving_right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        #Draw ship in POS
        self.screen.blit(self.image, self.rect)
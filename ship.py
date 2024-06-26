import pygame
#from settings import Settings
class Ship:

    def __init__(self, ai_game):
        #Init Ship POS

        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        #Load ship imag
        original_image = pygame.image.load('ship.png')
        self.image = pygame.transform.scale(original_image, (100, 100))
        self.rect = self.image.get_rect()

        #Start each new ship at bottom center
        self.rect.midbottom = self.screen_rect.midbottom

        #Store a decimal value for the ship pos
        self.x = float(self.rect.x)

        #Movement
        self.moving_right = False
        self.moving_left = False

    def update(self):
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def blitme(self):
        #Draw ship in POS
        self.screen.blit(self.image, self.rect)
    
    def center_ship(self):
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
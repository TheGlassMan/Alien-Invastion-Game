import pygame
class Settings:
    #All settings stored in here

    def __init__(self):
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg = None

        #Ship Settings
        self.ship_speed = 7.0
        self.ship_limit = 3

        #Bullet settings
        self.bullet_speed = 15.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 20
        self.fleet_drop_speed = 30
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
        #Framerate 
        self.clock = pygame.time.Clock()
        self.fps = 60
    def load_background(self):
        self.bg = pygame.image.load('/Users/ernestomartinez/Documents/GitHub/Alien-Invastion-Game/space.jpeg).convert()')

    def get_background_width(self):
        return self.bg.get_width()
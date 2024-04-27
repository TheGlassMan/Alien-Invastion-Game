class Settings:
    #All settings stored in here

    def __init__(self):
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10,230,230)

        #Ship Settings
        self.ship_speed = 2.5

        #Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # alien settings
        self.alien_speed = 7.5
        self.fleet_drop_speed = 10
        # fleet direction of 1 represents right; -1 represents left.
        self.fleet_direction = 1
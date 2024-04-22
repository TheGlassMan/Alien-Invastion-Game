class Settings:
    #All settings stored in here

    def __init__(self):
        #Screen Settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (10,230,230)

        #Ship Settings
        self.ship_speed = 1.5

        #Bullet settings
        self.bullet_speed = 1.0
        self.bullet__width = 3
        self.bullet_height = 15
        self.bullet__color = (60,60,60)
        self.bullets_allowed = 3
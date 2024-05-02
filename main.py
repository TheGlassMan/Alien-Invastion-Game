import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep


class AlienInvasion:
    def __init__(self):
        # init the game and game resources

        pygame.init()
        self.settings = Settings()
        # Screen Settings
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        

        pygame.display.set_caption("Ernesto's Alien Invasion")

       # self.bg_color = (50,230,230)
        self.stats = GameStats(self)
        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.current_level = 1
        self.upgrades_available = ['Extra life', 'Faster Ship', 'Thicker bullets']
        self.upgrade_menu_active = False
    
    def run_game(self):
        while True:
            self._check_events()
            self.clock.tick(self.settings.fps) 
            if self.stats.game_active:    
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
            self._update_screen()
    def _check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                     self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                     self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
             sys.exit()
        elif event.key == pygame.K_SPACE:
             self._fire_bullet()
        elif event.key == pygame.K_f:
                    self._toggle_fullscreen()
        elif event.key == pygame.K_u:
            if self.current_level % 5 == 0 and not self.upgrade_menu_active:
                self.upgrade_menu_active = True
    
    def _toggle_fullscreen(self):
        self.settings.fullscreen = not self.settings.fullscreen
        if self.settings.fullscreen:
            self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        else:
            self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
            self.settings.screen_width = self.screen.get_rect().width
            self.settings.screen_height = self.screen.get_rect().height
        if self.settings.fullscreen:
            self.ship.rect.bottom = self.settings.screen_height - 10  # Adjust ship position
        else:
            self.ship.rect.bottom = self.settings.screen_height - 80

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
                self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
                self.ship.moving_left = False


    def _fire_bullet(self):
         if len(self.bullets) < self.settings.bullets_allowed:
              new_bullet = Bullet(self)
              self.bullets.add(new_bullet)
    
    def _update_bullets(self):
        self.bullets.update()
        
        for bullet in self.bullets.copy():
         if bullet.rect.bottom <= 0:
              self.bullets.remove(bullet)
        self._check_bullet_collision_area()

    def _check_bullet_collision_area(self):
        collisions = pygame.sprite.groupcollide(self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.aliens_killed += len(aliens)
        if not self.aliens:
            self.bullets.empty()
            self.current_level += 1
            self.settings.alien_speed += 2
            if self.current_level % 5 == 0:
                self._pause_game()
                self._prompt_upgrade()
                self._resume_game()
            self._create_fleet()

    def _update_aliens(self):
         self._check_fleet_edges()
         self.aliens.update()
         self._check_aliens_bottom()
    
    def _create_fleet(self):
         #Make a single alien
         aliens = Alien(self)
         alien_width, alien_height = aliens.rect.size
         #Determine how much space you have on the screen for aliens
         available_space_x = self.settings.screen_width - (2*alien_width)
         number_aliens_x = available_space_x // (2 * alien_width)
        
        #Determine the number of rows of aliens that fit on the screen
         ship_height = self.ship.rect.height
         available_space_y = (self.settings.screen_height - (3 * alien_height) - ship_height)
         number_rows = available_space_y // (2 * alien_height)
        #Create the full fleet of aliens
         for row_number in range (number_rows):
              for alien_number in range(number_aliens_x):
                   self._create_alien(alien_number, row_number)
    
    def _create_alien(self, alien_number, row_number):
         aliens = Alien(self)
         alien_width, alien_height = aliens.rect.size
         alien_width = aliens.rect.width
         aliens.x = alien_width + 2 * alien_width * alien_number
         aliens.rect.x = aliens.x
         aliens.rect.y = alien_height + 2 * aliens.rect.height * row_number
         self.aliens.add(aliens)

    def _check_fleet_edges(self):
         for alien in self.aliens.sprites():
              if alien.check_edges():
                   self._change_fleet_direction()
                   break
              
    def _change_fleet_direction(self):
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        if self.stats.ships_left > 0:
              self.stats.ships_left -= 1
              self.aliens.empty()
              self.bullets.empty()
              self._create_fleet()
              self.ship.center_ship()
              sleep(0.5)
        else:
             self.stats.game_active = False
        
    def _check_aliens_bottom(self):
         screen_rect = self.screen.get_rect()
         for alien in self.aliens.sprites():
              if alien.rect.bottom >= screen_rect.bottom:
                   self._ship_hit()
                   break
             

    def _update_screen(self):
        bg = pygame.image.load('space.png')
        # Scale background to fit the screen size
        bg = pygame.transform.scale(bg, (self.settings.screen_width, self.settings.screen_height))
        # Draw background
        self.screen.blit(bg, (0, 0))
        #Draw lives counter
        self._draw_lives_counter()
        #Draw alien counter
        self._draw_alien_counter()
        #Draw levels counter
        self._draw_levels_counter()
        self.ship.blitme()
        for bullet in self.bullets.sprites():
             bullet.draw_bullet()
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self._draw_game_over()
        pygame.display.flip()
        ############################
    
    def _draw_game_over(self):
        font = pygame.font.SysFont(None, 48)
        game_over_text = font.render("Game Over", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect()
        game_over_rect.center = self.screen.get_rect().center
        self.screen.blit(game_over_text, game_over_rect)

    def _draw_lives_counter(self):
        font = pygame.font.SysFont(None, 24)
        lives_text = font.render(f"Lives: {self.stats.ships_left}", True, (255, 255, 255))
        lives_rect = lives_text.get_rect()
        lives_rect.topleft = (10, 10)
        self.screen.blit(lives_text, lives_rect)
    
    def _draw_alien_counter(self):
        font = pygame.font.SysFont(None, 24)
        alien_kill_text = font.render(f"Aliens Killed: {self.stats.aliens_killed}", True, (255, 255, 255))
        alien_kill_rect = alien_kill_text.get_rect()
        alien_kill_rect.topright = (self.settings.screen_width - 10, 10)
        self.screen.blit(alien_kill_text, alien_kill_rect)
    
    def _draw_levels_counter(self):
        font = pygame.font.SysFont(None, 24)
        levels_text = font.render(f"Level: {self.current_level}", True, (255, 255, 255))
        levels_rect = levels_text.get_rect()
        levels_rect.centerx = self.settings.screen_width // 2
        levels_rect.top = 10
        self.screen.blit(levels_text, levels_rect)
    
    def _display_upgrade_menu(self):
        """Display the upgrade menu on the screen."""
        upgrade_font = pygame.font.Font(None, 36)
        upgrade_text = upgrade_font.render("Upgrade Menu", True, (255, 255, 255))
        upgrade_rect = upgrade_text.get_rect(center=(self.settings.screen_width // 2, self.settings.screen_height // 2))
        self.screen.blit(upgrade_text, upgrade_rect)

        option_font = pygame.font.Font(None, 24)
        option_y = upgrade_rect.bottom + 20
        for i, upgrade in enumerate(self.upgrades_available, start=1):
            option_text = option_font.render(f"{i}. {upgrade}", True, (255, 255, 255))
            option_rect = option_text.get_rect(midtop=(self.settings.screen_width // 2, option_y))
            self.screen.blit(option_text, option_rect)
            option_y += option_rect.height + 10

        pygame.display.flip()

    def _handle_upgrade_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self._apply_upgrade(1)
                elif event.key == pygame.K_2:
                    self._apply_upgrade(2)
                elif event.key == pygame.K_3:
                    self._apply_upgrade(3)
    
    def _apply_upgrade(self, choice):
        if choice == 1:
            self.settings.ship_limit += 1
            self.stats.ships_left += 1
        elif choice == 2:
            self.settings.ship_speed += 5
        elif choice == 3:
            self.settings.bullet_width += 20
    
    def _pause_game(self):
        """Pause the game loop."""
        self.stats.game_active = False

    def _resume_game(self):
            """Resume the game loop."""
            self.stats.game_active = True
    def _prompt_upgrade(self):
        self.stats.game_active = False  # Pause the game

        upgrade_font = pygame.font.SysFont(None, 48)
        text_color = (255, 255, 255)
        upgrade_texts = [
            "Congratulations! You've reached a milestone level.",
            "Choose an upgrade:",
            "1. Extra life",
            "2. Faster Ship",
            "3. Thicker bullets"
        ]
        upgrade_surfaces = [upgrade_font.render(text, True, text_color) for text in upgrade_texts]

        # Display upgrade options on the screen
        while True:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self._apply_upgrade(1)
                        return
                    elif event.key == pygame.K_2:
                        self._apply_upgrade(2)
                        return
                    elif event.key == pygame.K_3:
                        self._apply_upgrade(3)
                        return

            # Clear the screen
            self.screen.fill((0, 0, 0))

            # Draw upgrade texts on the screen
            for i, surface in enumerate(upgrade_surfaces):
                self.screen.blit(surface, (10, 10 + i * 50))

            pygame.display.flip()
            self.clock.tick(30)

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()

quit()
import pygame
import math

# Settings class to store game configuration
class Settings:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.fps = 60
        self.triangle_size = 20
        self.projectile_speed = 5
        self.colors = {
            'white': (255, 255, 255),
            'black': (0, 0, 0),
            'red': (255, 0, 0)
        }

# Spaceship class to handle player movement and drawing
class Spaceship:
    def __init__(self, settings):
        self.settings = settings
        self.position = pygame.Vector2(self.settings.width // 2, self.settings.height // 2)
        self.angle = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.angle -= 5
            self.angle -= 324
        if keys[pygame.K_RIGHT]:
            self.angle += 5

    def draw(self, surface):
        points = [
            pygame.Vector2(0, -self.settings.triangle_size),  # top point
            pygame.Vector2(-self.settings.triangle_size / 2, self.settings.triangle_size),  # left side point
            pygame.Vector2(self.settings.triangle_size / 2, self.settings.triangle_size)  # right side point
        ]
        rotated_points = [point.rotate(self.angle) + self.position for point in points]
        pygame.draw.polygon(surface, self.settings.colors['white'], rotated_points)

# Projectile class to handle projectile movement and drawing
class Projectile:
    def __init__(self, position, angle, settings):
        self.position = position.copy()
        self.direction = pygame.Vector2(0, -1).rotate(angle)
        self.settings = settings

    def move(self):
        self.position += self.direction * self.settings.projectile_speed

    def draw(self, surface):
        pygame.draw.circle(surface, self.settings.colors['red'], (int(self.position.x), int(self.position.y)), 5)

# Game class to manage the game loop and objects
class Game:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("Really Boring Asteroids")
        self.clock = pygame.time.Clock()
        self.running = True
        self.spaceship = Spaceship(self.settings)
        self.projectiles = []

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # Create and fire a projectile
                    new_projectile = Projectile(self.spaceship.position, self.spaceship.angle, self.settings)
                    self.projectiles.append(new_projectile)

    def update(self):
        # Update spaceship
        self.spaceship.handle_input()

        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.move()
            if not (0 <= projectile.position.x <= self.settings.width) or not (0 <= projectile.position.y <= self.settings.height):
                self.projectiles.remove(projectile)

    def draw(self):
        self.screen.fill(self.settings.colors['black'])
        self.spaceship.draw(self.screen)
        for projectile in self.projectiles:
            projectile.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.settings.fps)
        pygame.quit()

# Start the game
if __name__ == "__main__":
    game = Game()
    game.run()

import pygame
import random
from pathlib import Path

# Initialize Pygame
pygame.init()

images_dir = Path(__file__).parent / "images" if (Path(__file__).parent / "images").exists() else Path(__file__).parent / "assets"

# Screen dimensions
WIDTH, HEIGHT = 600, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dino Jump")

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# FPS
FPS = 60

# Player attributes
PLAYER_SIZE = 25
player_speed = 5

# Obstacle attributes
OBSTACLE_WIDTH = 20
MIN_OBSTACLE_HEIGHT = 20
MAX_OBSTACLE_HEIGHT = 100
obstacle_speed = 5

# Font
font = pygame.font.SysFont(None, 36)

# Define an obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, random.randint(MIN_OBSTACLE_HEIGHT, MAX_OBSTACLE_HEIGHT)))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)  # Randomly place obstacle within screen

        self.explosion = pygame.image.load(images_dir / "explosion1.gif") if images_dir.exists() else None

    def update(self):
        self.rect.x -= obstacle_speed
        # Remove the obstacle if it goes off screen
        if self.rect.right < 0:
            self.kill()

    def explode(self):
        """Replace the image with an explosion image."""
        if self.explosion:
            self.image = self.explosion
            self.image = pygame.transform.scale(self.image, (OBSTACLE_WIDTH, self.rect.height))
            self.rect = self.image.get_rect(center=self.rect.center)

# Define a player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT - PLAYER_SIZE - 10
        self.speed = player_speed

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

        # Keep the player on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Create a player object
player = Player()
player_group = pygame.sprite.GroupSingle(player)

# Add obstacles periodically
def add_obstacle(obstacles):
    # random.random() returns a random float between 0 and 1, so a value
    # of 0.4 means that there is a 40% chance of adding an obstacle.
    if random.random() < 0.4:
        obstacle = Obstacle()
        obstacles.add(obstacle)
        return 1
    return 0

# Main game loop
def game_loop():
    clock = pygame.time.Clock()
    game_over = False
    last_obstacle_time = pygame.time.get_ticks()

    # Group for obstacles
    obstacles = pygame.sprite.Group()

    obstacle_count = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        # Update player
        player.update()

        # Add obstacles and update
        if pygame.time.get_ticks() - last_obstacle_time > 500:
            last_obstacle_time = pygame.time.get_ticks()
            obstacle_count += add_obstacle(obstacles)
        
        obstacles.update()

        # Check for collisions
        collider = pygame.sprite.spritecollide(player, obstacles, dokill=False)
        if collider:
            collider[0].explode()  # Trigger explosion animation for obstacle
            game_over = True  # End the game when a collision happens

        # Draw everything
        screen.fill(WHITE)
        pygame.draw.rect(screen, BLUE, player.rect)
        obstacles.draw(screen)

        # Display obstacle count
        obstacle_text = font.render(f"Obstacles: {obstacle_count}", True, BLACK)
        screen.blit(obstacle_text, (10, 10))

        pygame.display.update()
        clock.tick(FPS)

    # Game over screen
    game_over_text = font.render("Game Over!", True, BLACK)
    screen.fill(WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Wait for 2 seconds before quitting

if __name__ == "__main__":
    game_loop()
    pygame.quit()

import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images
bg_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/background.png')
base_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/base.png')
bird_down_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/bluebird-downflap.png')
bird_mid_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/bluebird-midflap.png')
bird_up_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/bluebird-upflap.png')
pipe_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/pipe-green.png')
gameover_img = pygame.image.load('lessons/07_Projects/01_Flappy_Bird/images/gameover.png')

# Resize images
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
base_img = pygame.transform.scale(base_img, (SCREEN_WIDTH, 100))
pipe_img = pygame.transform.scale(pipe_img, (70, 500))

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.width = bird_mid_img.get_width()
        self.height = bird_mid_img.get_height()
        self.image = bird_mid_img
        self.rect = self.image.get_rect(center=(self.x, self.y))

    def move(self):
        self.velocity += 1  # Gravity
        self.y += self.velocity
        if self.y < 0:
            self.y = 0
        if self.y > SCREEN_HEIGHT - self.height:
            self.y = SCREEN_HEIGHT - self.height
        self.rect.centery = self.y

    def jump(self):
        self.velocity = -10  # Jump impulse

    def update(self):
        self.move()
        self.image = bird_mid_img  # Keep the bird in the mid flap
        screen.blit(self.image, self.rect)

# Pipe class
# Pipe class
class Pipe:
    def __init__(self, x):
        self.gap = 300  # Increased gap between the pipes
        self.x = x
        # Ensure there's enough space for both pipes and the gap
        self.height = random.randint(0, SCREEN_HEIGHT - self.gap - 100)  # Random height for the top pipe
        
        # Define the top and bottom pipe positions
        self.top_rect = pygame.Rect(self.x, 0, pipe_img.get_width(), self.height)
        self.bottom_rect = pygame.Rect(self.x, self.height + self.gap, pipe_img.get_width(), SCREEN_HEIGHT - self.height - self.gap)

        # Debugging print statements
        print(f"Pipe created at x: {self.x}, top height: {self.height}, bottom y: {self.height + self.gap}")

    def move(self):
        self.x -= 5  # Move the pipes leftward
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Make sure the pipes are within bounds before drawing
        if self.top_rect.x + self.top_rect.width > 0:  # Only draw pipes if they are visible on screen
            screen.blit(pipe_img, self.top_rect)
            screen.blit(pipe_img, self.bottom_rect)

    def off_screen(self):
        return self.x < -pipe_img.get_width()

    def collide(self, bird_rect):
        return self.top_rect.colliderect(bird_rect) or self.bottom_rect.colliderect(bird_rect)

# Base class
class Base:
    def __init__(self):
        self.x = 0
        self.y = SCREEN_HEIGHT - 100
        self.image = base_img
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def move(self):
        self.x -= 5
        if self.x < -SCREEN_WIDTH:
            self.x = 0
        self.rect.x = self.x

    def draw(self):
        screen.blit(self.image, self.rect)

# Game Initialization function
def init_game():
    bird = Bird()
    base = Base()
    pipes = []
    clock = pygame.time.Clock()
    score = 0
    game_over = False
    bird_alive = True

    # Game Over Image position
    game_over_rect = gameover_img.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))

    return bird, base, pipes, clock, score, game_over, bird_alive, game_over_rect

# Main game loop
def game_loop():
    bird, base, pipes, clock, score, game_over, bird_alive, game_over_rect = init_game()

    while True:
        screen.fill(WHITE)
        screen.blit(bg_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # If the player clicks anywhere after the game over, nothing happens
            # We don't restart the game
            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_over and game_over_rect.collidepoint(event.pos):
                    # No restart action, game stays in the game over state
                    pass

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_over:
                    bird.jump()

        if not game_over:
            bird.update()
            base.move()

            # Pipe movement and spawning
            if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 300:
                pipes.append(Pipe(SCREEN_WIDTH))

            for pipe in pipes:
                pipe.move()
                pipe.draw()

                if pipe.off_screen():
                    pipes.remove(pipe)

                if pipe.collide(bird.rect):
                    bird_alive = False

            if bird_alive:
                score += 0.1
            else:
                game_over = True

            base.draw()
        else:
            # Display game over screen and show instruction to exit or just leave the screen
            screen.blit(gameover_img, (SCREEN_WIDTH // 2 - gameover_img.get_width() // 2, SCREEN_HEIGHT // 3))


        pygame.display.update()
        clock.tick(FPS)

# Start the game loop
game_loop()

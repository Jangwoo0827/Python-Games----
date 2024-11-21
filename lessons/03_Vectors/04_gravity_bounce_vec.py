import pygame
from jtlgames.spritesheet import SpriteSheet
from pathlib import Path
from dataclasses import dataclass

pygame.init()
screen = pygame.display.set_mode((800, 400))

# Path to the image
spritesheet_path = Path(__file__).parent.parent / '06_Surfaces' / 'images' / 'spritesheet.png'

# Create sprite sheet instance
sprite_sheet = SpriteSheet(spritesheet_path, (16, 16))
image_path = sprite_sheet.image_at(4)  # Get the frog sprite from the spritesheet

class Colors:
    """Constants for Colors"""
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    PLAYER_COLOR = (0, 0, 255)
    BACKGROUND_COLOR = (0, 0, 0)


@dataclass
class GameSettings:
    """Settings for the game"""
    width: int = 600
    height: int = 400
    gravity: float = 0.3
    player_start_x: int = 100
    player_start_y: int = None
    player_v_y: float = 0  # Initial y velocity
    player_v_x: float = 4  # Initial x velocity
    player_width: int = 50
    player_height: int = 50
    player_jump_velocity: float = 10
    frame_rate: int = 50
    drag_coefficient: float = 0.005  # The coefficient for drag


class Game:
    """Main object for the top level of the game."""

    def __init__(self, settings: GameSettings):
        pygame.init()

        self.settings = settings
        self.running = True

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        self.clock = pygame.time.Clock()

        # Turn Gravity into a vector
        self.gravity = pygame.Vector2(0, self.settings.gravity)

    def run(self):
        """Main game loop"""
        player = Player(self)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    player.jump()  # Trigger jump on spacebar press

            player.update()

            self.screen.fill(Colors.BACKGROUND_COLOR)
            player.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(self.settings.frame_rate)

        pygame.quit()


class Player:
    """Player class, representing a frog character"""

    def __init__(self, game: Game):
        self.game = game
        settings = self.game.settings

        # Load the frog image from the spritesheet
        self.image = image_path  # Already loaded from the sprite sheet
        self.original_width = settings.player_width
        self.original_height = settings.player_height

        # Player position
        self.pos = pygame.Vector2(settings.player_start_x,
                                   settings.player_start_y if settings.player_start_y is not None else settings.height - self.original_height)

        # Player's velocity
        self.vel = pygame.Vector2(settings.player_v_x, 0)  # Initial vertical velocity is 0
        self.rotation_angle = 0  # To keep track of rotation
        self.is_jumping = False

    def update(self):
        """Update player position, continuously jumping"""
        self.update_jump()
        self.update_v()
        self.update_pos()

    def update_v(self):
        """Update the player's velocity based on gravity, drag, and bounce on edges"""
        self.vel.y += self.game.gravity.y  # Apply gravity

        # Apply drag only when the player is moving
        if self.vel.length() > 0:
            drag_force = self.vel * -self.game.settings.drag_coefficient
            self.vel += drag_force  # Apply drag to velocity

        if self.at_bottom() and self.vel.y > 0:
            self.vel.y = 0
            self.is_jumping = False

        # Rotate the frog only if the player is not at the bottom
        if not self.at_bottom():
            self.rotation_angle += 5  # Adjust rotation speed as needed
        else:
            self.rotation_angle = 0  # Reset rotation when on the ground

    def update_pos(self):
        """Update the player's position based on velocity"""
        self.pos += self.vel  # Update the player's position based on the current velocity

        if self.at_bottom():
            self.pos.y = self.game.settings.height - self.original_height

        if self.at_bottom() and self.vel.y == 0:
            self.is_jumping = False

        if self.at_bottom():
            self.vel.y = 0
        elif self.at_top():
            self.vel.y = -self.vel.y  # Bounce off the top.

        if self.at_left() and self.vel.x < 0 or self.at_right() and self.vel.x > 0:
            self.vel.x = -self.vel.x

    def update_jump(self):
        """Handle the player's jumping logic"""
        if self.at_bottom() and not self.is_jumping:
            self.vel.y -= self.game.settings.player_jump_velocity
            self.is_jumping = True
    
    def jump(self):
        """Player can jump if they're at the bottom"""
        if self.at_bottom() and not self.is_jumping:
            self.vel.y -= self.game.settings.player_jump_velocity
            self.is_jumping = True

    def at_top(self):
        """Check if the player is at the top of the screen"""
        return self.pos.y <= 0

    def at_bottom(self):
        """Check if the player is at the bottom of the screen"""
        return self.pos.y >= self.game.settings.height - self.original_height

    def at_left(self):
        """Check if the player is at the left of the screen"""
        return self.pos.x <= 0

    def at_right(self):
        """Check if the player is at the right of the screen"""
        return self.pos.x >= self.game.settings.width - self.original_width

    def draw(self, screen):
        # Only stretch vertically while jumping
        scale_factor_y = 1
        if self.is_jumping:
            scale_factor_y = 1.2  # Stretch vertically while jumping
        
        # Calculate new dimensions with vertical scaling
        scaled_width = self.original_width
        scaled_height = int(self.original_height * scale_factor_y)

        # Rotate the image if in the air
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)

        # Draw the scaled and rotated image
        scaled_image = pygame.transform.scale(rotated_image, (scaled_width, scaled_height))
        screen.blit(scaled_image, (self.pos.x - (scaled_width - self.original_width) // 2,
                                self.pos.y - (scaled_height - self.original_height) // 2))

        # Calculate new dimensions with vertical scaling
        scaled_width = self.original_width
        scaled_height = int(self.original_height * scale_factor_y)

        # Rotate the image if in the air
        rotated_image = pygame.transform.rotate(self.image, self.rotation_angle)

        # Draw the scaled and rotated image
        scaled_image = pygame.transform.scale(rotated_image, (scaled_width, scaled_height))
        screen.blit(scaled_image, (self.pos.x - (scaled_width - self.original_width) // 2,
                                   self.pos.y - (scaled_height - self.original_height) // 2))


settings = GameSettings()
game = Game(settings)
game.run()

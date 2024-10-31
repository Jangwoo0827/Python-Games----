import pygame

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
SQUARE_SIZE = 50
SQUARE_COLOR = (255, 0, 0)  # Red
K = 1.5

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Accelerating Red Square")

# Square starting position
x_pos = 20
y_pos = (SCREEN_HEIGHT - SQUARE_SIZE) // 2
velocity = 0

# Movement direction: 1 for right, -1 for left
direction = 1

# Main loop
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            
            running = False
         
    # Calculate the spring force, which is the force that pulls the square back
    # to the center, as if it was attached to a spring
    a = -K * (x_pos - (SCREEN_WIDTH-SQUARE_SIZE) // 2)

    # Update the velocity with the acceleration. Notice that we change
    # the velocity by adding the acceleration, not setting it to the acceleration, 
    # and we change it a bit each frame. 
    velocity += a
    
    # Update the position with the velocity. Like with the velocity, we change
    # the position by adding the velocity, not setting it to the velocity, and
    # we change it a bit each frame.
    x_pos += velocity

    # Fill the screen with black (clears previous frame)
    screen.fill((0, 0, 0))

    # Draw the red square
    pygame.draw.rect(screen, SQUARE_COLOR, (x_pos, y_pos, SQUARE_SIZE, SQUARE_SIZE))

    # Update the display
    pygame.display.flip()

    # Frame rate control
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()

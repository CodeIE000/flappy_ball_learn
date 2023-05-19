import pygame
import random

# Initialize Pygame
pygame.init()

# Set the screen dimensions
screen_width = 400
screen_height = 600

# Set the wall dimensions
wall_width = 50
wall_gap = 200  # Gap between the walls
wall_velocity = 5

# Set the colors for the walls
wall_color = (0, 255, 0)  # Green color

# Set the initial positions of the walls
wall_x = random.randint(0, screen_width - wall_width)  # Random horizontal position
wall_y = -wall_gap - wall_width  # Start above the screen

# Create the Pygame screen
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the walls from top to bottom
    wall_y += wall_velocity

    # Check if the walls have reached the bottom of the screen
    if wall_y > screen_height:
        # Reset the walls' positions to the top of the screen
        wall_y = -wall_gap - wall_width

        # Randomize the horizontal position for the next pair of walls
        wall_x = random.randint(0, screen_width - wall_width)

    # Clear the screen
    screen.fill((0, 0, 0))  # Black color

    # Draw the walls
    pygame.draw.rect(screen, wall_color, (wall_x, wall_y, wall_width, wall_width))
    pygame.draw.rect(screen, wall_color, (wall_x, wall_y + wall_gap + wall_width, wall_width, wall_width))

    # Update the display
    pygame.display.flip()

    # Set the frame rate
    clock.tick(60)  # 60 FPS

# Quit Pygame and exit the program
pygame.quit()

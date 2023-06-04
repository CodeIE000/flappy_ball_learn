import pygame
import os

pygame.init()

# Window dimensions
WIN_WIDTH = 800
WIN_HEIGHT = 600

# Background dimensions
BG_WIDTH = 800
BG_HEIGHT = 600

# Initialize the window and clock
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
clock = pygame.time.Clock()

# Load the backgrounds
backgrounds = [
    pygame.image.load(os.path.join("imgs", "bg.png")),
    pygame.image.load(os.path.join("imgs", "bg1.png")),
    pygame.image.load(os.path.join("imgs", "bg2.png"))
]

# Define the initial positions for the backgrounds
initial_positions = [(0, 0), (0, BG_HEIGHT), (0, 2 * BG_HEIGHT)]

# Create a list to store the background objects and their positions
background_objects = [(backgrounds[i], position) for i, position in enumerate(initial_positions)]

# Background movement speed
BG_SPEED = 1

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update the positions of the backgrounds
    for i in range(len(background_objects)):
        x, y = background_objects[i][1]
        # Move the backgrounds downward
        y += BG_SPEED
        # Check if a background has moved off the screen, reset its position
        if y >= WIN_HEIGHT:
            y = -BG_HEIGHT
        # Update the position in the list
        background_objects[i] = (background_objects[i][0], (x, y))

    # Redraw the window
    win.fill((255, 255, 255))  # Fill with white color
    for background, position in background_objects:
        win.blit(background, position)

    pygame.display.update()
    clock.tick(60)  # Limit the frame rate to 60 FPS

pygame.quit()

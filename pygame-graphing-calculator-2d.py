import pygame

from pygame.locals import (
    K_ESCAPE,
)

class CalculatorSettings2D:
    def __init__(self):
        self.min_x = -10
        self.max_x = 10
        self.min_y = -10
        self.max_y = 10
        
class ScreenSettings:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

def x_pixel_to_x(x_pixel, calcSettings, screenSettings):
    return calcSettings.min_x + (x_pixel / screenSettings.width) * (calcSettings.max_x - calcSettings.min_x)
    
def y_to_y_pixel(y, calcSettings, screenSettings):
    if not (calcSettings.min_y < y < calcSettings.max_y):
        return None
    return screenSettings.height - int(((y - calcSettings.min_y) / (calcSettings.max_y - calcSettings.min_y)) * screenSettings.height)
    
def get_y_pixel(x_pixel, f, calcSettings, screenSettings):
    x = x_pixel_to_x(x_pixel, calcSettings, screenSettings)
    y = f(x)
    y_pixel = y_to_y_pixel(y, calcSettings, screenSettings)
    return y_pixel

def renderGraph(f, calcSettings, screenSettings):
    pygame.draw.line(screenSettings.screen, (0,0,0), (screenSettings.width // 2, 0), (screenSettings.width // 2, screenSettings.height))
    pygame.draw.line(screenSettings.screen, (0,0,0), (0, screenSettings.height // 2), (screenSettings.width, screenSettings.height // 2))

    prev = (0,None)
    for x_pixel in range(screenSettings.width):
        y_pixel = get_y_pixel(x_pixel, f, calcSettings, screenSettings)
        if y_pixel is not None:
            if prev[1] is not None:
                pygame.draw.line(screenSettings.screen, (255,0,0), prev, (x_pixel, y_pixel))
            else:
                screenSettings.screen.set_at((x_pixel, y_pixel), (255,0,0))
        prev = (x_pixel, y_pixel)
pygame.init()

# Set up the drawing window
# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screenSettings = ScreenSettings(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
calcSettings = CalculatorSettings2D()

# Run until the user asks to quit
running = True
while running:

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    def f(x):
        return x*x + x

    renderGraph(f, calcSettings, screenSettings)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
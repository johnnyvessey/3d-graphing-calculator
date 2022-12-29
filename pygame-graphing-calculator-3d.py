import pygame
from utils3dcalc import *
from calculatorClasses import *
import math

from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_w,
    K_s,
)


SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700     
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

screenSettings = ScreenSettings(SCREEN_WIDTH, SCREEN_HEIGHT, screen)
calcSettings = CalculatorSettings3D()

#this is where the function that you want to graph is defined
f = lambda x,y: x * math.sin(x * math.pi) + math.sin(y * math.pi)

calculator = Calculator(f, calcSettings, screenSettings)
viewpoint = Viewpoint(.01)

x_cross_sections, y_cross_sections, grid_draw_locations = calculator.getDrawGrid()

pygame.init()

pygame.font.init() 
my_font = pygame.font.SysFont('Times New Roman', 15)

theta, phi = 0,0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_UP:
                phi += .1
            elif event.key == K_DOWN:
                phi -= .1
            elif event.key == K_LEFT:
                theta -= .1
            elif event.key == K_RIGHT:
                theta += .1
            elif event.key == K_s:
                viewpoint.viewpoint_scale += .002
            elif event.key == K_w:
                if viewpoint.viewpoint_scale >= .006:
                    viewpoint.viewpoint_scale -= .002

            viewpoint.viewpoint_center_vector = get_viewpoint_from_angles(theta, phi)
            u,v = get_screen_basis_vectors(viewpoint, theta, phi)

            screen.fill((255, 255, 255))
            calculator.renderAxes(viewpoint, u, v)
            calculator.renderGraph(viewpoint, grid_draw_locations, x_cross_sections, y_cross_sections, u, v)

            #render text info
            text_surface = my_font.render(f"theta {round(theta,1)}; phi {round(phi,1)}; {viewpoint.viewpoint_center_vector}", False, (0, 0, 0))
            screen.blit(text_surface, (0,100))

    # Flip the display
    pygame.display.flip()

pygame.quit()


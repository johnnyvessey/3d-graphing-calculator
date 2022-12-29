from utils3dcalc import *
import pygame

class CalculatorSettings3D:
    def __init__(self):
        self.min_x = -1
        self.max_x = 1
        self.min_y = -1
        self.max_y = 1
        self.min_z = -2
        self.max_z = 2

        self.cross_section_density = 25


#get x and y locations to have the graph lines be drawn at to approximate the 3d surface
    def get_x_cross_sections(self):
        return [self.min_x + i * ((self.max_x - self.min_x) / self.cross_section_density) for i in range(self.cross_section_density + 1)]

    def get_y_cross_sections(self):
        return [self.min_y + i * ((self.max_y - self.min_y) / self.cross_section_density) for i in range(self.cross_section_density + 1)]

        
class ScreenSettings:
    def __init__(self, width, height, screen):
        self.width = width
        self.height = height
        self.screen = screen

class Viewpoint:
    def __init__(self,viewpoint_scale):
        self.viewpoint_center_vector = [1,1,1]
        self.viewpoint_scale = viewpoint_scale

class Calculator:
    def __init__(self, f, calcSettings, screenSettings):
        self.calcSettings = calcSettings
        self.screenSettings = screenSettings
        self.f = f
    
    def getDrawGrid(self):
        x_cross_sections = self.calcSettings.get_x_cross_sections()
        y_cross_sections = self.calcSettings.get_y_cross_sections()
        grid_draw_locations = [[(None, None) for _ in range(len(x_cross_sections))] for _ in range(len(y_cross_sections))]

        return x_cross_sections, y_cross_sections, grid_draw_locations

    def renderGraph(self,viewpoint, grid_draw_locations, x_cross_sections, y_cross_sections, u, v):

        
        #draw grid approximation of surface
        for x_index in range(len(x_cross_sections)):
            for y_index in range(len(y_cross_sections)):
                x,y = x_cross_sections[x_index], y_cross_sections[y_index]
                hit = raycast_from_location(x,y, self.f, viewpoint, self, u, v)
                grid_draw_locations[x_index][y_index] = hit

        #draw lines between adjacent points on grid on the transformed space (based on viewpoint)
        for x_index in range(len(grid_draw_locations) - 1):
            for y_index in range(len(grid_draw_locations[0]) - 1):
                cur_pixel_location = grid_draw_locations[x_index][y_index]
                if cur_pixel_location:
                    right_pixel_location = grid_draw_locations[x_index+1][y_index]
                    down_pixel_location = grid_draw_locations[x_index][y_index+1]

                    cur_z = self.f(x_cross_sections[x_index], y_cross_sections[y_index])
                    if right_pixel_location:
                        right_z = self.f(x_cross_sections[x_index+1], y_cross_sections[y_index])
                        color = get_line_color_from_z(.5 * (cur_z + right_z), self.calcSettings)
                        pygame.draw.line(self.screenSettings.screen, color, cur_pixel_location, right_pixel_location)
                    if down_pixel_location:
                        down_z = self.f(x_cross_sections[x_index], y_cross_sections[y_index+1])
                        color = get_line_color_from_z(.5 * (cur_z + down_z), self.calcSettings)
                        pygame.draw.line(self.screenSettings.screen, color, cur_pixel_location, down_pixel_location)

    def renderAxes(self, viewpoint, u, v):
        #draw axes
        for i, (axis_top, axis_bot) in enumerate(get_axes(viewpoint, self.calcSettings, self.screenSettings, u, v)):
            color = [(255,0,0), (0,255,0), (0,0,255)]
            pygame.draw.line(self.screenSettings.screen, color[i], axis_top, axis_bot)




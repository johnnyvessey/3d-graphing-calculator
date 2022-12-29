import math
import numpy as np


def sgn(x):
    if x == 0:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


def get_origin(calcSettings):
    return (calcSettings.max_x - calcSettings.min_x)/2, (calcSettings.max_y - calcSettings.min_y)/2, (calcSettings.max_z - calcSettings.min_z)/2

def get_point_at_t_on_line(x0,y0,z0, nx, ny, nz, t):
    return (x0 + t * nx, y0 + t * ny, z0 + t * nz)

def getPlaneEquation(calculator, viewpoint):
    origin = get_origin(calculator.calcSettings)
    #next step: incorporate 'origin' -> make it be centered on viewpoint center
    a,b,c = viewpoint.viewpoint_center_vector
    d = - (a*a + b*b + c*c)
    return a,b,c,d

#defining this to get around numpy bug that makes code marked as "unreachable"
cross_product = lambda x,y: np.cross(x,y)

def get_screen_basis_vectors(viewpoint, theta, phi):
    nx,ny,nz = viewpoint.viewpoint_center_vector

    ux,uy = 0,0
    if nx == 0:
        uy = 0
        ux = 1
    else:
        tmp = math.sqrt(1 + (ny/nx)*(ny/nx))
        uy = 1 / tmp
        ux = -ny / (nx * tmp)

    u = [ux,uy,0]


    n = [nx,ny,nz]

    v = cross_product(u,n)
    magV = math.sqrt(sum(x*x for x in v))
    v = list(-x / magV for x in v)


    if nx < 0:
        u = [-p for p in u]
        v = [-p for p in v]
  
    return u,v

#get pixel coordinates on screen for x,y,z point
def project(u,v, x, y, z):
    newX, newY = np.dot(u, [x,y,z]), np.dot(v, [x,y,z])
    return newX, newY

def get_line_color_from_z(z, calcSettings):
    #This is assuming that the calculator will always be centered on (0,0,0)
    return (0, 0 , 255 * z / calcSettings.min_z) if z < 0 else (255 * z / calcSettings.max_z,0,0)

def get_viewpoint_from_angles(theta, phi):
    return [math.cos(theta) * math.cos(phi), math.sin(theta) * math.cos(phi), math.sin(phi)]
    
def get_axes(viewpoint, calcSettings, screenSettings, u, v):
    x_axis = (project(u, v, calcSettings.max_x, 0, 0), project(u,v, 0, 0, 0))
    y_axis = (project(u,v, 0, calcSettings.max_y, 0), project(u,v, 0, 0, 0))
    z_axis = (project(u,v, 0, 0, calcSettings.max_z), project(u,v, 0, 0, 0))

    return ([on_screen(x[0], x[1], viewpoint, screenSettings) for x in x_axis], [on_screen(y[0], y[1], viewpoint, screenSettings) for y in y_axis], [on_screen(z[0], z[1], viewpoint, screenSettings) for z in z_axis])

def on_screen(u,v,viewpoint, screenSettings):
    u_width = (screenSettings.width * viewpoint.viewpoint_scale) / 2
    v_height = (screenSettings.height * viewpoint.viewpoint_scale) / 2

    if not (-u_width < u < u_width and -v_height < v < v_height):
        return None
    u_pixel = screenSettings.width * (u + u_width) / (2*u_width)
    v_pixel = screenSettings.height * (v + v_height) / (2 * v_height)

    return u_pixel, screenSettings.height - v_pixel #y-axis on screen is flipped

def within_bounds(x,y,z, calcSettings):
    return calcSettings.min_x < x < calcSettings.max_x and calcSettings.min_y < y < calcSettings.max_y and calcSettings.min_z < z < calcSettings.max_z


#shoot out ray in direction of the viewpoint from the x,y,z location
#if it hits the surface before getting to the viewpoint, return None (because it was blocked)
#return location on screen where the ray hits (if it does hit the screen)
#after getting raycast hits from all of the grid locations, draw lines between the points of adjacent grid locations
def raycast_from_location(x0, y0, f, viewpoint, calculator, u, v):
    nx,ny,nz = viewpoint.viewpoint_center_vector

    z0 = f(x0,y0)
    if not within_bounds(x0,y0,z0, calculator.calcSettings):
        return None
    prevG = None
    step_size = 0.2
    t = step_size #start a little bit out from the surface so it doesn't say it collides with itself right away

    while True:
        x,y,z = get_point_at_t_on_line(x0,y0,z0,nx,ny,nz, t)
        if within_bounds(x,y,z, calculator.calcSettings):
            g = z - f(x,y)
            if prevG is not None and sgn(g) != sgn(prevG):
                return None   
            prevG = g
        else:
            u,v = project(u, v, x0,y0,z0)
            return on_screen(u,v, viewpoint, calculator.screenSettings)
    
        t += step_size
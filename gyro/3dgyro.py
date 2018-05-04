import pygame
import requests
import math
from requests.auth import HTTPDigestAuth
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

verticies = [
    (1, -0.1, -0.5),
    (1, 0.1, -0.5),
    (-1, 0.1, -0.5),
    (-1, -0.1, -0.5),
    (1, -0.1, 0.5),
    (1, 0.1, 0.5),
    (-1, 0.1, 0.5),
    (-1, -0.1, 0.5),
]

edges = [
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 6),
    (7, 4),
    (7, 3),
    (7, 6),
    (5, 1),
    (5, 4),
    (5, 6),
]

surfaces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6),
]

triangles = [
    (0, 1, 2),
    (0, 3, 2),
    (4, 5, 6),
    (4, 7, 6),
    (1, 2, 6),
    (1, 5, 6),
    (0, 3, 7),
    (0, 4, 7),
    (0, 1, 5),
    (0, 4, 5),
    (2, 3, 7),
    (2, 6, 7),
]

def dist(a,b):
	return math.sqrt((a*a)+(b*b))

def get_y_rotation(x,y,z):
	radians = math.atan2(x, dist(y,z))
	return -math.degrees(radians)

def get_x_rotation(x,y,z):
	radians = math.atan2(y, dist(x,z))
	return math.degrees(radians)

def read_values():
    link = "http://192.168.77.183/axis-cgi/admin/uptime.cgi" # Change this address to your settings
    r = requests.get(link, auth=HTTPDigestAuth('root', 'pass'))
    values = r.text.split(' ')
    accel_x = float(values[0])/16384.0
    accel_y = float(values[1])/16384.0
    accel_z = float(values[2])/16384.0

    x_rot = get_x_rotation(accel_x, accel_y, accel_z);
    y_rot = get_y_rotation(accel_x, accel_y, accel_z);

    return str(x_rot) + " " + str(y_rot)

def Cube_line():
    glBegin(GL_LINES)
    glColor3fv((0.2, 1, 1))
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()

def Cube_triangle():
    glBegin(GL_TRIANGLES)
    glColor3fv((0.0, 0.8, 0.8))
    for triangle in triangles:
        for vertex in triangle:
            glVertex3fv(verticies[vertex])
    glEnd()

def background():
    glColor((1.0, 1.0, 1.0))
    glLineWidth(0.1)
    glBegin(GL_LINES)

    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1,-1)
        glVertex3f(x/10.,-1,1)
        
    for x in range(-20, 22, 2):
        glVertex3f(x/10.,-1, 1)
        glVertex3f(x/10., 1, 1)
        
    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f( 2, -1, z/10.)

    for z in range(-10, 12, 2):
        glVertex3f(-2, -1, z/10.)
        glVertex3f(-2,  1, z/10.)

    for z in range(-10, 12, 2):
        glVertex3f( 2, -1, z/10.)
        glVertex3f( 2,  1, z/10.)

    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f( 2, y/10., 1)
        
    for y in range(-10, 12, 2):
        glVertex3f(-2, y/10., 1)
        glVertex3f(-2, y/10., -1)
        
    for y in range(-10, 12, 2):
        glVertex3f(2, y/10., 1)
        glVertex3f(2, y/10., -1)
        
    glEnd()

def run():
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    glViewport(0, 0, display[0], display[1])
    gluPerspective(45.0, (float(display[0])/display[1]), 0.01, 10.0)

    gluLookAt(0.0, 1.0, -5.0,
              0.0, 0.0, 0.0,
              0.0, 1.0, 0.0)
    #glTranslatef(0.0, 0.0, -5)

    #glRotate(float(-28.032), 1, 0, 0)
    #glRotate(-float(-39.4132), 0, 0, 1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        background()
        values = read_values().split(' ')

        glPushMatrix()
        glRotate(float(values[0]), 1, 0, 0)
        glRotate(-float(values[1]), 0, 0, 1)

        Cube_triangle()
        glPopMatrix()

        pygame.display.flip()
        #pygame.time.wait(10)


if __name__ == "__main__":
    run()



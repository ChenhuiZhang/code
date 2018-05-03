import pygame
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
    (-1, -0.1, 0.5),
    (-1, 0.1, 0.5),
]

edges = [
    (0, 1),
    (0, 3),
    (0, 4),
    (2, 1),
    (2, 3),
    (2, 7),
    (6, 4),
    (6, 3),
    (6, 7),
    (5, 1),
    (5, 4),
    (5, 7),
]

surfaces = [
    (0, 1, 2, 3),
    (3, 2, 7, 6),
    (6, 7, 5, 4),
    (4, 5, 1, 0),
    (1, 5, 7, 2),
    (4, 0, 3, 6)
]

def Cube():
    glBegin(GL_LINES)
    glColor3fv((0.2, 1, 1))
    for edge in edges:
        for vertex in edge:
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
        glPushMatrix()
        glRotate(float(-28.032), 1, 0, 0)
        glRotate(-float(-39.4132), 0, 0, 1)

        Cube()
        glPopMatrix()

        pygame.display.flip()
        pygame.time.wait(10)


if __name__ == "__main__":
    run()



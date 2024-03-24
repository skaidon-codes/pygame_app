import random
from typing import Iterator

from pygame_app.engine import create_basic_window
from pygame_app.engine import Engine
from pygame_app.world import World
from pygame_app.object import Object
from pygame_app.utils import get_random_color
import pygame
from OpenGL.GL import *
from OpenGL.GLU import *


class Cube(Object):
    edges = (
        (0, 1),
        (0, 3),
        (0, 4),
        (2, 1),
        (2, 3),
        (2, 7),
        (6, 3),
        (6, 4),
        (6, 7),
        (5, 1),
        (5, 4),
        (5, 7)
    )

    vertices = (
        (1, -1, -1),
        (1, 1, -1),
        (-1, 1, -1),
        (-1, -1, -1),
        (1, -1, 1),
        (1, 1, 1),
        (-1, -1, 1),
        (-1, 1, 1)
    )

    def __init__(self, x: float, y: float, z: float) -> None:
        self.color = get_random_color(70)
        self.scale_growth = 0.01 / random.randint(1, 5)
        self.max_scale = random.randint(4, 6) / 3.0
        self.pos = (x, y, z)
        self.rot = (0.0, 0.0, 0.0)
        self.scale = (1.0, 1.0, 1.0)
        self.growing = True
        self.turn = (random.randrange(-300, 300) / 1000.0,
                     random.randrange(-300, 300) / 1000.0,
                     random.randrange(-300, 300) / 1000.0)

    def draw(self, surface: pygame.Surface) -> None:
        glPushMatrix()
        # specify location of this cube
        glTranslated(self.pos[0], self.pos[1], self.pos[2])
        # scale the cube
        glScaled(self.scale[0], self.scale[1], self.scale[2])
        # specify rotation of this cube around 3 axes
        glRotated(self.rot[0], 1, 0, 0)
        glRotated(self.rot[1], 0, 1, 0)
        glRotated(self.rot[2], 0, 0, 1)
        # draw the cube
        glColor3b(self.color.r, self.color.g, self.color.b)
        glBegin(GL_LINES)
        for edge in Cube.edges:
            for vertex in edge:
                glVertex3fv(Cube.vertices[vertex])
        glEnd()
        glPopMatrix()

    def update(self) -> None:
        self.rot = (self.rot[0] + self.turn[0],
                    self.rot[1] + self.turn[1],
                    self.rot[2] + self.turn[2])
        if self.growing:
            self.scale = (min(self.scale[0] + self.scale_growth, self.max_scale),
                          min(self.scale[1] + self.scale_growth, self.max_scale),
                          min(self.scale[2] + self.scale_growth, self.max_scale))
            if self.scale[0] >= self.max_scale:
                self.growing = False
        else:
            self.scale = (max(self.scale[0] - self.scale_growth, 0.1),
                          max(self.scale[1] - self.scale_growth, 0.1),
                          max(self.scale[2] - self.scale_growth, 0.1))
            if self.scale[0] <= 0.1:
                self.growing = True


class MyWorld(World):
    def __init__(self):
        self.cubes = [Cube(0, 0, 0),
                      Cube(0.5, 0.5, 0.5),
                      Cube(-0.5, -0.5, -0.5),
                      Cube(0.5, -0.5, 0.5),
                      Cube(-0.5, 0.5, -0.5),
                      Cube(0.5, 0.5, -0.5)]

    def init(self, window: pygame.Surface):
        gluPerspective(45, ((1.0 * window.get_width()) / window.get_height()), 0.1, 50.0)
        glTranslatef(0.0, 0.0, -5)

    def pre_update(self) -> None:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def objects(self) -> Iterator[Object]:
        return iter(self.cubes)


def main():
    flags = pygame.OPENGL | pygame.DOUBLEBUF
    window = create_basic_window(600, 400,
                                 "pygame_app/examples/ex2", flags=flags)

    engine = Engine(window, MyWorld(), frame_rate=60)
    engine.init()
    engine.run()


if __name__ == '__main__':
    main()

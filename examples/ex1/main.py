import random
from typing import Iterator

from pygame import Color
from pygame_app.engine import create_basic_window
from pygame_app.engine import Engine
from pygame_app.world import World
from pygame_app.object import Object
from pygame_app.utils import get_random_color
import pygame


class Circle(Object):
    def __init__(self, x: int, y: int) -> None:
        self.color = get_random_color(70)
        self.radius = random.randint(0, 5)
        self.growth = random.randint(1, 5)
        self.max_radius = random.randint(0, 100)
        self.center = (x, y)

    def draw(self, surface: pygame.Surface) -> None:
        if self.radius < self.max_radius:
            pygame.draw.circle(surface, self.color, self.center, self.radius, 1)

    def update(self) -> None:
        self.radius += self.growth


class MyWorld(World):
    def __init__(self):
        self.circles = []
        self.window = None
        self.background_color = pygame.Color(0, 0, 0)

    def init(self, window):
        self.window = window

    def pre_update(self) -> None:
        # delete all overgrown circles at the front of the list
        while self.circles:
            c = self.circles[0]
            if c.radius <= c.max_radius:
                break
            self.circles = self.circles[1:]
        # create a few new circles per frame
        for i in range(5):
            self.create_circle()

    def objects(self) -> Iterator[Object]:
        return iter(self.circles)

    def process_mouse_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.create_circle(*event.pos)

    def get_erase_background_color(self) -> Color:
        return self.background_color

    def create_circle(self, x=None, y=None):
        if x is None:
            x = random.randint(0, self.window.get_width())
        if y is None:
            y = random.randint(0, self.window.get_height())
        self.circles.append(Circle(x, y))


def main():
    flags = 0
    window = create_basic_window(600, 400,
                                 "pygame_app/examples/ex1", flags=flags)

    engine = Engine(window, MyWorld(), frame_rate=60)
    engine.init()
    engine.run()


if __name__ == '__main__':
    main()

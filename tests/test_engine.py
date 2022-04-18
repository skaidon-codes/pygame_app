import pygame

from pygame_app.engine import create_basic_window
from pygame_app.engine import Engine
from pygame_app.world import World


def test_create_basic_window():
    window = create_basic_window(200, 100, "MyGame")
    assert window is not None
    assert isinstance(window, pygame.Surface), "expected pygame.Surface"
    assert window.get_size() == (200, 100)


def test_engine():
    class TestWorld(World):
        pass
    window = create_basic_window(200, 100, "MyGame")
    engine = Engine(window, TestWorld())
    assert engine is not None

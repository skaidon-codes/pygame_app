from typing import Protocol, Iterator, Optional
from pygame_app.object import Object
from pygame import Color


class World(Protocol):
    """Every application must have a single class that implements World protocol"""

    def init(self, window):
        """Called once before entering main loop, links main window to world"""
        pass

    def create_objects(self) -> None:
        """Called once to create initial game objects"""
        pass

    def pre_update(self) -> None:
        """Called before game update"""
        pass

    def post_update(self) -> None:
        """Called after game update"""
        pass

    def objects(self) -> Iterator[Object]:
        return []

    def update_list(self) -> Optional[list]:
        return None

    def process_keyboard_event(self, event):
        pass

    def process_mouse_event(self, event):
        pass

    def process_keyboard_state(self):
        pass

    def get_erase_background_color(self) -> Color:
        """
        This function is called once on startup, application can control whether screen
        contents will be erased to some background color at the beginning of each frame.
        Games that draw entire screen should return None to disable this behavior to improve performance.
        """
        return Color(0, 0, 0)

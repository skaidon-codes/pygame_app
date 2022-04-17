from typing import Protocol


class Object(Protocol):
    def draw(self, surface) -> None:
        """Defines a function that will be called to draw the object"""
        pass

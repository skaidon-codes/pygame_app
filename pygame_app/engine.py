import sys

import pygame

from pygame_app.world import World
from pygame_app import defaults


class Engine:
    def __init__(self, window: pygame.Surface, world: World, frame_rate: int = defaults.FRAME_RATE):
        self.window = window
        self.world = world
        self.frame_rate = frame_rate
        self.background_erase_color = world.get_erase_background_color()

    def draw(self):
        for o in self.world.objects():
            o.draw(self.window)

    def update(self):
        self.world.pre_update()
        for o in self.world.objects():
            o.update()
        self.world.post_update()

    def refresh_screen(self):
        # conditionally erase background
        if self.background_erase_color:
            self.window.fill(self.background_erase_color)

        # redraw world
        self.draw()

        # flip the display buffer
        if self.window.get_flags() & pygame.OPENGL:
            # display.update() does not work with OPENGL
            pygame.display.flip()
        else:
            update_list = self.world.update_list()
            if update_list is not None:
                pygame.display.update(update_list)
            else:
                pygame.display.update()

    def process_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.world.process_mouse_event(event)
        elif event.type == pygame.KEYDOWN:
            self.world.process_keyboard_event(event)
        elif event.type == pygame.QUIT:
            self.exit()

    def init(self):
        self.world.init(self.window)
        self.world.create_objects()

    def run(self):
        fps_controller = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                self.process_event(event)
            self.world.process_keyboard_state()
            self.update()
            self.refresh_screen()
            fps_controller.tick(self.frame_rate)

    @staticmethod
    def exit():
        pygame.quit()
        sys.exit()


def create_basic_window(window_width: int, window_height: int, title: str, flags=0):
    # Checks for errors encountered
    check_errors = pygame.init()
    pygame.font.init()
    # pygame.init() example output -> (6, 0)
    # second number in tuple gives number of errors
    if check_errors[1] > 0:
        print(f'[!] Had {check_errors[1]} errors when initialising game, exiting...')
        sys.exit(-1)
    else:
        print('[+] Game successfully initialised')
    # Initialise game window
    if title:
        pygame.display.set_caption(title)
    game_window = pygame.display.set_mode((window_width, window_height), flags)
    return game_window

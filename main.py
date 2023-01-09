import sys
import pygame
from pygame_tools.asset_machine import AssetMachine
from pygame_tools.state_machine import BaseState
from menu_test1 import MainMenu, Splash
from config import SCREEN_WIDTH, SCREEN_HEIGHT, main_menu_dict, sound_menu_dict, asset_dict


class Game(BaseState):
    def __init__(self, screen, assets, states, start_state):
        self.done = False
        self.screen = screen
        self.assets = assets
        self.states = states
        self.state_name = start_state

        # Get actual state from the state name
        self.state = self.states[self.state_name]

        # initialize the clock
        self.clock = pygame.time.Clock()
        self.fps = 60

        # normally this gets executed in flip_state but not for
        # the base object first time through
        self.persist = {'assets': self.assets, 'states': self.states, 'screen': self.screen}

    def startup(self, persistent):
        self.persist = persistent

    def flip_state(self):
        # current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state.upper()
        persistent = self.state.persist | self.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def event_loop(self):
        for event in pygame.event.get():
            self.state.get_event(event)

    def update(self, dt):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        self.state.draw(self.screen)

    def run(self):
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pygame.display.update()


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # The various processing states, game play, menus, splash screen, etc.
    # Do remember that the game state objects have already run their init
    #   here and not when called.  This is why we have a 'startup' function
    #   in case previous processing has changed something that they need
    #   to react to.
    states = {
        "SPLASH":   Splash("Incompetent Game", 'MENU'),
        "MENU":     MainMenu(main_menu_dict),
        "GAMEPLAY": Splash("GamePlay", 'MENU'),
        "SOUND":    MainMenu(sound_menu_dict),
        "CREDITS":  Splash("Credits", 'MENU'),
        "TVOLUME":  Splash("Theme Volume", 'SOUND'),
        "EVOLUME":  Splash("Effects Volume", 'SOUND'),
    }

    # Gather the assets for this game
    assets = AssetMachine(asset_dict)

    game = Game(screen, assets, states, "SPLASH")
    game.run()

pygame.quit()
sys.exit()

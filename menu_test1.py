import pygame
from pygame_tools.state_machine import BaseState
from pygame_tools.menu_machine1 import MenuEngine


class MainMenu(BaseState):
    def __init__(self, menu_dict):
        ''' executes parent init and gathers parmameter data only
            actual initialization function done by startup function '''
        super().__init__()
        self.menu_dict = menu_dict

    def startup(self, persistent):
        ''' Functionally the __init__ of any child of the State Machine '''
        self.persist = persistent

        # finish menu dictionary setup, replace Font Names with actual Fonts
        #    We do this here because the assets dictionary is passed through 'persisitant'.
        #    This is actually how the State Machine was designed to work.
        if ("Fonts" not in self.menu_dict) or (len(self.menu_dict["Fonts"]) == 0):
            for fontname in self.menu_dict["FontNames"]:
                self.menu_dict["Fonts"].append(persistent['assets'].retrieve_asset(fontname))

        self.menu = MenuEngine(self.persist["screen"], self.menu_dict)

    def get_event(self, event):
        ''' Process Quit and keyboard events '''
        # Check for quit
        if event.type == pygame.QUIT:
            self.done = True
            self.quit = True
            self.run_display = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.menu.current_item -= 1
            elif event.key == pygame.K_DOWN:
                self.menu.current_item += 1
            self.menu.current_item = self.menu.current_item % self.menu.item_count
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.quit = True
                self.run_display = False
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                self.next_state = self.menu.menu_dict["MenuStates"][self.menu.current_item]
                if self.menu.menu_dict["MenuStates"][self.menu.current_item] == 'QUIT':
                    self.quit = True
                self.done = True
                self.run_display = False

    def update(self, dt):
        ''' call the Menu processor update procedure '''
        self.menu.update(dt)  # This rarely has any use

    def draw(self, surface):
        ''' call the Menu processing draw procdure '''
        self.menu.draw(surface)  # This must be called to see the menu


class Splash(BaseState):
    def __init__(self, display_text, next_state):
        super().__init__()
        self.title = self.font.render(display_text, True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = next_state
        self.time_active = 0

    def startup(self, persistent):
        self.persist = persistent
        self.time_active = 0

    def update(self, dt):
        ''' wait three seconds and end '''
        self.time_active += dt
        if self.time_active >= 3000:
            self.done = True

    def draw(self, surface):
        ''' create blank screen and display text '''
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)

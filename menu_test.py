import pygame
from pygame_tools.state_machine import BaseState
from pygame_tools.menu_machine import MenuEngine


class MainMenu(BaseState):
    def __init__(self, menu_dict):
        super().__init__()
        self.menu_dict = menu_dict

    def startup(self, persistent):
        self.persist = persistent
        for fontname in self.menu_dict["FontNames"]:
            self.menu_dict["Fonts"].append(persistent['assets'].retrieve_asset(fontname))
        self.menu = MenuEngine(self.persist["screen"], self.menu_dict)

    def get_event(self, event):
        # Check for quit
        if event.type == pygame.QUIT:
            self.quit = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.done = True
                self.quit = True
                self.run_display = False
            if event.key in [pygame.K_SPACE, pygame.K_RETURN]:
                if self.menu.current_item == 0:
                    self.next_state = "GAMEPLAY"
                elif self.menu.current_item == 1:
                    self.next_state = "SOUND"
                elif self.menu.current_item == 2:
                    self.next_state = "CREDITS"
                elif self.menu.current_item == 3:
                    self.quit = True
                self.done = True
                self.run_display = False
        self.menu.get_event(event)

    def update(self, dt):
        self.menu.update(dt)

    def draw(self, surface):
        self.menu.draw(surface)


class Splash(BaseState):
    def __init__(self, display_text):
        super(Splash, self).__init__()
        self.title = self.font.render(display_text, True, pygame.Color("blue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.next_state = "MENU"
        self.time_active = 0

    def update(self, dt):
        self.time_active += dt
        if self.time_active >= 3000:
            self.done = True

    def draw(self, surface):
        surface.fill(pygame.Color("black"))
        surface.blit(self.title, self.title_rect)

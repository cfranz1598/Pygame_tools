import pygame
import sys

# text with selection cursor
# text that changes color on selection
# with a border or without a border
#
# main_menu_dict = {
#     "MenuTitle": "Main Menu",
#     "MenuItems": ["Start Game", "Sound", "Credits", "Quit Game"],
#     "Cursor": "*",
#     "FontNames": ["titlefont", "sysfont50", "sysfont50"],
#     "Fonts": [],
#     "Colors": ["blue", "white", "red"],
#     "Border": False,
#     "Margin": 30
#     "YTop": 100,
# }

#       Has Border  Has Cursor  Text starts 1 margin below border, items left justified
#       Has Border  No Cursor   Text starts 1 margin below border, centered
#       No Border   Has Cursor  Text starts at YTop, items left justfiied
#       No Border   No Cursor   Text starts at YTop, centered


class MenuEngine():
    def __init__(self, screen, menu_dict):

        # Get and/or validate parameter data
        self.screen = screen
        self.menu_dict = self.validate(menu_dict)  # validate the menu_dict

        # Not sure just how much having this data helps
        self.mid_w = round(screen.get_rect().width / 2)
        self.mid_h = round(screen.get_rect().height / 2)
        self.current_item = 0
        self.menu_fonts = menu_dict["Fonts"]

        # need these data items to calculate the y position of menu items
        self.title_height = 0
        self.text_height = 0
        self.margin = menu_dict["Margin"]
        self.item_count = len(menu_dict["MenuItems"])
        self.items = []

        # need these data items to calculate the x position of menu items
        self.max_text_width = 0  # Maximum width of all text
        self.cursor_width = 0    # Width of the cursor character (if any)
        self.title_start_y = 0   # y of where to start calculating title position
        self.text_start_y = 0    # y of where to start calculating menu items position

        self.title_border_rect = None
        self.items_border_rect = None
        self.title_rect = None
        self.items_rect = []

        # get all the menu information (fonts and stuff)
        self.render_menu_text(menu_dict)    # render the text
        self.create_menu_rects(menu_dict)   # build pygame.Rect for all the pieces

    def validate(self, menu_dict):
        ''' check for the existance of necessary values '''

        def error(str):
            print(str)
            pygame.quit()
            sys.exit()

        if "MenuTitle" not in menu_dict:
            error("MenuTitle missing")
        if "MenuItems" not in menu_dict or len(menu_dict["MenuItems"]) < 2:
            error("MenuItems not found or too few")
        if "FontNames" not in menu_dict or len(menu_dict["FontNames"]) < 2:
            error("FontNames not found or too few")
        if "Fonts" not in menu_dict or len(menu_dict["Fonts"]) < 2:
            error("no Fonts were built or not enought of them")
        if "Colors" not in menu_dict or len(menu_dict["Colors"]) < 2:
            error("Colors not found or too few")
        if "Margin" not in menu_dict or type(menu_dict["Margin"]) is not int:
            error("Margin missing or not an integer")
        if "YTop" not in menu_dict or type(menu_dict["YTop"]) is not int:
            error("YTop missing or not an integer")
        if "Border" not in menu_dict:
            menu_dict["Border"] = False
        if "Cursor" not in menu_dict:
            menu_dict["Cursor"] = False
        return menu_dict

    def render_menu_text(self, menu_dict):
        ''' get rendered text for title and items plus stuff to calculate where they go '''

        # render Title
        self.title_surf = self.menu_fonts[0].render(
            menu_dict["MenuTitle"], True, menu_dict["Colors"][0])
        self.max_text_width = self.title_surf.get_width()
        self.title_height = self.title_surf.get_height()

        # render Cursor
        if menu_dict["Cursor"]:
            self.cursor_surf = self.menu_fonts[1].render(
                menu_dict["Cursor"], True, menu_dict["Colors"][2])
            self.cursor_width = self.cursor_surf.get_width()
            self.cursor_height = self.cursor_surf.get_height()

        # render Menu Items and get max width
        for item in menu_dict["MenuItems"]:

            item_surf = self.menu_fonts[1].render(item, True, menu_dict["Colors"][1])
            self.max_text_width = item_surf.get_width() if self.max_text_width < item_surf.get_width() else self.max_text_width

            if not menu_dict["Cursor"]:
                item_surf1 = self.menu_fonts[1].render(item, True, menu_dict["Colors"][2])
                self.items.append([item_surf, item_surf1, None])
            else:
                self.items.append([item_surf, None])
                self.cursor_height = self.cursor_surf.get_height()

    def create_menu_rects(self, menu_dict):
        ''' Calculate position of all text and rectangles '''

        # calculate the top left x and y position for Border and non Border
        title_topleft_y = menu_dict["YTop"]
        title_topleft_x = self.mid_w - round((self.max_text_width - self.margin) / 2)
        if menu_dict["Cursor"]:
            title_width = self.max_text_width - (self.margin * 2)
        else:
            title_width = self.cursor_width + self.max_text_width - (self.margin * 3)
        title_height = self.title_height + (self.margin * 2)

        text_topleft_y = menu_dict["YTop"] + self.title_height + (self.margin * 2)
        text_topleft_x = self.mid_w - round((self.max_text_width - self.margin) / 2)
        if menu_dict["Cursor"]:
            text_width = self.max_text_width - (self.margin * 2)
        else:
            text_width = self.cursor_width + self.max_text_width - (self.margin * 3)
        text_height = self.margin + ((self.text_height + self.margin) * self.item_count)

        self.title_border_rect = pygame.Rect(
            [title_topleft_x, title_topleft_y, title_width, title_height])
        self.items_border_rect = pygame.Rect(
            [text_topleft_x, text_topleft_y, text_width, text_height])

        # Now we do the text positioning
        #
        #   Title text rect
        title_topleft_x = self.mid_w - round(self.title_surf.get_width() / 2)
        title_topleft_y = menu_dict["YTop"] + self.margin
        title_width = self.title_surf.get_width()
        title_height = self.title_surf.get_height()
        self.title_rect = pygame.Rect([title_topleft_x, title_topleft_y, title_width, title_height])

        # set text_top_y
        text_y = text_topleft_y + self.margin
        # place the menu selection items
        for sel, items_surf in enumerate(self.items):
            if menu_dict["Cursor"]:
                # Position items with cursor
                x = text_topleft_x + self.margin
                y = text_y + ((self.text_height + self.margin) * sel)
                self.items_rect.append(
                    [items_surf[0].get_rect(topleft=(x + self.margin + self.cursor_width, y)),
                     self.cursor_surf.get_rect(topleft=(x, y))])
            else:
                # position items without cursor
                x = self.mid_w - round(items_surf[0].get_width() / 2)
                y = text_y + ((self.text_height + self.margin) * sel)
                self.items_rect.append([items_surf[0].get_rect(midtop=(x, y))])

    def get_event(self, event):
        ''' process the up/down events '''
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.current_item -= 1
            if event.key == pygame.K_DOWN:
                self.current_item += 1

        self.current_item = self.current_item % len(self.items)

    def update(self, dt):
        ''' process results of the get_event changes '''
        pass

    def draw(self, surface):
        ''' Draw the menu '''
        surface.fill(pygame.Color("gray20"))
        if self.menu_dict["Border"]:
            pygame.draw.rect(surface, "white", self.title_border_rect, 2)
            pygame.draw.rect(surface, "white", self.items_border_rect, 2)

        # put title on the screen
        surface.blit(self.title_surf, self.title_rect)

        for sel, item_surf in enumerate(self.items):
            if self.menu_dict["Cursor"]:
                surface.blit(item_surf[0], self.items_rect[sel][0])
                if sel == self.current_item:
                    surface.blit(self.cursor_surf, self.items_rect[sel][1])
            else:
                if sel != self.current_item:
                    surface.blit(item_surf[0], self.items_rect[sel][0])
                else:
                    surface.blit(item_surf[1], self.items_rect[sel][0])

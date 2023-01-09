import pygame


class MenuEngine():
    def __init__(self, screen, menu_dict):

        # Get and/or validate parameter data
        self.screen = screen
        self.menu_dict = menu_dict.copy()
        self.validate()  # validate the self.menu_dict

        # Not sure just how much having this data helps
        self.mid_w = round(screen.get_rect().width / 2)
        self.mid_h = round(screen.get_rect().height / 2)
        self.current_item = 0
        self.menu_fonts = self.menu_dict["Fonts"]

        # need these data items to calculate the y position of menu items
        self.title_height = 0
        self.margin = self.menu_dict["Margin"]
        self.item_count = len(self.menu_dict["MenuItems"])
        self.item_surfs = []

        # Maximum width of all text; title and selection items
        self.max_text_width = 0

        # this will contain the items surfaces (color 1 and color 2) and rects
        self.items_draw = []

        # get all the menu information (fonts and stuff)
        self.render_menu_text()    # render the text
        # build pygame.Rect for all the pieces
        self.create_items_rect()
        # work out the offsets for positioning and justification and move everything to match
        self.do_justify()

    def validate(self):
        ''' check for the existance and correctness of necessary input values...
            asserts... lots and lots of asserts.  Sigh.
        '''

        # Minimum number of definitions that absolutely must be there
        assert ("MenuTitle" in self.menu_dict), "The Menu Title is missing"
        assert ("MenuItems" in self.menu_dict), "Menu selection items are missing"
        assert ("Fonts" in self.menu_dict), "Text Fonts are missing"
        assert ("Colors" in self.menu_dict), "Text Colors are missing"

        # validate the Menu Title
        assert (type(self.menu_dict["MenuTitle"]) is str) and \
            (len(self.menu_dict["MenuTitle"]) > 0), \
            "MenuTitle must be a non zero length string"

        # validate the menu selection items
        assert (type(self.menu_dict["MenuItems"])
                is list), "MenuItems must be an array of strings"
        assert (len(self.menu_dict["MenuItems"]) >
                2), "Menu Items must have more then 2 string"
        for item in self.menu_dict["MenuItems"]:
            if type(item) is not str:
                raise TypeError(f"MenuItems {item} is not a string")

        # validate the list of pygame fonts
        assert (type(self.menu_dict["Fonts"])
                is list), "Fonts must be a list of fonts"
        if len(self.menu_dict["Fonts"]) == 2:
            self.menu_dict["Fonts"].append(self.menu_dict["Fonts"][-1])
        assert (len(self.menu_dict["Fonts"]) > 1), "Must be then 2 fonts"
        for item in self.menu_dict["Fonts"]:
            if type(item) is not pygame.font.Font:
                raise TypeError("One of the Fonts isn't")

        # convert all items to pygame.Color type which will validate the colors automatically
        assert (type(self.menu_dict["Colors"])
                is list), "Colors must be a list of fonts"
        assert (len(self.menu_dict["Colors"]) == 3), "There must be 3 colors"
        for x, item in enumerate(self.menu_dict["Colors"]):
            if type(item) is not pygame.Color:
                self.menu_dict["Colors"][x] = pygame.Color(
                    self.menu_dict["Colors"][x])

        # validate margin. If missing then default is 15 pixels
        if "Margin" not in self.menu_dict:
            self.menu_dict["Margin"] = 15
        assert (type(self.menu_dict["Margin"])
                is int), "Margin must be an integer"

        # validate cursor.  If not there then defalut to false
        if "Cursor" not in self.menu_dict:
            self.menu_dict["Cursor"] = False
        assert (type(self.menu_dict["Cursor"]) in [
                bool, str]), "Cursor invalid type"

        # validate menu topleft. Must be a tuple of 2 integers
        assert ("TopLeft" in self.menu_dict), "TopLeft not defined"
        assert (type(self.menu_dict["TopLeft"]) is tuple), \
            "TopLeft must be a tuple of 2 integers"
        assert (len(self.menu_dict["TopLeft"]) == 2) and \
               (type(self.menu_dict["TopLeft"][0]) is int) and \
               (type(self.menu_dict["TopLeft"][1])
                is int), "Tuple can contain only 2 integers"

        # if complete TopLeft then Justify isn't needed, force to empty string
        if (self.menu_dict["TopLeft"][0] > 0 and "Justify" in self.menu_dict) or \
                "Justify" not in self.menu_dict:
            self.menu_dict["Justify"] = ""
        assert (type(self.menu_dict["Justify"])
                is str), "Justify must be a string"
        assert (self.menu_dict["Justify"] in ['left', 'right', 'center', '']
                ), "Justify string must be left, right, or center"

        # Border must be boolean, if missing default to False.
        if "Border" not in self.menu_dict:
            self.menu_dict["Border"] = False
        assert (type(self.menu_dict["Border"])
                is bool), "Border is boolean (True, False  Only)"

    def render_menu_text(self):
        ''' Rendered text for title and items, and get height/width stats '''

        # render Title
        self.title_surf = self.menu_fonts[0].render(
            self.menu_dict["MenuTitle"], True, self.menu_dict["Colors"][0])
        self.max_text_width = self.title_surf.get_width()
        self.title_height = self.title_surf.get_height()

        # render Cursor and stor in self.menu_dict - Rect and positioning is done later
        if self.menu_dict["Cursor"]:
            cursor_surf = self.menu_fonts[1].render(
                self.menu_dict["Cursor"], True, self.menu_dict["Colors"][2])
            self.menu_dict["Cursor"] = [cursor_surf,
                                        cursor_surf.get_width(),
                                        cursor_surf.get_height()]

        # render Menu Items and get max width
        for item in self.menu_dict["MenuItems"]:
            item_surf = self.menu_fonts[1].render(
                item, True, self.menu_dict["Colors"][1])
            item_surf_s = self.menu_fonts[1].render(
                item, True, self.menu_dict["Colors"][2])
            self.item_surfs.append([item_surf, item_surf_s])

            self.max_text_width = \
                item_surf.get_width() if self.max_text_width < item_surf.get_width() \
                else self.max_text_width

    def create_items_rect(self):
        '''
            Calculate position of all text and rectangles and populate the
            self.menu_dict dictionary with the various [surfaces, rectangles]
            to draw
        '''

        # start all calculations from (1, 1).  I've honestly no idea
        #   why I chose (1, 1) rather then (0, 0).  I'm pretty sure that was
        #   at one time, a reason.
        # we'll move_ip them when we have enough data to deal
        # the complexities of Justify
        menu_topleft = (1, 1)

        # calculate selection items start
        menu_text_topleft = (1, (1 + (self.margin * 2) + self.title_height))

        # calculate menu total width... this is the maximum text width plus margins
        # plus cursor text width (if aay)
        menu_width = menu_topleft[0] + ((self.margin * 2) + self.max_text_width)
        if self.menu_dict["Cursor"]:  # add cursor and another margin to the nmenu_width
            menu_width = menu_width + (self.margin + self.menu_dict["Cursor"][1])
        self.menu_width = menu_width

        # topleft position title text (title text is always centered)
        # self.menu_dict["Menutitle"] will contain the surface and rectangle
        #   necessary to draw the menu title
        title_text_topleft = (
            menu_topleft[0] + round(menu_width / 2), menu_topleft[1] + self.margin)
        title_text_rect = self.title_surf.get_rect(midtop=title_text_topleft)
        self.menu_dict["MenuTitle"] = [self.title_surf, title_text_rect]

        # position first selection text
        # - if cursor then text starts 1 margin in and 1margin down
        # - If no cursor, text is centered in the menu width
        if self.menu_dict["Cursor"]:
            item_text_topleft = (menu_text_topleft[0] + self.margin,
                                 menu_text_topleft[1] + self.margin)
            self.cursor_offset = -(self.margin + self.menu_dict["Cursor"][1])
        else:
            item_text_topleft = (menu_text_topleft[0] + round(menu_width / 2),
                                 menu_text_topleft[1] + self.margin)

        # Loop through items and place them same logic as item_text_topleft with margin offset
        for sel, item_surf in enumerate(self.item_surfs):
            pos_x = item_text_topleft[0]
            pos_y = item_text_topleft[1] + \
                ((self.margin + item_surf[0].get_height()) * sel)
            if self.menu_dict["Cursor"]:
                pos_x = pos_x + self.menu_dict["Cursor"][1] + self.margin
                item_rect = item_surf[0].get_rect(topleft=(pos_x, pos_y))
            else:
                item_rect = item_surf[0].get_rect(midtop=(pos_x, pos_y))
            self.items_draw.append([item_surf[0], item_surf[1], item_rect])

        # find bottom y coordinate
        bottom_y = self.items_draw[-1][2][1] + self.items_draw[-1][2][3] + self.margin

        # rect = left, top, width, height
        self.title_border_rect = pygame.Rect(menu_topleft[0],
                                             menu_topleft[1],
                                             menu_width,
                                             (self.margin * 2) + self.title_height)
        self.items_border_rect = pygame.Rect(item_text_topleft[0] - self.margin,
                                             item_text_topleft[1] - self.margin,
                                             menu_width,
                                             bottom_y)

    def do_justify(self):
        if self.menu_dict["Justify"] == "center":
            move_x = round(self.screen.get_rect().width / 2) - round(self.menu_width / 2)
            move_y = self.menu_dict["TopLeft"][1]
        elif self.menu_dict["Justify"] == "left":
            move_x = self.menu_dict["TopLeft"][0]
            move_y = self.menu_dict["TopLeft"][1]
        elif self.menu_dict["Justify"] == "right":
            move_x = self.screen.get_rect().width - self.menu_width
            move_y = self.menu_dict["TopLeft"][1]
        else:
            move_x = self.menu_dict["TopLeft"][0]
            move_y = self.menu_dict["TopLeft"][1]

        # start moving all of the pieces (boxes, menu title, and selection items)
        self.title_border_rect.move_ip(move_x, move_y)
        self.items_border_rect.move_ip(move_x, move_y)
        self.menu_dict["MenuTitle"][1].move_ip(move_x, move_y)
        for item in self.items_draw: item[2].move_ip(move_x, move_y)

    def get_event(self, event):
        '''
            I've no idea how you might wish use this as events
            are generally handled by whatever creates the MenuEngine
            instance and only self.current_item is used to facilitate
            drawing (see 'draw' below).
        '''
        pass

    def update(self, dt):
        '''
            Process any results of the get_event changes.  Again, I've no
            idea how you might wish to use this but it's here for you.
        '''
        pass

    def draw(self, surface):
        ''' Draw the menu '''
        surface.fill(pygame.Color("gray20"))
        if self.menu_dict["Border"]:
            pygame.draw.rect(surface, "white", self.title_border_rect, 2)
            pygame.draw.rect(surface, "white", self.items_border_rect, 2)

        surface.blit(self.menu_dict["MenuTitle"][0], self.menu_dict["MenuTitle"][1])

        for sel, item in enumerate(self.items_draw):
            if (sel == self.current_item):
                if self.menu_dict["Cursor"]:
                    surface.blit(item[0], item[2])
                    surface.blit(self.menu_dict["Cursor"][0], item[2].move(
                        self.cursor_offset, -3))
                else:
                    surface.blit(item[1], item[2])
            else:
                surface.blit(item[0], item[2])

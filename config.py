'''
    This is where you put all the stuff that defines the various
    parameters and constants for your game.
'''

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600

asset_dict = {
    "titlefont": ['f', "fonts/StarcruiserExpandedSemiItalic-gKeY.ttf", 50],
    "subtitlefont": ['f', "fonts/FleshWound.ttf", 40],
    "sysfont60": ['fs', None, 60],
    "sysfont50": ['fs', None, 50],
    "comicsans65": ['fs', "comicsans", 65],
    "comicsans25": ['fs', "comicsans", 25],
    "comicsans20": ['fs', "comicsans", 20],
}

main_menu_dict = {
    "MenuTitle": "Game Menu",
    "MenuItems": ["Start the Game", "Adjust Sound", "Show Credits", "Quit Game"],
    "MenuStates": ["GAMEPLAY", "SOUND", "CREDITS", "QUIT"],
    "Cursor": "=>",
    "FontNames": ["titlefont", "sysfont50", "sysfont50"],
    "Fonts": [],
    "Colors": ["blue", "white", "red"],
    "Margin": 10,
    "Border": True,
    "TopLeft": (0, 100),
    "Justify": "center",
}

sound_menu_dict = {
    "MenuTitle": "Sound Control Menu",
    "MenuItems": ["Theme Volume", "Effects volume", "Back", "Quit Game"],
    "MenuStates": ["TVOLUME", "EVOLUME", "MENU", "SPLASH"],
    "FontNames": ["titlefont", "sysfont50", "sysfont50"],
    "Fonts": [],
    "Colors": ["blue", "white", "red"],
    "Margin": 20,
    "Border": True,
    "TopLeft": (0, 100),
    "Justify": "center"
}

'''
        Author: Carl Franz
        Name: Pygame Assets
        Date: 02/09/2022
        License: use it, don't use it, whatever

    A method to collect and load all of your pygame assets at once.  I needed
    this for a game I was re-writing and so I generalized it.  You define your
    program/pygame assets in a python dictionary and create an instance of the
    class.  You can then retrieve any asset by the name you gave it in the
    asset dictionary.

    This process will read a dictionary of assets formated as:
    {asset name : (asset type, asset file, font size]), ...}
    where:
        asset name : string - is whatever name you wish to reference it by
        asset type : string - 'i': image, 'f': font, 'fs': SysFont,
                              's': sound, maybe 'a': anamation if I get that sorted
        asset file : path to the asset including file name
        font size  : if the asset is a font (or SysFont), the font size must be provided

    At some point I'm going to deal with animation in this... later.

'''
import pygame


class AssetMachine():
    """
    Takes a dictionary of game assets and gathers them as self.assets.

    Attributes
    ----------
    assetdict : dictionary
        your assets, what kind and where they are.
        {asset name : (asset type, asset file (, font size)), ...}

    Methods
    -------
    retrieve_asset(name)
        provide the asset name you assigned originally
        return: the asset as pygame likes it
    render(name, string, color)
        will render the string from font dictionary item 'name'.
        this is kind of experimental to see if it's useful...
        return: returns a surface with the rendered string ready to blit
    """

    def __init__(self, assetdict):
        self.assets = {}
        for item_name, item in assetdict.items():
            # Yes, this could have been done with the 'match case' but I've
            # found a lot of people with Raspian Unix have trouble getting
            # Python 3.10 going... Including me.
            if item[0] == 'i':  # load image
                self.assets[item_name] = [item[0], pygame.image.load(
                    item[1]).convert_alpha()]
            elif item[0] == 'f':  # load font
                self.assets[item_name] = [item[0], pygame.font.Font(
                    item[1], int(item[2]))]
            elif item[0] == 'fs':  # load sysfont
                self.assets[item_name] = [item[0], pygame.font.SysFont(
                    item[1], int(item[2]))]
            elif item[0] == 's':  # load audio
                self.assets[item_name] = [item[0], pygame.mixer.Sound(item[1])]
            else:
                # this should be an exception, maybe next time
                # currently I just put out a message and ignore
                print(f'bad asset load type: {item[0]} - item: {item[1]}')

    def retrieve_asset(self, assetname):
        ''' Input: the asset name...
            returns: the asset
        '''
        return self.assets[assetname][1]

    def render(self, assetname, rstring, color):
        ''' This one is merely for convenience because... why not.
            Input: the asset (font) name
                    string to render
                    color
            returns: a rendered string ready to blit
        '''
        return self.retrieve_asset(assetname).render(rstring, True, color)

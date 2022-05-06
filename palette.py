from dataclasses import dataclass
import numpy as np

def interpolate_color(c1, c2, r):
    """Interpolate between two arrays. Clamps r to [0,1]

    :param c1: Minimum value (when r=0)
    :type c1: np.ndarray
    :param c2: _description_
    :type c2: Minimum value (when r=1)
    :param r: _description_
    :type r: Coefficient of interpolation.
    :return: Interpolation between c1 and c2.
    :rtype: np.ndarray
    """
    r = max(0, min(1, r))
    return np.array(c1) * (1-r) + np.array(c2) * r

# from https://lospec.com/palette-list/sweetie-16
s16_raw = np.array([
    (26,  28,  44),
    (93,  39,  93),
    (177, 62,  83),
    (239, 125, 87),
    (255, 205, 117),
    (167, 240, 112),
    (56,  183, 100),
    (37,  113, 121),
    (41,  54,  111),
    (59,  93,  201),
    (65,  166, 246),
    (115, 239, 247),
    (244, 244, 244),
    (148, 176, 194),
    (86,  108, 134),
    (51,  60,  87)
])

@dataclass
class S16:
    '''
    Informal names for the 16 colors
    in GrafxKid's SWEETIE16 palette.
    '''
    black  = np.array((26,  28,  44, 255))
    purple = np.array((93,  39,  93, 255))
    red    = np.array((177, 62,  83, 255))
    orange = np.array((239, 125, 87, 255))
    yellow = np.array((255, 205, 117, 255))
    lime   = np.array((167, 240, 112, 255))
    green  = np.array((56,  183, 100, 255))
    teal   = np.array((37,  113, 121, 255))
    navy   = np.array((41,  54,  111, 255))
    blue   = np.array((59,  93,  201, 255))
    cerulean = np.array((65,  166, 246, 255))
    cyan = np.array((115, 239, 247, 255))
    livid_darkest = np.array((51,  60,  87, 255))
    livid_dark    = np.array((86,  108, 134, 255))
    livid_light   = np.array((148, 176, 194, 255))
    white  = np.array((244, 244, 244, 255))

    # livid is a grey-blue
    # black and white


BLACK   = np.array([0,     0,   0])
WHITE   = np.array([255, 255, 255])
RED     = np.array([255,   0,   0])
GREEN   = np.array([0,   255,   0])
BLUE    = np.array([0,     0, 255])
CYAN    = np.array([0,   255, 255])
YELLOW  = np.array([255, 255,   0])
MAGENTA = np.array([255,   0, 255])


''' full palette
(26,  28,  44)
(93,  39,  93)
(177, 62,  83)
(239, 125, 87)
(255, 205, 117)
(167, 240, 112)
(56,  183, 100)
(37,  113, 121)
(41,  54,  111)
(59,  93,  201)
(65,  166, 246)
(115, 239, 247)
(244, 244, 244)
(148, 176, 194)
(86,  108, 134)
(51,  60,  87)
'''
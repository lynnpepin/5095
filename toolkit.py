import numpy as np
import pygame
from palette import interpolate_color, S16

def polar_to_xy(r: float, theta: float = 0):
    """Convert polar coordinates in (r, theta) to cartesian (x, y).

    Here +x is right (0rad) and +y is up (pi/2 rad)

    :param r: Radius
    :type r: float
    :param theta: Angle, default 0
    :type theta: float
    :return: Cartesian x, y coordinates.
    :rtype: tuple[float, float]
    """
    return (r*np.cos(theta), r*np.sin(theta))

class Node:
    def __init__(
        self,
        x = 0,
        y = 0,
        hist_length = 20,
        screen = None,
    ):      
        # X[0] = current position
        self.hist_length = 20
        self.X = [x for _ in range(hist_length)]
        self.Y = [y for _ in range(hist_length)]
        self.screen = screen

    def update(self, x = 0, y = 0):
        # remove the last element of each list
        self.X.pop()
        self.Y.pop()
        # add the new element
        self.X.insert(0, x)
        self.Y.insert(0, y)
    
    def draw(self, screen = None, tail: bool = True):
        if screen is None:
            screen = self.screen
        
        assert self.hist_length == len(self.X) == len(self.Y)

        # draw tail
        if tail:
            for ii in range(self.hist_length - 1):
                alpha = (ii + 1) / self.hist_length
                color = interpolate_color(S16.white, S16.livid_darkest, alpha)
                pygame.draw.line(
                    screen,
                    color,
                    (self.X[ii], self.Y[ii]),
                    (self.X[ii + 1], self.Y[ii + 1]),
                    width = 2
                )
        
        # draw self
        pygame.draw.circle(
            screen, S16.white, center=(self.X[0], self.Y[0]), radius=2
        )



class Swarm:
    def __init__(
        self,
        N: int = 20,
        get_radius = lambda: np.random.normal(100, 10),
        get_theta  = lambda: np.random.uniform(0, 2*np.pi),
        hist_length = 20,
        screen = None
    ):

        self._get_radius = get_radius
        self._get_theta = get_theta
        self.hist_length = hist_length
        self.screen = screen

        # Instantiate nodes
        self.nodes = []
        for _ in range(N):
            x, y = polar_to_xy(
                r = self._get_radius(),
                theta = self._get_radius()
            )
            new_node = Node(x=x, y=y, hist_length=hist_length)
            self.nodes.append(new_node)

    def update(self):
        pass

    def draw(self, screen = None, tail: bool = True):
        if screen is None:
            screen = self.screen
        
        for node in self.nodes:
            node.draw(screen, tail=tail)
import math
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

def center_origin(coord, width=360, height=360):
    """Transform an (x,y) coordinate so (0,0) is centered
    according to width, height.

    E.g. center_origin((100,50), 400, 300) = (300,200)

    :param coord: Tuple of (x,y)
    :type coord: Tuple[float, float]
    :param width: Width of screen, defaults to 360
    :type width: int, optional
    :param height: Width of screen, defaults to 360
    :type height: int, optional
    :return: _description_
    :rtype: _type_
    """
    return (coord[0] + width/2, coord[1] + width/2)

class Node:
    def __init__(
        self,
        x = 0,
        y = 0,
        hist_length = 20,
        screen = None,
    ):      
        # X[0] = current position
        self.hist_length = hist_length
        self.X = [x for _ in range(hist_length)]
        self.Y = [y for _ in range(hist_length)]
        self.screen = screen

    def update(self, x = 0, y = 0, dt = 1/60):
        # remove the last element of each list
        self.X.pop()
        self.Y.pop()
        # add the new element
        self.X.insert(0, x)
        self.Y.insert(0, y)
    
    def draw_tail(self, screen = None, transform = lambda x: x):
        if screen is None:
            screen = self.screen
        
        assert self.hist_length == len(self.X) == len(self.Y)

        # draw tail
        for ii in range(self.hist_length - 1):
            alpha = (ii + 1) / self.hist_length
            color = interpolate_color(S16.white, S16.livid_darkest, alpha)
            pygame.draw.line(
                screen,
                color,
                transform((self.X[ii], self.Y[ii])),
                transform((self.X[ii + 1], self.Y[ii + 1])),
                width = 2
            )
    
    def draw(self, screen = None, transform = lambda x: x):
        if screen is None:
            screen = self.screen
        
        pygame.draw.circle(
            screen,
            S16.white,
            center = transform((self.X[0], self.Y[0])),
            radius = 2
        )



class Swarm:
    def __init__(
        self,
        N: int = 20,
        get_radius = lambda: np.random.normal(200, 30),
        get_theta  = lambda: np.random.uniform(0, 2*np.pi),
        hist_length = 40,
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

    def update(self,
        dt = 1/60,
        noise = lambda: np.random.normal(0, 30),
        drdt = lambda r: (100 - r)/100 + (3/2)*np.cos(r*np.pi/3),
        dthetadt = lambda r: (20000 / r**2)
        ):
        # todo: redefine update on x, y as entirely functional
        for node in self.nodes:
            x, y = node.X[0], node.Y[0]
            # convert to polar
            # (todo -- should this be taken from node directly?)
            r = (x**2 + y**2)**.5
            theta = math.atan2(y, x)

            # differential equations defining motion
            dr = drdt(r) * dt
            dtheta = dthetadt(r) * dt

            # test
            #print(r, theta, dr, dtheta)

            # apply dr, dtheta to r, theta
            r += dr + noise() * dt
            theta += dtheta

            # and now update each node
            x, y = polar_to_xy(r, theta)
            #x += noise()
            #y += noise()
            node.update(x, y, dt)

    def draw(self, screen = None, tail: bool = True, transform = lambda x: x):
        if screen is None:
            screen = self.screen
        
        # draw tails before nodes
        if tail:
            for node in self.nodes:
                node.draw_tail(screen, transform)
            
        for node in self.nodes:
            node.draw(screen, transform)

def spectrum(
    x,
    y,
    m
):
    '''
    Given x in (n), y in (n), bool m in (n,k),
    compute matrix d(n,n)

    TODO: Come back tomorrow!

>>> for k in range(4):
...   for i in range(3):
...     if ((I[i,:,k] / Ir[i,k]) >= 0.5).any():
...       print(i,k, (I[i,:,k] / Ir[i,k]))
i k 
0 0 [0. 1. 0.]
1 0 [1. 0. 0.]
2 0 [0.47213595 0.52786405 0.        ]
0 2 [0. 0. 1.]
1 2 [0. 0. 1.]

    Here, 0 and 1 hear eachother on k=0,
    2 hears only 1 on k=0,
    and 0 and 1 both hear node 2 on k=2.

    From here:
        - Meaningful metrics? (Throughput? Etc)
        - Implement this
        - Make nodes send messages

    '''

    # 1. Take xs and ys, compute pairwise d[i, k] in (N,N)
    # 2. Take ms and construct m[i, k] in (N,K)
    # 3. Create I = np.einsum('ij,jk->ijk', dd, m) in (N, N, K)
    #    Ir= I_ijk.sum(axis=1)
    # E.g. Node 2 sees from 0 on channel k I[2,0,0]
    #    compare as I[2,0,0] / Ir[2,0] to get ratio

    # record successes
    # send destruction deets to i and j so they can respond


# import numpy as np; d = np.array([[0,3,4],[3,0,5],[4,5,0]]); m = np.array([[1,0,0,0],[1,0,0,0],[0,0,1,0]]); dd = d**.5; I = np.einsum('ij,jk->ijk', dd, m); Ir = I.sum(axis=1)


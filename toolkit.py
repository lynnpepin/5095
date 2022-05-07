import math
import numpy as np
import pygame
from palette import interpolate_color, S16
from typing import List, Tuple

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
        """
        A single particle that moves in the system

        :param x: Initial x-coordinate, defaults to 0
        :type x: int, optional
        :param y: Initial y-coordinate, defaults to 0
        :type y: int, optional
        :param hist_length: Position history, used for drawing tail, defaults to 20
        :type hist_length: int, optional
        :param screen: Display to draw to, defaults to None
        :type screen: pygame.Surface, optional
        """
        # X[0] = current position
        self.hist_length = hist_length
        self.X = [x for _ in range(hist_length)]
        self.Y = [y for _ in range(hist_length)]
        self.screen = screen

    def update(self, x: int = 0, y: int = 0, dt = 1/60):
        """Set a new x,y and update the history.

        :param x: New x coordinate, defaults to 0
        :type x: int, optional
        :param y: New y coordinate, defaults to 0
        :type y: int, optional
        :param dt: Dt, unused, defaults to 1/60
        :type dt: float, optional
        """
        # remove the last element of each list
        self.X.pop()
        self.Y.pop()
        # add the new element
        self.X.insert(0, x)
        self.Y.insert(0, y)
    
    def draw_tail(self, screen = None, transform = lambda x: x):
        """Draw the tail following the node

        :param screen: Pygame display, defaults to None
        :type screen: pygame.Surface, optional
        :param transform: Function to apply to (x,y) coordinate,
            e.g. to reposition to center. Defaults to lambdax:x

        :type transform: _type_, optional
        """
        if screen is None:
            screen = self.screen
        
        assert self.hist_length == len(self.X) == len(self.Y)

        # draw tail
        for ii in range(self.hist_length - 1):
            alpha = (ii + 1) / self.hist_length
            color = interpolate_color(S16.cyan, S16.livid_darkest, alpha)
            # Quick fix: The line made the nodes look a certain way.
            # Let's change that here...
            '''
            pygame.draw.line(
                screen,
                color,
                transform((self.X[ii], self.Y[ii])),
                transform((self.X[ii + 1], self.Y[ii + 1])),
                width = 2
            )
            '''
            pygame.draw.circle(
                screen,
                color,
                transform((self.X[ii], self.Y[ii])),
                radius = 2 + (ii // 6) # cheap quick hack; dependent on dt!
            )

    
    def draw(self, screen = None, transform = lambda x: x):
        """Draw the node as a circle

        :param screen: Pygame display, defaults to None
        :type screen: pygame.Surface, optional
        :param transform: Function to apply to (x,y) coordinate,
            e.g. to reposition to center. Defaults to lambdax:x

        :type transform: _type_, optional
        """
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
        get_radius = lambda: np.random.normal(200, 30),
        N: int = 0,
        get_theta  = lambda: np.random.uniform(0, 2*np.pi),
        hist_length = 40,
        screen = None
    ):
        """A collection of N nodes.

        :param N: Number of nodes, defaults to 20
        :type N: int, optional
        :param get_radius: Function to choose radius to initialize nodes on,
            defaults to lambda:np.random.normal(200, 30)
        :type get_radius: function, optional
        :param get_theta: Function to choose angle to initialize nodes on,
            defaults to lambda:np.random.uniform(0, 2*np.pi)
        :type get_theta: _type_, optional
        :param hist_length: Number of coordinates to store per node, defaults to 40
        :type hist_length: int, optional
        :param screen: Display to draw to, defaults to None
        :type screen: pygame.Surface, optional
        """

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

    def update(
        self,
        dt = 1/60,
        drdt = lambda r: (100 - r)/100 + (3/2)*np.cos(r*np.pi/3) + np.random.normal(0, 30),
        dthetadt = lambda r: (20000 / r**2)
    ):
        """Update the positions of the nodes according to
        dr and dtheta series of differential equations

        drdt and dthetadt are functions

        :param dt: Timestep, defaults to 1/60
        :type dt: float, optional
        :param drdt: Function that updates r; defaults per paper
        :type drdt: Function, optional
        :param dthetadt: Function that updates theta, defaults per paper
        :type dthetadt: Function, optional
        """
        # todo: redefine update on x, y as entirely functional
        for node in self.nodes:
            x, y = node.X[0], node.Y[0]
            # convert to polar
            r = (x**2 + y**2)**.5
            theta = math.atan2(y, x)

            # differential equations defining motion
            r += drdt(r) * dt
            theta += dthetadt(r) * dt

            # and now update each node
            x, y = polar_to_xy(r, theta)
            node.update(x, y, dt)

    def draw(self, screen = None, tail: bool = True, transform = lambda x: x):
        """Draw all the nodes in the swarm to the screen.

        :param screen: PyGame surface, defaults to None
        :type screen: pygame.Surface, optional
        :param tail: Draw the node tails, defaults to True
        :type tail: bool, optional
        :param transform: Transform to apply to each pixel (x,y) coordinate, defaults to lambdax:x
        :type transform: Function, optional
        """
        if screen is None:
            screen = self.screen
        
        # draw tails before nodes
        if tail:
            for node in self.nodes:
                node.draw_tail(screen, transform)
        
        # draw nodes
        for node in self.nodes:
            node.draw(screen, transform)


def example_physical_simulation(
    coordinates: List[Tuple[float, float]],
    dt: float = 1/60,
    K: int = 10
):
    """Example physical-layer simulator as per the paper.

    Our assumptions and simplifications let us simulate
    the entire network in just one function, given only
    the x,y coordinates and metadata!

    :param coordinates: List of x, y coordinates
    :type coordinates: List[Tuple[float, float], ...]
    :param dt: Timestep, defaults to 1/60
    :type dt: float, optional
    :param K: Number of channels, defaults to 10
    :type K: int, optional

    :returns: Total messages sent, total messages received,
        plus matrices M, A, and Ar (for experimentation).
    """
    # N = number of nodes
    N = len(coordinates)

    # 1. create D
    D = np.zeros((N, N))
    for ii in range(N):
        xi, yi = coordinates[ii]
        for jj in range(N):
            xj, yj = coordinates[jj]
            # distance^-2 = (Dx^2 + Dy^2)^.5^-2
            if ii == jj:
                D[ii,ii] = 0
            else:
                D[ii,jj] = ((xi - xj)**2 + (yi - yj)**2)**-1
        
        # zero out the diagonal
        

    # 2. Generate message matrix M according to paper
    # That is, each node creates a message on channel k with probability dt
    M = (np.random.random((N, K)) < dt).astype(int)
    
    # 3. Calculate A' and A
    Ar = D @ M 
    A = np.einsum('ij,jk->ijk',D,M) # Loudness per node-pair per message

    # 4. Calculate metrics
    total_messages_sent = np.sum(M)
    total_message_received = 0
    
    # this can probably be vectorized
    for ii in range(N):
      for jj in range(N):
        for kk in range(K):
          if Ar[ii, kk] != 0 and A[ii,jj,kk] / Ar[ii, kk] > 1/2:
            total_message_received += 1
    
    return total_messages_sent, total_message_received, M, D, A, Ar


def draw_M(
    M,
    screen,
    corner = (0.0,0.0),
    width = 3.0,
    border = 1.0,
    C1 = S16.lime,
    C2 = S16.black
):
    """Draw a summary of the messages being sent by M.

    :param M: message matrix
    :type M: np.ndarray
    :param screen: PyGame screen
    :type screen: pygame.Surface
    :param corner: Top-left corner to draw, defaults to (0.0,0.0)
    :type corner: tuple, optional
    :param width: Width of each block, defaults to 3.0
    :type width: float, optional
    :param border: Border between blocks, defaults to 1.0
    :type border: int, optional
    :param alpha: Degradation of the previous-M rendering, defaults to 0.9
    :type alpha: float, optional
    :param C1: Main color, defaults to S16.lime
    :type C1: np.ndarray or Tuple
    :param C2: Background color, defaults to S16.black
    :type C2: np.ndarray or Tuple
    """

    N, K = M.shape
    for ii in range(N):
        for kk in range(K):
            color = interpolate_color(C1, C2, 1 - M[ii,kk])
            #rect = pygame.Rect(
            #    left   = corner[0] + (width+border)*ii,
            #    top    = corner[1] + (width+border)*kk,
            #    width  = width,
            #    height = width
            #)

            pygame.draw.rect(
                surface = screen,
                color = color,
                rect = (
                    corner[0] + (width+border)*ii,
                    corner[1] + (width+border)*kk,
                    width,
                    width
                )
            )

def _normalize_safe(A):
    # quick helper function
    maxval = A.max()
    minval = A.min()
    if (maxval - minval) < 0.001:
        return A
    else:
        return (A - minval)/(maxval - minval)
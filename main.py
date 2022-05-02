"""
"""

import argparse
import math as mt
import os
import pickle
import random
import sys

import matplotlib
import numpy as np

import pygame

def polar_to_xy(r: float, theta: float):
    return (r*np.cos(theta), r*np.sin(theta))

class Node:
    def __init__(
        self,
        x = 0,
        y = 0,
        hist_length = 20
    ):      

        # X[0] = current position
        self.hist_length = 20
        self.X = [x for _ in range(hist_length)]
        self.Y = [y for _ in range(hist_length)]

    def update(self, x = 0, y = 0):
        # remove the last element of each list
        self.X.pop()
        self.Y.pop()
        # add the new element
        self.X.insert(0, x)
        self.Y.insert(0, y)

class Swarm:
    def __init__(
        self,
        N: int = 20,
        get_radius = lambda: np.random.normal(100, 10),
        get_theta  = lambda: np.random.uniform(0, 2*np.pi)
    ):
        print("hey")
        #nodes = [
        #    Node(


def main(width: int = 360, height: int = 360):
    # See https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
    pygame.init()
    pygame.display.set_caption("5095 go vroom")
    screen = pygame.display.set_mode((width,height))

    # Instantiate nodes

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                running = False



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--width","-scrw", 
        default=[360],
        help="Integer argument.",
        type=int, nargs=1
    )
    parser.add_argument(
        "--height","-scrh", 
        default=[360],
        help="Integer argument.",
        type=int, nargs=1
    )
    args = parser.parse_args()
    print(args.width[0], args.height[0])

    main(args.width[0], args.height[0])
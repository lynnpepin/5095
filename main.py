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

from toolkit import Node, Swarm, polar_to_xy

def main(width: int = 360, height: int = 360):
    # See https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
    pygame.init()
    pygame.display.set_caption("5390 go vroom")
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
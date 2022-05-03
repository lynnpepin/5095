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
from palette import S16, interpolate_color

def main(width: int = 360, height: int = 360, fps: int = 60):
    # See https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
    pygame.init()
    pygame.display.set_caption("5390 go vroom")
    screen = pygame.display.set_mode((width,height))
    dt = 1/fps
    clock = pygame.time.Clock()
    # dt is used in game logic. ideally is 1/fps

    swarm = Swarm(N = 20)

    # Main game logic loop    
    while True:
        screen.fill(S16.black)
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return 0
        
        # todo: render nodes
    
    # fixed dt = visual inconsistency but simulated consistency
    # setting dt as `dt = clock.tick(FPS)/1000` gives us the opposite
    clock.tick(FPS) 
    pygame.display.update()



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
    parser.add_argument(
        "--fps","-f", 
        default=[60],
        help="Frames per second (simulated and rendered)",
        type=int, nargs=1
    )
    args = parser.parse_args()

    main(args.width[0], args.height[0],  args.fps[0])
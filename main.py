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
from pygame import freetype

from toolkit import Node, Swarm, example_physical_simulation, polar_to_xy, center_origin, draw_M
from palette import S16, interpolate_color


def main(
    N: int = 40,
    K: int = 10,
    width: int = 360,
    height: int = 360,
    fps: int = 60,
    font_fn = "BitPotion.ttf"
):
    # See https://dr0id.bitbucket.io/legacy/pygame_tutorial00.html
    pygame.init()
    pygame.freetype.init()
    font = pygame.freetype.Font(font_fn, 16)
    # bitpotion font by https://joebrogers.itch.io/bitpotion

    pygame.display.set_caption("Particles")
    screen = pygame.display.set_mode((width,height))
    dt = 1/fps
    clock = pygame.time.Clock()
    # dt is used in game logic. ideally is 1/fps

    #### Start simulation
    swarm = Swarm(N=N, screen=screen, hist_length=60)
    M_to_draw = np.zeros((N,K))

    while True:
        screen.fill(S16.black)

        #### Handle controls
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return 0
        
        #### Handle physical simulation
        swarm.update()
        swarm.draw(
            screen,
            transform = lambda coord: center_origin(coord, width, height)
        )

        #### Handle network simulation
        coordinates = np.zeros((N,2))
        for ii in range(N):
            coordinates[ii] = (swarm.nodes[ii].X[0], swarm.nodes[ii].Y[0])
        
        tot_sent, tot_recv, M, _, _ = example_physical_simulation(coordinates, dt, K)

        #### Draw metadata
        # Draw M graph
        M_to_draw = np.clip(M + 0.9 * M_to_draw, 0, 1)
        draw_M(corner=(12, 24), M=M_to_draw, screen=screen)

        # Draw FPS
        #fps_text = font.render('abc', S16.white)
        #screen.blit(fps_text[0], (4,4))

        #### Update frames
        # fixed dt = visual inconsistency but simulated consistency
        # setting dt as `dt = clock.tick(FPS)/1000` gives us the opposite
        clock.tick(fps) 
        pygame.display.update()



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument(
        "--width","-scrw", 
        default=[600],
        help="Integer argument.",
        type=int, nargs=1
    )
    parser.add_argument(
        "--height","-scrh", 
        default=[600],
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

    main(width = args.width[0], height = args.height[0], fps = args.fps[0])
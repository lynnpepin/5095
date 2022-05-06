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

from toolkit import Node, Swarm, example_physical_simulation, polar_to_xy, center_origin, draw_M, _normalize_safe
from palette import S16, interpolate_color


def main(
    N: int = 40,
    K: int = 10,
    width: int = 360,
    height: int = 360,
    fps: int = 60,
    total_time: float = 120,
    font_fn = "BitPotion.ttf",
    simplify_render: bool = False,
    ratelimit: bool = True
):
    """Run the network experiment on the particle swarm.

    Generates N nodes talking over K channels,
    displays to a window of (width, height),
    with timestep defined by fps.

    :param N: Number of nodes, defaults to 40
    :type N: int, optional
    :param K: Number of channels, defaults to 10
    :type K: int, optional
    :param width: Display width, defaults to 360
    :type width: int, optional
    :param height: Display height, defaults to 360
    :type height: int, optional
    :param fps: Frames per second, controls dt timestep, defaults to 60
    :type fps: int, optional
    :param total_time: Total time (in seconds) to simulate, defaults to 120
    :type total_time: float, optional
    :param font_fn: Font to use for rendering on screen, defaults to "BitPotion.ttf"
    :type font_fn: str, optional
    :param simplify_render: Turn off tails and graphs, defaults to False
    :type simplify_render: bool, optional
    :param ratelimit: Slow the simulation rendering if it runs faster than the display, defaults to True
    :type ratelimit: bool, optional
    :return: Returns 0 on exit
    :rtype: int
    """
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
    swarm = Swarm(N=N, screen=screen, hist_length=int(1/(2*dt)))
    M_to_draw = np.zeros((N,K))
    Ar_to_draw = np.zeros((N,K))

    tt = 0
    while tt < total_time:
        screen.fill(S16.black)

        #### Handle controls
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                return 0
        
        #### Handle physical simulation
        swarm.update(dt=dt)
        swarm.draw(
            screen,
            transform = lambda coord: center_origin(coord, width, height),
            tail = not simplify_render
        )

        #### Handle network simulation
        coordinates = np.zeros((N,2))
        for ii in range(N):
            coordinates[ii] = (swarm.nodes[ii].X[0], swarm.nodes[ii].Y[0])
        
        tot_sent, tot_recv, M, D, _, Ar = example_physical_simulation(coordinates, dt, K)

        if not simplify_render:
            #### Draw metadata
            # Draw M and Ar here
            fps_text = font.render('M and A\' visualization', S16.lime)
            screen.blit(fps_text[0], (4,4))

            # Draw M graph
            M_to_draw = np.clip(M + (1-dt*6) * M_to_draw, 0, 1)
            draw_M(corner=(4, 16), M=M_to_draw.T, screen=screen, width=3)

            # Draw Ar graph
            Ar_to_draw = np.clip(
                _normalize_safe(Ar) + (1-dt*6) * Ar_to_draw,
                0, 1
            )
            draw_M(corner=(13 + K*4, 16), M=Ar_to_draw.T, screen=screen, width=3)

            # Draw D graph text
            D_corner=(width - N*3 - 4, height-N*3 - 4)
            fps_text = font.render('D visualization', S16.orange)
            screen.blit(fps_text[0], (D_corner[0], D_corner[1] - 16))

            # Draw D graph
            D = _normalize_safe(D)**(1/4)
            draw_M(
                corner=D_corner,
                M=D, screen=screen, width=3, border=0, C1=S16.orange
            )
        

        #### Update frames
        # fixed dt = visual inconsistency but simulated consistency
        # setting dt as `dt = clock.tick(FPS)/1000` gives us the opposite
        tt += dt
        if ratelimit:
            clock.tick(fps)
            
        pygame.display.update()
    return 0



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
        "--nodes","-n", 
        default=[40],
        help="Total number of nodes to simulate",
        type=int, nargs=1
    )
    parser.add_argument(
        "--channels","-k", 
        default=[10],
        help="Total number of channels to simulate",
        type=int, nargs=1
    )
    parser.add_argument(
        "--totaltime","-t", 
        default=[120],
        help="Total number of seconds to simulate",
        type=int, nargs=1
    )
    parser.add_argument(
        "--fps","-f", 
        default=[60],
        help="Frames per second (simulated and rendered)",
        type=int, nargs=1
    )
    parser.add_argument(
        "--simple","-s",
        default=False,
        help="Simplify the rendering to only show particles",
        action="store_true"
    )
    parser.add_argument(
        "--font",
        default=["BitPotion.ttf"],
        help="Font to use when rendering. ",
        type=str, nargs=1)

    parser.add_argument(
        "--noratelimit",
        default=False,
        help="Render faster than FPS",
        action="store_true"
    )



    args = parser.parse_args()

    main(
        N = args.nodes[0],
        K = args.channels[0],
        width = args.width[0],
        height = args.height[0],
        fps = args.fps[0],
        font_fn = args.font[0],
        total_time=args.totaltime[0],
        simplify_render=args.simple,
        ratelimit = not args.noratelimit

    )
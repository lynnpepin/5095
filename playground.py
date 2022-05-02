import argparse
import math as mt
import os
import pickle
import random
import sys

import matplotlib
import numpy as np
import pygame

pygame.init()
pygame.display.set_caption("5390 go vroom")
screen = pygame.display.set_mode((600,600))

# colors, see https://lospec.com/palette-list/sweetie-16
BG = np.array((26, 28, 44))
TRAIL_END = np.array((93, 39, 93))
TRAIL_START = np.array((115, 239, 255))
NODE = np.array((244, 244, 244))

FPS = 60
delta = 1/FPS
clock = pygame.time.Clock()

# Instantiate nodes
running = True
t = 0
x, y = 0,0
Xs = [0 for _ in range(20)]
Ys = [0 for _ in range(20)]

def interpolate(a, b, r, vmin=0, vmax=255):
    return min(vmax, max(vmin, a*r + b*(1-r)))

def interpolate_color(c1 = TRAIL_START, c2 = TRAIL_END, r = 0.5):
    r1, g1, b1 = c1
    r2, g2, b2 = c2
    r = interpolate(r1, r2, r)
    g = interpolate(g1, g2, r)
    b = interpolate(b1, b2, r)
    return (r, g, b)

while running:
    screen.fill(BG)
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            running = False
    
    # Update x, y
    x += 100 * delta
    y += 100 * delta
    Xs.pop()
    Xs.insert(0, x)
    Ys.insert(0, y)

    # Draw trail
    for ii in range(20):
        #color = np.interp(ii, [0, 20], [TRAIL_END, TRAIL_START])
        color = TRAIL_END * (ii / 20) + TRAIL_START * (1 - ii / 20)
        pygame.draw.circle(screen, color, (Xs[ii], Ys[ii]), 2)

    pygame.draw.circle(screen, NODE, (x, y), 3)

    clock.tick(FPS)
    pygame.display.update()

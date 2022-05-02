"""
"""

import argparse
import math as mt
import os
import pickle
import sys

import matplotlib
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("--number","-n", default=[0],
                        help="Integer argument.",
                        type=int, nargs=1)
    args = parser.parse_args()
    print(args)

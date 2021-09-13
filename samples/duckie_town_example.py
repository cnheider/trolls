#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01-06-2021
           """

import argparse

from gym_duckietown.envs import DuckietownEnv

parser = argparse.ArgumentParser()
parser.add_argument("--env-name", default="Duckietown-small_loop-v0")
parser.add_argument("--map-name", default="udem1")
parser.add_argument("--distortion", default=False, action="store_true")
parser.add_argument("--camera_rand", default=False, action="store_true")
parser.add_argument("--draw-curve", action="store_true", help="draw the lane following curve")
parser.add_argument("--draw-bbox", action="store_true", help="draw collision detection bounding boxes")
parser.add_argument("--domain-rand", action="store_true", help="enable domain randomization")
parser.add_argument("--dynamics_rand", action="store_true", help="enable dynamics randomization")
parser.add_argument("--frame-skip", default=1, type=int, help="number of frames to skip")
parser.add_argument("--seed", default=1, type=int, help="seed")
args = parser.parse_args()

env = DuckietownEnv(
    seed=args.seed,
    map_name=args.map_name,
    draw_curve=args.draw_curve,
    draw_bbox=args.draw_bbox,
    domain_rand=args.domain_rand,
    frame_skip=args.frame_skip,
    distortion=args.distortion,
    camera_rand=args.camera_rand,
    dynamics_rand=args.dynamics_rand,
)

env.reset()
env.render()

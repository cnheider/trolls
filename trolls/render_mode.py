#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 01-05-2021
           """

import enum


class RenderModeEnum(enum.Enum):
    """Common render modes"""

    none = "none"
    human = "human"
    to_screen = "human"  # to_screen
    rgb_array = "rgb_array"
    depth_array = "depth_array"
    segmentation_array = "segmentation_array"  # categories
    ansi = "ansi"

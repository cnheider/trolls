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
    """no render"""

    human = "human"
    """to_screen"""

    to_screen = "human"
    """to_screen"""

    rgb_array = "rgb_array"
    """to_array"""

    depth_array = "depth_array"
    """to_array"""

    segmentation_array = "segmentation_array"
    """to_array in categories"""

    ansi = "ansi"
    """to_text_array"""

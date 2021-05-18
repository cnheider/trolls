#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 29/01/2020
           """

from trolls.spaces import SignalSpace

__all__ = ["VectorSignalSpace"]


class VectorSignalSpace:
    """ """

    def __init__(self, signal_space: SignalSpace, num_env: int):
        self.signal_space = signal_space
        self.num_env = num_env

    def __getattr__(self, item):
        return getattr(self.signal_space, item)

    def __repr__(self):
        return self.signal_space.__repr__()

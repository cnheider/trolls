#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 29/01/2020
           """

from trolls.spaces import ObservationSpace


__all__ = ["VectorObservationSpace"]


class VectorObservationSpace:
    """ """

    def __init__(self, observation_space: ObservationSpace, num_env: int):
        self.observation_space = observation_space
        self.num_env = num_env

    def __getattr__(self, item):
        return getattr(self.observation_space, item)

    def __repr__(self):
        return self.observation_space.__repr__()

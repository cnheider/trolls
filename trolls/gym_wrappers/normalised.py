#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 04/01/2020
           """

import gym
import numpy
from gym.spaces import Discrete

__all__ = ["NormalisedActions"]


class NormalisedActions(gym.ActionWrapper):
    def reverse_action(self, a: numpy.ndarray) -> numpy.ndarray:
        """ """
        if isinstance(self.env.action_space, Discrete):
            return a.item()

        low = self.env.action_space.low
        high = self.env.action_space.high
        a = 2 * (a - low) / (high - low) - 1
        return numpy.clip(a, low, high)

    def action(self, a: numpy.ndarray) -> numpy.ndarray:
        """ """
        if isinstance(self.env.action_space, Discrete):
            return a.item()

        low = self.env.action_space.low
        high = self.env.action_space.high
        a = low + (a + 1.0) * 0.5 * (high - low)
        return numpy.clip(a, low, high)

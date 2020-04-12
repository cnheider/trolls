#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 04/01/2020
           """

import gym
import numpy
from gym.spaces import Discrete


class NormalisedActions(gym.ActionWrapper):
    def reverse_action(self, a):
        if isinstance(self.env.action_space, Discrete):
            return a

        low = self.env.action_space.low
        high = self.env.action_space.high

        a = 2 * (a - low) / (high - low) - 1
        a = numpy.clip(a, low, high)

        return a

    def action(self, a):
        if isinstance(self.env.action_space, Discrete):
            return a

        low = self.env.action_space.low
        high = self.env.action_space.high

        a = low + (a + 1.0) * 0.5 * (high - low)
        a = numpy.clip(a, low, high)

        return a

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import gym
import numpy
from gym.spaces.box import Box

__all__ = ["NoisyObservationWrapper", "NoisyActionWrapper"]


class NoisyObservationWrapper(gym.ObservationWrapper):
    """Make observation dynamic by adding noise"""

    def __init__(self, env: gym.Env = None, percent_pad=5, bottom_margin: int = 20):
        """
        # doom 20px bottom is useless

        :param env:
        :param percent_pad:
        :param bottom_margin:"""
        super().__init__(env)
        self.original_shape = env.space.shape
        new_side = int(round(max(self.original_shape[:-1]) * 100.0 / (100.0 - percent_pad)))
        self.new_shape = [new_side, new_side, 3]
        self.observation_space = Box(0.0, 255.0, self.new_shape)
        self.bottom_margin = bottom_margin
        self.ob = None

    def _observation(self, obs: numpy.ndarray) -> numpy.ndarray:
        im_noise = numpy.random.randint(0, 256, self.new_shape).astype(obs.dtype)
        im_noise[: self.original_shape[0] - self.bottom_margin, : self.original_shape[1], :] = obs[
            : -self.bottom_margin, :, :
        ]
        self.ob = im_noise
        return im_noise

    # def render(self, mode='human', close=False):
    #     temp = self.env.render(mode, close)
    #     return self.ob


class NoisyActionWrapper(gym.ActionWrapper):
    """
    TODO: finish
    Make action dynamic by adding noise"""

    def __init__(self, env: gym.Env = None, percent_pad=5, bottom_margin: int = 20):
        super().__init__(env)
        self.original_shape = env.space.shape
        new_side = int(round(max(self.original_shape[:-1]) * 100.0 / (100.0 - percent_pad)))
        self.new_shape = [new_side, new_side, 3]
        self.action_space = Box(0.0, 255.0, self.new_shape)
        self.bottom_margin = bottom_margin
        self.ob = None

    def _action(self, obs: numpy.ndarray) -> numpy.ndarray:
        im_noise = numpy.random.randint(0, 256, self.new_shape).astype(obs.dtype)
        im_noise[: self.original_shape[0] - self.bottom_margin, : self.original_shape[1], :] = obs[
            : -self.bottom_margin, :, :
        ]
        self.ob = im_noise
        return im_noise

    # def render(self, mode='human', close=False):
    #     temp = self.env.render(mode, close)
    #     return self.ob

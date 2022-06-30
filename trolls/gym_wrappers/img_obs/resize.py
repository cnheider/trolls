#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
Resize wrapper for gym.Env.
           Created on 31-03-2021
           """

import warnings
from typing import Dict, Sequence, Tuple

import gym
import gym.spaces
import numpy
from gym.spaces import Box
from skimage import img_as_ubyte
from skimage.transform import resize
from torchvision.transforms import Compose, Normalize, Resize

from trolls.spaces_mixin import SpacesMixin

__all__ = ["Resize", "ResizeObservation"]


class ResizeSkImage(gym.Wrapper, SpacesMixin):
    """gym.Env wrapper for resizing frame to (width, height).

    Only works with gym.spaces.Box environment with 2D single channel frames.

    Example:
        | env = gym.make('Env')
        | # env.observation_space = (100, 100)
        | env_wrapped = Resize(gym.make('Env'), width=64, height=64)
        | # env.observation_space = (64, 64)

    Args:
        env: gym.Env to wrap.
        width: resized frame width.
        height: resized frame height.

    Raises:
        ValueError: If observation space shape is not 2
            or environment is not gym.spaces.Box.

    """

    def __init__(self, env, width, height):
        if not isinstance(env.observation_space, gym.spaces.Box):
            raise ValueError("Resize only works with Box environment.")

        if len(env.observation_space.shape) != 2:
            raise ValueError("Resize only works with 2D single channel image.")

        super().__init__(env)

        _low = env.observation_space.low.flatten()[0]
        _high = env.observation_space.high.flatten()[0]
        self._dtype = env.observation_space.dtype
        self._observation_space = gym.spaces.Box(_low, _high, shape=[width, height], dtype=self._dtype)

        self._width = width
        self._height = height

    def _observation(self, obs):
        with warnings.catch_warnings():
            """
            Suppressing warnings for
            1. possible precision loss when converting from float64 to uint8
            2. anti-aliasing will be enabled by default in skimage 0.15
            """
            warnings.simplefilter("ignore")
            obs = resize(obs, (self._width, self._height))  # now it's float
            if self._dtype == numpy.uint8:
                obs = img_as_ubyte(obs)
        return obs

    def reset(self):
        """gym.Env reset function."""
        return self._observation(self.env.reset())

    def step(self, action) -> Tuple[Sequence, float, bool, Dict]:
        """gym.Env step function."""
        obs, reward, done, info = self.env.step(action)
        return self._observation(obs), reward, done, info


class ResizeObservation(gym.ObservationWrapper):
    def __init__(self, env, shape):
        super().__init__(env)
        if isinstance(shape, int):
            self.shape = (shape, shape)
        else:
            self.shape = tuple(shape)

        obs_shape = self.shape + self.observation_space.shape[2:]
        self.observation_space = Box(low=0, high=255, shape=obs_shape, dtype=numpy.uint8)

    def observation(self, observation):
        transforms = Compose([Resize(self.shape), Normalize(0, 255)])
        observation = transforms(observation).squeeze(0)
        return observation

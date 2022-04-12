#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""
Grayscale wrapper for gym.Env.
           Created on 31-03-2021
           """

from typing import Dict, Sequence, Tuple

import gym
import gym.spaces
import numpy
import torch
from draugr.extensions import rgb_to_grayscale
from gym.spaces import Box
from torchvision.transforms import Grayscale
from trolls.spaces_mixin import SpacesMixin

__all__ = ["Grayscale", "GrayScaleObservation"]


class GrayscaleNonTorch(gym.Wrapper, SpacesMixin):
    """Grayscale wrapper for gym.Env, converting frames to grayscale.

    Only works with gym.spaces.Box environment with 2D RGB frames.
    The last dimension (RGB) of environment observation space will be removed.

    Example:
        env = gym.make('Env')
        # env.observation_space = (100, 100, 3)

        env_wrapped = Grayscale(gym.make('Env'))
        # env.observation_space = (100, 100)

    Args:
        env (gym.Env): Environment to wrap.

    Raises:
        ValueError: If observation space shape is not 3
            or environment is not gym.spaces.Box.

    """

    def __init__(self, env):
        if not isinstance(env.observation_space, gym.spaces.Box):
            raise ValueError("Grayscale only works with gym.spaces.Box environment.")

        if len(env.observation_space.shape) != 3:
            raise ValueError("Grayscale only works with 2D RGB images")

        super().__init__(env)

        _low = env.observation_space.low.flatten()[0]
        _high = env.observation_space.high.flatten()[0]
        assert _low == 0
        assert _high == 255
        self._observation_space = gym.spaces.Box(
            _low, _high, shape=env.observation_space.shape[:-1], dtype=numpy.uint8
        )

    def reset(self, **kwargs):
        """gym.Env reset function.

        Args:
            **kwargs: Unused.

        Returns:
            numpy.ndarray: Observation conforming to observation_space
        """
        del kwargs
        return rgb_to_grayscale(self.env.reset())

    def step(self, action) -> Tuple[Sequence, float, bool, Dict]:
        """See gym.Env.

        Args:
            action (numpy.ndarray): Action conforming to action_space

        Returns:
            numpy.ndarray: Observation conforming to observation_space
            float: Reward for this step
            bool: Termination signal
            dict: Extra information from the environment.

        """
        obs, reward, done, info = self.env.step(action)
        return rgb_to_grayscale(obs), reward, done, info


class GrayScaleObservation(gym.ObservationWrapper):
    def __init__(self, env):
        super().__init__(env)
        obs_shape = self.observation_space.shape[:2]
        self.observation_space = Box(low=0, high=255, shape=obs_shape, dtype=numpy.uint8)

    def permute_orientation(self, observation):
        # permute [H, W, C] array to [C, H, W] tensor
        observation = numpy.transpose(observation, (2, 0, 1))
        observation = torch.tensor(observation.copy(), dtype=torch.float)
        return observation

    def observation(self, observation):
        observation = self.permute_orientation(observation)
        transform = Grayscale()
        observation = transform(observation)
        return observation

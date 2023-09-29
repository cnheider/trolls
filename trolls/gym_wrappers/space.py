#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 10-05-2021
           """

from typing import List

import gym
from trolls.spaces import ActionSpace, Dimension, ObservationSpace, SignalSpace
from trolls.spaces_mixin import SpacesMixin


def box_to_dimensions(box_space: gym.spaces.Box) -> List[Dimension]:
    assert isinstance(box_space, gym.spaces.Box), f"{box_space} is not a Box space"
    # TODO: CHECK ASSUMPTIONS!
    # bounded = box_space.is_bounded('below') or box_space.is_bounded('above')

    # print(box_space)

    if (
        len(box_space.high.shape) == 3  # assume image
        and box_space.high.shape[-1]
        and box_space.high[-1, -1, -1] == 255
        and box_space.low[-1, -1, -1] == 0
    ):
        h, w, c = box_space.high.shape
        return [
            Dimension(max_value=255, min_value=0, decimal_granularity=0)
            for _ in range(w)
            for __ in range(h)
            for ___ in range(c)
        ]
    else:
        return list(
            Dimension(max_value=high, min_value=low, decimal_granularity=3)
            for high, low in zip(box_space.high, box_space.low)
        )


def discrete_to_dimensions(box_space: gym.spaces.Discrete) -> List[Dimension]:
    """

    :param box_space:
    :type box_space:
    :return:
    :rtype:
    """
    assert isinstance(box_space, gym.spaces.Discrete), f"{box_space} is not a Discrete space"
    # TODO: CHECK ASSUMPTIONS!
    # bounded = box_space.is_bounded('below') or box_space.is_bounded('above')
    return list(
        Dimension(max_value=high, min_value=low, decimal_granularity=0)
        for high, low in zip((box_space.n - 1,), (0,))
    )


def to_dimension(space: gym.spaces.Space) -> List[Dimension]:
    """

    :param space:
    :type space:
    :return:
    :rtype:
    """
    if isinstance(space, gym.spaces.Box):
        return box_to_dimensions(space)
    elif isinstance(space, gym.spaces.Discrete):
        return discrete_to_dimensions(space)
    else:
        raise NotImplementedError(f"{space} is not a supported space")


def get_dict_attr(obj, attr):
    for obj in [obj] + obj.__class__.mro():
        if attr in obj.__dict__:
            return obj.__dict__[attr]
    # raise AttributeError


class SpaceWrapper(SpacesMixin):
    def __init__(self, env: gym.Env):
        self.env = env

    @property
    def observation_space(self) -> ObservationSpace:
        return ObservationSpace(to_dimension(self.env.observation_space))

    @property
    def action_space(self) -> ActionSpace:
        return ActionSpace(to_dimension(self.env.action_space))

    @property
    def signal_space(self) -> SignalSpace:
        min_val, max_val = self.env.reward_range
        return SignalSpace((Dimension(min_value=min_val, max_value=max_val),))

    def __getattr__(self, item):
        p = get_dict_attr(self, item)
        if p and isinstance(p, property):
            return p.__get__(self)
        return getattr(self.env, item)

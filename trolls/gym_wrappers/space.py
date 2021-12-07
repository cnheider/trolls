#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 10-05-2021
           """

from typing import Iterable, List

import gym
from gym.spaces import Box

from trolls.spaces import ActionSpace, ObservationSpace, Range, SignalSpace
from trolls.spaces_mixin import SpacesMixin


def box_to_ranges(box_space: gym.spaces.Box) -> List[Range]:
    # TODO: CHECK ASSUMPTIONS!
    # bounded = box_space.is_bounded('below') or box_space.is_bounded('above')
    return list(
        Range(max_value=high, min_value=low, decimal_granularity=3)
        for high, low in zip(box_space.high, box_space.low)
    )


class SpaceWrapper(SpacesMixin):
    def __init__(self, env: gym.Env):
        self.env = env

    @property
    def observation_space(self) -> ObservationSpace:
        return ObservationSpace(box_to_ranges(self.env.observation_space))

    @property
    def action_space(self) -> ActionSpace:
        return ActionSpace(box_to_ranges(self.env.action_space))

    @property
    def signal_space(self) -> SignalSpace:
        print(self.env.reward_range)
        return SignalSpace(self.env.reward_range)

    def __getattr__(self, item):
        return getattr(self.env, item)

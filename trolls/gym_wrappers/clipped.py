#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import gym
from warg import Number

__all__ = ["ClippedSignal"]


class ClippedSignal(gym.RewardWrapper):
    """Clip signal."""

    def reward(self, signal: Number) -> Number:
        return self._signal(signal)

    def __init__(
        self,
        env: gym.Env = None,
        negative_clip: Number = 0.0,
        positive_clip: Number = None,
    ):
        super().__init__(env)
        self._negative_clip = negative_clip
        self._positive_clip = positive_clip

    def _signal(self, signal: Number) -> Number:
        new_signal = self._negative_clip if self._positive_clip and signal < self._negative_clip else signal
        new_signal = (
            self._positive_clip if self._positive_clip and signal > self._positive_clip else new_signal
        )
        return new_signal

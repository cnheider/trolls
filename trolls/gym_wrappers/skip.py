# !/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

from typing import Any, Dict, Sequence, Tuple

import gym

__all__ = ["SkipRepeatAccumulateLast"]


class SkipRepeatAccumulateLast(gym.Wrapper):
    """Skip timesteps: repeat action, accumulate signal, take last obs."""

    def __init__(self, env: gym.Env = None, num_skips: int = 4):
        super().__init__(env)
        self._num_skips = num_skips

    def _step(self, action: Any) -> Tuple[Sequence, float, bool, Dict]:
        total_signal = 0
        obs = 0
        terminal = False
        info = {}

        for i in range(0, self._num_skips):
            obs, signal, terminal, info = self.env.act(action)
            total_signal += signal
            info["steps"] = i + 1
            if terminal:
                break

        return obs, total_signal, terminal, info

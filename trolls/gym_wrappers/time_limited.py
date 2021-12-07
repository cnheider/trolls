#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import logging
import time
from typing import Dict, Sequence, Tuple

from gym import Wrapper

_logger = logging.getLogger(__name__)

__all__ = ["EpisodeLimitedWrapper"]


class EpisodeLimitedWrapper(Wrapper):
    """ """

    def __init__(self, env, max_episode_seconds=None, max_episode_steps=None):
        super().__init__(env)
        self._max_episode_seconds = max_episode_seconds
        self._max_episode_steps = max_episode_steps

        self._elapsed_steps = 0
        self._episode_started_at = None

    @property
    def _elapsed_seconds(self) -> float:
        return time.time() - self._episode_started_at

    def _past_limit(self) -> bool:
        """Return true if we are past our limit"""
        if self._max_episode_steps is not None and self._max_episode_steps <= self._elapsed_steps:
            _logger.debug("Env has passed the step limit defined by TimeLimit.")
            return True

        if self._max_episode_seconds is not None and self._max_episode_seconds <= self._elapsed_seconds:
            _logger.debug("Env has passed the seconds limit defined by TimeLimit.")
            return True

        return False

    def _step(self, action) -> Tuple[Sequence, float, bool, Dict]:
        assert self._episode_started_at is not None, "Cannot call env.step() before calling reset()"
        observation, reward, done, info = self.env.act(action)
        self._elapsed_steps += 1

        if self._past_limit():
            if self.metadata.get("semantics.autoreset"):
                _ = self.reset()  # automatically reset the env
            done = True

        return observation, reward, done, info

    def _reset(self):
        self._episode_started_at = time.time()
        self._elapsed_steps = 0
        return self.env.reset()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

import logging
from typing import Dict, Sequence, Tuple

from gym import Wrapper

_logger = logging.getLogger(__name__)

__all__ = ["NoTerminationWrapper"]


class NoTerminationWrapper(Wrapper):
    """ """

    def _step(self, action) -> Tuple[Sequence, float, bool, Dict]:
        observation, reward, done, info = self.env.act(action)
        if done:
            _ = self.reset()
        return observation, reward, False, info

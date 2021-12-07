#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 03-04-2021
           """

__all__ = ["SpacesMixin"]

from trolls.spaces import ActionSpace, ObservationSpace, SignalSpace


class SpacesMixin(ABC):
    @property
    @abstractmethod
    def action_space(self) -> ActionSpace:
        """gym.Env: Action space."""

        raise NotImplemented

    @property
    @abstractmethod
    def observation_space(self) -> ObservationSpace:
        """gym.Env: Observation space."""

        raise NotImplemented

    @property
    @abstractmethod
    def signal_space(self) -> SignalSpace:
        """gym.Env: Signal space."""
        raise NotImplemented

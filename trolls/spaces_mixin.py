#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 03-04-2021
           """

__all__ = [
    "SpacesMixin",
    "SignalSpaceMixin",
    "ObservationSpaceMixin",
    "ActionSpaceMixin",
]

from trolls.spaces import ActionSpace, ObservationSpace, SignalSpace


class SignalSpaceMixin(ABC):
    @property
    @abstractmethod
    def signal_space(self) -> SignalSpace:
        """gym.Env: Signal space."""
        raise NotImplemented


class ObservationSpaceMixin(ABC):
    @property
    @abstractmethod
    def observation_space(self) -> ObservationSpace:
        """gym.Env: Observation space."""

        raise NotImplemented


class ActionSpaceMixin(ABC):
    @property
    @abstractmethod
    def action_space(self) -> ActionSpace:
        """gym.Env: Action space."""

        raise NotImplemented


class SpacesMixin(SignalSpaceMixin, ObservationSpaceMixin, ActionSpaceMixin):
    pass

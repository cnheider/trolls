#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 03-04-2021
           """

__all__ = ["VectorEnvironments", "VectorEnvironmentsWrapper", "VectorWrap"]

import logging
from abc import abstractmethod
from .spaces_mixin import SpacesMixin


class VectorEnvironments(SpacesMixin):
    """ """

    def __init__(self, num_envs, observation_space, action_space, signal_space):
        self.num_envs = num_envs
        self._observation_space = observation_space
        self._action_space = action_space
        self._signal_space = signal_space

    """
An abstract asynchronous, vectorized environment.
"""

    @abstractmethod
    def reset(self):
        """
        Reset all the environments and return an array of
        observations.

        If step_async is still doing work, that work will
        be cancelled and step_wait() should not be called
        until step_async() is invoked again."""
        pass

    @abstractmethod
    def step_async(self, actions):
        """
        Tell all the environments to start taking a step
        with the given actions.
        Call step_wait() to get the results of the step.

        You should not call this if a step_async run is
        already pending."""
        pass

    @abstractmethod
    def step_wait(self):
        """
        Wait for the step taken with step_async().

        Returns (obs, rews, dones, info):
        - obs: an array of observations
        - rews: an array of rewards
        - dones: an array of "episode done" booleans
        - info: an array of info objects"""
        pass

    @abstractmethod
    def close(self):
        """
        Clean up the environments' resources."""
        pass

    def step(self, actions):
        """

        :param actions:
        :type actions:
        :return:
        :rtype:
        """
        self.step_async(actions)
        return self.step_wait()

    def render(self):
        """ """
        logging.warning(f"Render not defined for {self}")


class VectorEnvironmentsWrapper(VectorEnvironments):
    """ """

    def __init__(self, venv, observation_space=None, action_space=None):
        self.venv = venv
        VectorEnvironments.__init__(
            self,
            num_envs=venv.num_envs,
            observation_space=observation_space or venv.space,
            action_space=action_space or venv.action_space,
        )

    def step_async(self, actions):
        """

        :param actions:
        :type actions:
        """
        self.venv.step_async(actions)

    @abstractmethod
    def reset(self):
        """ """
        pass

    @abstractmethod
    def step_wait(self):
        """ """
        pass

    def close(self):
        """

        :return:
        :rtype:
        """
        return self.venv.close()

    def render(self):
        """ """
        self.venv.render()


class VectorWrap:
    """ """

    def __init__(self, env):
        self.env = env

    def react(self, a, *args, **kwargs):
        """

        :param a:
        :type a:
        :param args:
        :type args:
        :param kwargs:
        :type kwargs:
        :return:
        :rtype:
        """
        return self.env.react(a[0], *args, **kwargs)

    def reset(self):
        """

        :return:
        :rtype:
        """
        return self.env.reset()

    def __getattr__(self, item):
        return getattr(self.env, item)

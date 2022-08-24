#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"

__doc__ = r"""

           Created on 03-04-2021
           """

import enum
import pickle
import time
import warnings
from collections import namedtuple
from contextlib import suppress
from functools import wraps
from multiprocessing import Pipe, Process
from multiprocessing.connection import Connection
from typing import Any, Callable, Optional, Sequence, Tuple, Union

import cloudpickle
import gym
import numpy
from skimage.transform import resize
from sorcery import assigned_names
from warg import Number, drop_unused_kws

from trolls.gym_wrappers import NormalisedActions
from trolls.gym_wrappers.space import SpaceWrapper
from trolls.render_mode import RenderModeEnum
from trolls.spaces import (
    ActionSpace,
    ObservationSpace,
    SSSS,
    VectorActionSpace,
    VectorObservationSpace,
    VectorSignalSpace,
)
from trolls.spaces_mixin import SpacesMixin

__all__ = [
    "EnvironmentWorkerCommandsEnum",
    "environment_worker",
    "make_gym_env",
    "MultipleEnvironments",
    "SubProcessEnvironments",
    "CloudPickleBase",
]


class EnvironmentWorkerCommandsEnum(enum.Enum):
    """ """

    (step, reset, close, get_spaces, render, seed) = assigned_names()


EWC = EnvironmentWorkerCommandsEnum

EnvironmentCommand = namedtuple("EnvironmentCommand", ("command", "data"))

EC = EnvironmentCommand

GymTuple = namedtuple("GymTuple", ("observation", "signal", "terminal", "info"))


class ItemizeNumpy(gym.Wrapper):
    def step(self, action: Union[numpy.ndarray, Number]):
        if isinstance(action, (numpy.ndarray, numpy.generic)):
            return super().step(action.item())
        # if isinstance(action, numpy.generic):
        #  return numpy.asscalar(action)
        return super().step(action)


def make_gym_env(env_nam: str, normalise_actions: bool = True) -> callable:
    """ """

    assert env_nam in gym.envs.registry.env_specs, f"{env_nam} not found in gym.envs.registry.env_specs"

    @wraps(gym.make)
    def wrapper() -> SpaceWrapper:
        """ """
        env = gym.make(env_nam)
        if normalise_actions:
            env = NormalisedActions(env)

        return SpaceWrapper(env)

    return wrapper


def environment_worker(
    remote: Connection,
    parent_remote: Connection,
    env_fn_wrapper: callable,
    auto_reset_on_terminal: bool = False,
    render_obs_size_tuple: Optional[Tuple[int, int]] = None,  # (128, 128)
):
    """

    :param remote:
    :param parent_remote:
    :param env_fn_wrapper:
    :param auto_reset_on_terminal:
    :param render_obs_size_tuple:
    :return:"""
    warnings.simplefilter("ignore")
    # with IgnoreInterruptSignal(): # TODO: DOES NOT WORK AS intended here, endless looping, needs another way to send a close signal
    with suppress(UserWarning, KeyboardInterrupt):
        parent_remote.close()
        env = env_fn_wrapper.x()
        terminated = False

        while True:
            cmd, data = remote.recv()
            if cmd is EWC.step:
                observation, signal, terminal, info = env.step(data)
                if terminated:
                    signal = 0
                if terminal:
                    terminated = True
                    if auto_reset_on_terminal:
                        observation = env.reset()
                        terminated = False
                remote.send(GymTuple(observation, signal, terminal, info))
            elif cmd is EWC.reset:
                observation = env.reset()
                terminated = False
                remote.send(observation)
            elif cmd is EWC.close:
                env.close()
                # remote.send(None)
                break
            elif cmd is EWC.get_spaces:
                remote.send((env.observation_space, env.action_space))
            elif cmd is EWC.render:
                res = env.render(data)
                if data != RenderModeEnum.human.value:
                    if render_obs_size_tuple:
                        res = resize(res, render_obs_size_tuple)  # VERY SLOW!!!
                    remote.send(res)
            elif cmd is EWC.seed:
                env.seed(data)
            else:
                raise NotImplementedError


class MultipleEnvironments(gym.Env):
    """
    An abstract asynchronous, vectorized environment."""

    def render(self, mode="human"):
        """ """
        pass

    def __init__(
        self,
        num_environments: int,
        observation_space: ObservationSpace,
        action_space: ActionSpace,
    ):
        self._num_environments = num_environments
        self._observation_space = VectorObservationSpace(observation_space, num_environments)
        self._action_space = VectorActionSpace(action_space, num_environments)
        self._signal_space = VectorSignalSpace(SSSS(), self._num_environments)

    @property
    def signal_space(self) -> VectorSignalSpace:
        return self._signal_space

    @property
    def observation_space(self) -> VectorObservationSpace:
        """ """
        return self._observation_space

    @property
    def action_space(self) -> VectorActionSpace:
        """ """
        return self._action_space

    def reset(self):
        """
        Reset all the environment_utilities and return an array of
        observations, or a tuple of observation arrays.
        If step_async is still doing work, that work will
        be cancelled and step_wait() should not be called
        until step_async() is invoked again."""
        raise NotImplementedError

    def step_async(self, actions):
        """
        Tell all the environment_utilities to start taking a step
        with the given actions.
        Call step_wait() to get the results of the step.
        You should not call this if a step_async run is
        already pending."""
        raise NotImplementedError

    def step_wait(self):
        """
        Wait for the step taken with step_async().
        Returns (obs, signals, terminals, infos):
        - obs: an array of observations, or a tuple of
        arrays of observations.
        - signals: an array of rewards
        - terminals: an array of "episode terminal" booleans
        - infos: a sequence of info objects"""
        raise NotImplementedError

    def close(self):
        """
        Clean up the environment_utilities' resources."""
        raise NotImplementedError

    def step(self, actions):
        """ """
        self.step_async(actions)
        return self.step_wait()


class CloudPickleBase(object):
    """
    Uses cloudpickle to serialize contents (otherwise multiprocessing tries to use pickle)
    :param x: (Any) the variable you wish to wrap for pickling with cloudpickle"""

    def __init__(self, x: Any):
        self.x = x

    def __getstate__(self):
        return cloudpickle.dumps(self.x)

    def __setstate__(self, x):
        self.x = pickle.loads(x)


class SubProcessEnvironments(MultipleEnvironments):
    """ """

    def __init__(
        self,
        environments: Sequence[Callable],
        auto_reset_on_terminal_state: bool = False,
    ):
        """
        environments: list of gym environment_utilities to run in subprocesses"""
        self._waiting = False
        self._closed = False
        self._num_environments = len(environments)
        self._remotes, self._work_remotes = zip(*[Pipe() for _ in range(self._num_environments)])
        self._processes = [
            Process(
                target=environment_worker,
                args=(
                    work_remote,
                    remote,
                    CloudPickleBase(env),
                    auto_reset_on_terminal_state,
                ),
            )
            for (work_remote, remote, env) in zip(self._work_remotes, self._remotes, environments)
        ]
        for p in self._processes:
            p.daemon = True  # if the main process crashes, we should not cause things to hang
            p.start()
        for remote in self._work_remotes:
            remote.close()

        self._remotes[0].send(EC(EWC.get_spaces, None))
        try:
            observation_space, action_space = self._remotes[0].recv()
        except EOFError as e:
            raise StopIteration(f"End of Stream, {e}")

        super().__init__(len(environments), observation_space, action_space)

    # noinspection PyMethodOverriding
    def seed(self, seed: Union[int, Sequence]) -> None:
        """

        :param seed:
        :return:"""
        if isinstance(seed, Sequence):
            assert len(seed) == self._num_environments
            for remote, s in zip(self._remotes, seed):
                remote.send(EC(EWC.seed, s))
        else:
            for remote in self._remotes:
                remote.send(EC(EWC.seed, seed))

    @drop_unused_kws
    def render(
        self,
        render_mode: Union[RenderModeEnum, str] = RenderModeEnum.human,
        only_render_single: bool = True,
    ) -> Optional[Sequence]:
        """

        :return:"""
        if isinstance(render_mode, RenderModeEnum):
            render_mode_str = render_mode.value
        else:
            render_mode_str = render_mode
            render_mode = RenderModeEnum(render_mode)

        remotes = self._remotes
        if only_render_single:
            remotes = remotes[:1]

        for remote in remotes:
            remote.send(EC(EWC.render, render_mode_str))

        if render_mode != RenderModeEnum.none and render_mode != RenderModeEnum.human:
            self._waiting = True
            res = [remote.recv() for remote in remotes]
            self._waiting = False
            return res

    def step_async(self, actions) -> None:
        """

        :param actions:
        :return:"""
        for remote, action in zip(self._remotes, actions):
            remote.send(EC(EWC.step, action))
        self._waiting = True

    def step_wait(self):
        """

        :return:"""
        with suppress(EOFError):
            results = [remote.recv() for remote in self._remotes]
            self._waiting = False
            return results
        raise StopIteration("End of Stream")

    def reset(self):
        """

        :return:"""
        for remote in self._remotes:
            remote.send(EC(EWC.reset, None))
        self._waiting = True
        res = [remote.recv() for remote in self._remotes]
        self._waiting = False
        return res

    def close(self) -> None:
        """

        :return:"""
        if self._closed:
            return
        if self._waiting:
            for remote in self._remotes:
                try:
                    remote.recv()
                except (EOFError, ConnectionResetError, BrokenPipeError) as e:
                    warnings.warn(str(e))
        for remote in self._remotes:
            remote.send(EC(EWC.close, None))
        for p in self._processes:
            p.join()
            p.close()
            self._closed = True

    def __len__(self) -> int:
        """

        :return:"""
        return self._num_environments


if __name__ == "__main__":

    def asidj():
        env = SubProcessEnvironments([make_gym_env("Pendulum-v1") for _ in range(3)])
        env.reset()
        for i in range(10):
            vector_action = env.action_space.sample()
            env.step(vector_action)
            env.render()

        env.close()
        time.sleep(1)

    asidj()

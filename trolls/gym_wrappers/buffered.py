#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Christian Heider Nielsen"

from collections import deque

import gym
import numpy
from PIL import Image
from gym.spaces.box import Box
from typing import Dict, Sequence, Tuple

__all__ = ["BufferedObservations"]


class BufferedObservations(gym.ObservationWrapper):
    """Buffer observations and stack e.g. for frame skipping.

    n is the length of the buffer, and number of observations stacked.
    skip is the number of steps between buffered observations (min=1).

    n.b. first obs is the oldest, last obs is the newest.
     the buffer is zeroed out on reset.
     *must* call reset() for init!"""

    def __init__(
        self,
        env=None,
        buffer_length=4,
        skip=4,
        shape=(84, 84),
        channel_last=True,
        maxFrames=True,
    ):
        super().__init__(env)
        self.obs_shape = shape

        self.obs_buffer = deque(maxlen=2)  # most recent raw observations (for max pooling across time steps)
        self._max_frames = maxFrames
        self.buffer_length = buffer_length
        self.skip = skip
        self.buffer = deque(maxlen=self.buffer_length)
        self.counter = 0  # init and reset should agree on this
        shape = shape + (buffer_length,) if channel_last else (buffer_length,) + shape
        self.observation_space = Box(0.0, 255.0, shape)
        self.ch_axis = -1 if channel_last else 0
        self.scale = 1.0 / 255
        self.observation_space.high[...] = 1.0

    def _step(self, action: numpy.ndarray) -> Tuple[Sequence, float, bool, Dict]:
        obs, signal, terminal, info = self.env.act(action)
        return self._observation(obs), signal, terminal, info

    def _observation(self, obs: numpy.ndarray) -> numpy.ndarray:
        obs = self._convert(obs)
        self.counter += 1
        if self.counter % self.skip == 0:
            self.buffer.append(obs)
        new_obs = numpy.stack(self.buffer, axis=self.ch_axis)
        return new_obs.astype(numpy.float32) * self.scale

    def _reset(self):
        """Clear buffer and re-fill by duplicating the first observation."""
        self.obs_buffer.clear()
        obs = self._convert(self.env.reset())
        self.buffer.clear()
        self.counter = 0
        for _ in range(self.buffer_length - 1):
            self.buffer.append(numpy.zeros_like(obs))
        self.buffer.append(obs)
        new_obs = numpy.stack(self.buffer, axis=self.ch_axis)
        return new_obs.astype(numpy.float32) * self.scale

    def _convert(self, obs):
        self.obs_buffer.append(obs)
        if self._max_frames:
            max_frame = numpy.max(numpy.stack(self.obs_buffer), axis=0)
        else:
            max_frame = obs
        intensity_frame = self._rgb2y(max_frame).astype(numpy.uint8)
        small_frame = numpy.array(
            Image.fromarray(intensity_frame).resize(self.obs_shape, resample=Image.BILINEAR),
            dtype=numpy.uint8,
        )
        return small_frame

    @staticmethod
    def _rgb2y(im):
        """Converts an RGB image to a Y image (as in YUV).

        These coefficients are taken from the torch/image library.
        Beware: these are more critical than you might think, as the
        monochromatic contrast can be surprisingly low."""
        if len(im.shape) < 3:
            return im

        return numpy.sum(im * [0.299, 0.587, 0.114], axis=2)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import List

from trolls.spaces.dimension import Dimension
from trolls.spaces.space import Space

__author__ = "Christian Heider Nielsen"
__all__ = ["ActionSpace"]

import numpy

from warg import Number, cached_property


class ActionSpace(Space):
    def validate(self, actions: List[Number]) -> List[Number]:
        """

        :param actions:
        :type actions:
        :return:
        :rtype:
        """
        for i in range(len(actions)):
            clipped = numpy.clip(actions[i], self._ranges[i].min_unnorm, self._ranges[i].max_unnorm)
            actions[i] = numpy.round(clipped, self._ranges[i].decimal_granularity)
        return actions

    def discrete_one_hot_sample(self) -> numpy.ndarray:
        """

        :return:
        :rtype:
        """
        idx = numpy.random.randint(0, self.num_actuators)
        zeros = numpy.zeros(self.num_actuators)
        if len(self._ranges) > 0:
            val = numpy.random.random_integers(
                int(self._ranges[idx].min_unnorm), int(self._ranges[idx].max_unnorm), 1
            )
            zeros[idx] = val
        return zeros

    def one_hot_sample(self) -> numpy.ndarray:
        """

        :return:
        :rtype:
        """
        idx = numpy.random.randint(0, self.num_actuators)
        zeros = numpy.zeros(self.num_actuators)
        if len(self._ranges) > 0:
            zeros[idx] = 1
        return zeros

    @cached_property
    def num_actuators(self) -> int:
        """

        :return:
        :rtype:
        """
        return self.n


if __name__ == "__main__":
    acs = ActionSpace(
        [
            Dimension(min_value=0, max_value=3, decimal_granularity=2),
            Dimension(min_value=0, max_value=2, decimal_granularity=1),
        ]
    )
    print(acs, acs.low, acs.high, acs.decimal_granularity, acs.discrete_steps, acs.shape)

    acs = ActionSpace(
        [
            Dimension(min_value=0, max_value=3, decimal_granularity=2, normalised=False),
            Dimension(min_value=0, max_value=2, decimal_granularity=1, normalised=False),
        ]
    )
    print(
        acs,
        acs.low,
        acs.high,
        acs.decimal_granularity,
        acs.discrete_steps,
        acs.shape,
        acs.discrete_steps_shape,
    )

    acs = ActionSpace(
        [
            Dimension(min_value=0, max_value=1, decimal_granularity=0, normalised=False),
            Dimension(min_value=0, max_value=1, decimal_granularity=0, normalised=False),
        ]
    )
    print(
        acs,
        acs.low,
        acs.high,
        acs.decimal_granularity,
        acs.discrete_steps,
        acs.shape,
        acs.discrete_steps_shape,
    )

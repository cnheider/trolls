#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import math
from typing import Sequence

import numpy
from trolls.spaces.range import Range
from trolls.spaces.space import Space

__author__ = "Christian Heider Nielsen"

__all__ = ["SignalSpace", "SingleScalarSignalSpaces", "SSSS"]

from warg import Number, cached_property


class SignalSpace(Space):
    """ """

    def __init__(self, ranges: Sequence[Range], solved_threshold: Number = math.inf):
        super().__init__(ranges)

        self.solved_threshold = solved_threshold

    def is_solved(self, value: Number) -> bool:
        """

        :param value:
        :type value:
        :return:
        :rtype:
        """
        return value > self.solved_threshold

    @cached_property
    def is_sparse(self) -> bool:
        """

        :return:
        :rtype:
        """
        return numpy.array([a.decimal_granularity == 0 for a in self._ranges]).all()


class SingleScalarSignalSpaces(SignalSpace):
    def __init__(self, ranges: Sequence[Range] = (Range(),)):
        super().__init__(ranges)


SSSS = SingleScalarSignalSpaces

if __name__ == "__main__":
    acs = SignalSpace(
        [
            Range(min_value=0, max_value=3, decimal_granularity=2),
            Range(min_value=0, max_value=2, decimal_granularity=1),
        ],
    )
    print(acs, acs.low, acs.high, acs.decimal_granularity)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import functools

# SpaceType = TypeVar("Space", bound=Space)
from typing import Iterable
from typing import List, Tuple, Generator, Sequence

import numpy

# from typing import Type, TypeVar, Union,
from warg import Number, cached_property

from trolls.spaces.dimension import Dimension

__author__ = "Christian Heider Nielsen"

__all__ = ["Space"]


class Space(object):
    """ """

    def __init__(self, ranges: Sequence[Dimension], names: Iterable[str] = ()):
        """

        :param ranges:
        :param names:"""
        assert isinstance(ranges, Iterable) and not isinstance(ranges, Generator), f"was type {type(ranges)}"
        self._ranges = ranges
        self._names = names
        if self.is_singular_discrete:
            self.sampler = self._singular_discrete_sample  # TODO: MAYBE REMOVE?
        else:
            self.sampler = self._sample

    def _sample(self) -> List[Number]:
        """

        :return:
        :rtype:
        """
        actions = []
        for valid_input in self._ranges:
            # sample = numpy.random.uniform(                valid_input.min_unnorm, valid_input.max_unnorm, 1                ).item()
            # sample = numpy.round(sample, valid_input.decimal_granularity)
            sample = valid_input.sample()
            actions.append(sample)
        return actions

    def _singular_discrete_sample(self) -> numpy.ndarray:
        """

        :return:
        :rtype:
        """
        return numpy.random.randint(0, self.discrete_steps)

    def project(self, a: Iterable[Number]) -> Iterable[float]:
        """

        :param a:
        :return:"""
        if self.is_singular_discrete:
            return a
        # if self.is_01normalised:
        #    return numpy.clamp()
        return a
        # return (a - self.min) / self.span

    def reproject(self, a: Iterable[Number]) -> Iterable[float]:
        """

        :param a:
        :return:"""
        if self.is_singular_discrete:
            return a
        # if self.is_01normalised:
        #    return numpy.clamp()
        return a
        # return (a * self.span) + self.min

    def clip(self, values: Iterable) -> numpy.ndarray:
        """

        :param values:
        :return:"""
        assert len(self.ranges) == len(values)
        return numpy.array([a.clip(v) for a, v in zip(self._ranges, values)])

    def sample(self) -> Iterable[float]:
        """

        :return:"""
        return [r.sample() for r in self._ranges]

    @property
    def max(self) -> numpy.ndarray:
        """

        :return:"""
        return self.high

    @property
    def min(self) -> numpy.ndarray:
        """

        :return:"""
        return self.low

    @cached_property
    def ranges(self) -> Iterable[Dimension]:
        """

        :return:"""
        return self._ranges

    @cached_property
    def low(self) -> numpy.ndarray:
        """

        :return:"""
        return numpy.array([motion_space.min_unnorm for motion_space in self._ranges])

    @cached_property
    def high(self) -> numpy.ndarray:
        """

        :return:"""
        return numpy.array([motion_space.max_unnorm for motion_space in self._ranges])

    @cached_property
    def span(self) -> numpy.ndarray:
        """

        :return:"""
        res = self.high - self.low
        assert (res > 0).all()
        return res

    @cached_property
    def decimal_granularity(self) -> List[int]:
        """

        :return:"""
        return [motion_space.decimal_granularity for motion_space in self._ranges if motion_space]

    @cached_property
    def is_singular(self) -> bool:
        """

        :return:"""
        return len(self._ranges) == 1

    @cached_property
    def is_singular_discrete(self) -> bool:
        """

        :return:"""
        return self.is_discrete and self.is_singular

    @cached_property
    def is_discrete(self) -> bool:
        """

        :return:"""
        return numpy.array([a.decimal_granularity == 0 for a in self._ranges if a]).all()

    @cached_property
    def is_mixed(self) -> bool:
        """

        :return:"""
        return (
            numpy.array([a.decimal_granularity != 0 for a in self._ranges]).any() and not self.is_continuous
        )

    @cached_property
    def is_continuous(self) -> bool:
        """

        :return:"""
        return numpy.array([a.decimal_granularity != 0 for a in self._ranges]).all()

    @cached_property
    def shape(self) -> Tuple[int, ...]:
        """

        :return:"""
        if self.is_singular_discrete:
            return self.discrete_steps_shape

        return self.continuous_shape

    @cached_property
    def discrete_steps(self) -> int:
        """

        :return:"""
        return sum(self.discrete_steps_shape)

    @cached_property
    def discrete_steps_shape(self) -> Tuple[int, ...]:
        """

        :return:"""
        return (*[r.discrete_steps for r in self._ranges],)

    @cached_property
    def continuous_shape(self) -> Tuple[int, ...]:
        """

        :return:"""
        return (len(self._ranges),)

    @cached_property
    def is_01normalised(self) -> numpy.ndarray:
        """

        :return:"""
        return numpy.array([a.normalised for a in self._ranges if hasattr(a, "normalised")]).all()

    # @functools.lru_cache()
    def __repr__(self) -> str:
        """

        :return:"""
        names_str = "".join([str(r.__repr__()) for r in self._names])
        ranges_str = "".join([str(r.__repr__()) for r in self._ranges])

        return (
            f"<Space>\n"
            f"<Names>\n{names_str}</Names>\n"
            f"<Ranges>\n{ranges_str}</Ranges>\n"
            f"<Discrete>{self.is_singular_discrete}</Discrete>\n"
            f"</Space>\n"
        )

    @cached_property
    def n(self) -> int:
        """

        :return:"""
        return len(self._ranges)

    @functools.lru_cache()
    def __len__(self) -> int:
        """

        :return:"""
        return self.n

    def __eq__(self, other) -> bool:  #:SpaceType
        return True if self.ranges == other.ranges else False

    def sample(self) -> List[Number]:
        return self.sampler()


if __name__ == "__main__":
    acs = Space([Dimension()], ["a"])
    print(acs, acs.decimal_granularity, acs.shape, acs.span)

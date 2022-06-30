#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from trolls.spaces import Dimension

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/09/2019
           """


def test_1():
    r = Dimension(min_value=0, max_value=5, decimal_granularity=2)
    print(r, r.sample())


def test_11():
    r = Dimension(min_value=0, max_value=2, decimal_granularity=0, normalised=False)
    print(r.span, r.sample(), r.discrete_steps, r.max, r.min)

    a = 2
    assert a == r.denormalise(r.normalise(a))

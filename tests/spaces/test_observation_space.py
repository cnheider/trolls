#!/usr/bin/env python3
# -*- coding: utf-8 -*-


__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 15/09/2019
           """

from trolls.spaces import Dimension, SignalSpace


def test1():
    acs = SignalSpace([Dimension(min_value=0, max_value=3, decimal_granularity=2)], ())
    print(acs, acs.low, acs.high, acs.decimal_granularity)


def test_sparsity():
    acs = SignalSpace([Dimension(min_value=0, max_value=3, decimal_granularity=0)], ())

    assert acs.is_sparse

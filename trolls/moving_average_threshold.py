#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 03-04-2021
           """
__all__ = ["ma_stop"]

from warg import Number


def ma_stop(solved_threshold: Number = 10) -> callable:
    """

    :param solved_threshold:
    :return:"""

    def ma_threshold(ma: Number) -> bool:
        """

        :param ma:
        :type ma:
        :return:
        :rtype:
        """
        return ma >= solved_threshold

    return ma_threshold


if __name__ == "__main__":
    stopping_condition = ma_stop(10)

    print(stopping_condition(1))
    print(stopping_condition(11))

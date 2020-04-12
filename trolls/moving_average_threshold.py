#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"


def ma_stop(solved_threshold: float = 10):
    """

  :param solved_threshold:
  :return:
  """

    def ma_threshold(ma: float):
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

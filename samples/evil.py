#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 02/02/2020
           """

if __name__ == "__main__":

    import random

    class Evil(object):
        """"""

        def __bool__(self) -> bool:
            return random.random() > 0.5

        def __repr__(self) -> bool:
            return bool(self)

        def __str__(self) -> str:
            return str(self.__repr__())

    true, false = Evil(), Evil()

    print(true, false)

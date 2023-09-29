#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from warg import package_is_editable, get_version, clean_string

try:
    from importlib.resources import files
    from importlib.metadata import PackageNotFoundError
except:
    from importlib_metadata import PackageNotFoundError
    from importlib_resources import files

from apppath import AppPath

__project__ = "Trolls"
__author__ = "Christian Heider Nielsen"
__version__ = "0.4.0"
__doc__ = r"""
Created on 27/04/2019

@author: cnheider
"""
__all__ = ["PROJECT_APP_PATH", "PROJECT_NAME", "PROJECT_VERSION"]

PROJECT_NAME = clean_string(__project__)
PROJECT_VERSION = __version__
PROJECT_YEAR = 2019
PROJECT_ORGANISATION = clean_string("Neodroid")
PROJECT_AUTHOR = clean_string(__author__)
PROJECT_APP_PATH = AppPath(app_name=PROJECT_NAME, app_author=PROJECT_AUTHOR)
PACKAGE_DATA_PATH = files(PROJECT_NAME) / "data"
INCLUDE_PROJECT_READMES = False

try:
    DEVELOP = package_is_editable(PROJECT_NAME)
except PackageNotFoundError as e:
    DEVELOP = True

__version__ = get_version(__version__, append_time=DEVELOP)

__version_info__ = tuple(int(segment) for segment in __version__.split("."))

# from .multiple_environments_wrapper import *
# from .moving_average_threshold import *
# from .gym_wrappers import *

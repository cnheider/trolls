#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = "heider"
__doc__ = r"""

           Created on 12/15/22
           """

import gym
from pynput import keyboard

from trolls.render_mode import RenderModeEnum


def up() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["z"] = 1


def down() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["z"] = -1


def left() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["x"] = -1


def right() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["x"] = 1


def backward() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["y"] = -1


def forward() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["y"] = 1


def reset() -> None:
    """

    :return:
    :rtype:
    """
    ACTION_SET["halt"] = 1


def listen_for_combinations():
    """

    :return:
    :rtype:
    """
    print(f"\n\nPress any of:\n{COMBINATIONS}\n\n")
    print("")
    return keyboard.Listener(on_press=on_press, on_release=on_release)


def on_press(key):
    """

    :param key:
    :type key:
    """
    if any([key in COMBINATIONS]):
        if key not in CURRENT_COMBINATIONS:
            CURRENT_COMBINATIONS.add(key)


def on_release(key):
    """

    :param key:
    :type key:
    """
    global ACTION_SET
    if any([key in COMBINATIONS]):
        if key in CURRENT_COMBINATIONS:
            CURRENT_COMBINATIONS.remove(key)
    if len(CURRENT_COMBINATIONS) == 0:
        ACTION_SET = ACTION_SET_RESET.copy()


def wrapped_exit():
    listener.stop()
    exit()


COMBINATIONS = {
    keyboard.KeyCode(char="q"): down,
    keyboard.KeyCode(char="Q"): down,
    keyboard.KeyCode(char="w"): forward,
    keyboard.KeyCode(char="W"): forward,
    keyboard.KeyCode(char="e"): up,
    keyboard.KeyCode(char="E"): up,
    keyboard.KeyCode(char="a"): right,
    keyboard.KeyCode(char="A"): right,
    keyboard.KeyCode(char="s"): backward,
    keyboard.KeyCode(char="S"): backward,
    keyboard.KeyCode(char="d"): left,
    keyboard.KeyCode(char="D"): left,
    keyboard.KeyCode(char="x"): wrapped_exit,
    keyboard.KeyCode(char="X"): wrapped_exit,
    keyboard.KeyCode(char="r"): reset,
    keyboard.KeyCode(char="R"): reset,
}

ACTION_SET = {"x": 0, "y": 0, "z": 0, "halt": 0}
ACTION_SET_RESET = ACTION_SET.copy()

ENVIRONMENT = gym.make("LunarLander")  # TODO: VectorWrap
ENVIRONMENT.reset()

CURRENT_COMBINATIONS = set()  # The currently active modifiers
STEP_I = 0
AUTO_RESET = False
RENDER = True
listener = listen_for_combinations()


def to_action(action_set):
    if action_set["x"] == 1:
        # if action_set['y'] == 1:
        #  return 4
        return 1
    if action_set["x"] == -1:
        # if action_set['y'] == 1:
        #  return 5
        return 3
    if action_set["y"] == 1:
        return 2

    return 0


def main():
    """"""
    global STEP_I

    listener.start()
    a = None
    while 1:  # ACTION_SET['halt']!=-1: # should not be necessary
        terminated = False
        signal = 0

        [COMBINATIONS[c]() for c in CURRENT_COMBINATIONS]

        if ACTION_SET["halt"] == 1:
            obs = ENVIRONMENT.reset()
            STEP_I = 0
        else:
            a = to_action(ACTION_SET)
            obs, signal, terminated, _ = ENVIRONMENT.step(a)
        if RENDER:
            ENVIRONMENT.render(RenderModeEnum.human.value)
        STEP_I += 1
        print(STEP_I, obs, signal, terminated)

        if AUTO_RESET and terminated:
            ENVIRONMENT.reset()
            STEP_I = 0


if __name__ == "__main__":
    main()

import typing
import enum
import pygame as pg


class SymmetryType(enum.IntEnum):
    NoSymmetry = (0,)
    Horizontal = (1,)
    Vertical = (2,)


class KeyBinding:
    def __init__(self, keycode: int, group: str, func: typing.Callable, on_pressed=False):
        self.keycode = keycode
        self.group = group
        self.func = func
        self.on_pressed = on_pressed

    def __str__(self):
        return f"(keycode={pg.key.name(self.keycode)}, group={self.group})"

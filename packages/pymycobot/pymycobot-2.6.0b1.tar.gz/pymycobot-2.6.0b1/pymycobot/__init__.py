# coding=utf-8

from __future__ import absolute_import
import datetime

from pymycobot.mycobot import MyCobot
from pymycobot.generate import MycobotCommandGenerater
from pymycobot.genre import Angle, Coord
from pymycobot import utils

__all__ = ["MyCobot", "MycobotCommandGenerater", "Angle", "Coord", "utils"]

__version__ = "2.6.0.beta.1"
__author__ = "Zachary zhang"
__email__ = "lijun.zhang@elephantrobotics.com"
__git_url__ = "https://github.com/elephantrobotics/pymycobot"
__copyright__ = "CopyRight (c) 2020-{0} Shenzhen Elephantrobotics technology".format(
    datetime.datetime.now().year
)

# For raspberry mycobot 280.
PI_PORT = "/dev/ttyAMA0"
PI_BAUD = 1000000

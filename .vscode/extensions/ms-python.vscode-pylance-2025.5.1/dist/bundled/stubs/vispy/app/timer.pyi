# Copyright (c) Vispy Development Team. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
from typing import Any

from . import Application
from .base import BaseTimerBackend as TimerBackend  # noqa

class Timer:
    def __init__(self, interval=..., connect=..., iterations=..., start=..., app=...) -> None: ...
    @property
    def app(self) -> Application: ...
    @property
    def interval(self) -> float: ...
    @interval.setter
    def interval(self, val) -> None: ...
    @property
    def elapsed(self) -> float: ...
    @property
    def running(self) -> bool: ...
    def start(self, interval=..., iterations=...) -> None: ...
    def stop(self) -> None: ...
    @property
    def native(self) -> Any: ...
    def connect(self, callback): ...
    def disconnect(self, callback=...): ...

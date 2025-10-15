from dataclasses import dataclass as component
from typing import Tuple, Union

@component
class Position():
    x: float
    y: float

@component
class Velocity():
    speed: float
    dx: float
    dy: float

@component
class PrevPosition():
    px: float
    py: float

@component
class StarRenderDetails():
    color: Union[Tuple[int, int, int], str]
    width: int

import math
import random
from typing import Tuple

import esper

from starfield_sim.components import Position, PrevPosition, StarRenderDetails, Velocity
from starfield_sim import constants



def find_initial_position(screen_width, screen_height) -> Tuple[float, float]:
    # IDEA: move center based in user input
    cx = screen_width / 2
    cy = screen_height / 2
    cr = (screen_width *.8)**2
    x = random.randint(1, screen_width - 1)
    y = random.randint(1, screen_height -1)
    attempt_counts = 0
    def is_valid(attempt_x, attempt_y):
        dx = attempt_x - cx
        dy = attempt_y - cy
        return dx**2 + dy**2 < cr
    while not is_valid(x, y) or attempt_counts < 100:
        x = random.randint(1, screen_width - 1)
        y = random.randint(1, screen_height -1)
        attempt_counts += 1
    return x, y

def find_initial_velocity(x: float, y: float, screen_width, screen_height) -> Tuple[float, float]:
    # IDEA: move center based in user input
    cx = screen_width / 2
    cy = screen_height / 2

    dx = x - cx
    dy = y - cy
    length = math.hypot(dx, dy)
    if length == (0,0):
        return (0,0)
    return (dx / length), (dy / length), constants.SPEED_MIN

def init_star(screen_width, screen_height):
    ent = esper.create_entity()
    x, y = find_initial_position(screen_width, screen_height)
    esper.add_component(ent, Position(x=x, y=y))
    dx, dy, speed = find_initial_velocity(x, y, screen_width, screen_height)
    esper.add_component(ent, Velocity(dx=dx, dy=dy, speed=speed))
    esper.add_component(ent, PrevPosition(x, y))
    color = constants.STAR_COLORS[ random.randint(0, len(constants.STAR_COLORS)-1)]
    width = 3
    esper.add_component(ent, StarRenderDetails(color=color, width=width))
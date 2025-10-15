import math

import esper
import pygame

from starfield_sim import constants
from starfield_sim.components import Position, PrevPosition, StarRenderDetails, Velocity
from starfield_sim import entities


class MovementProcessor(esper.Processor):
    def process(self, dt: float):
        for _ent, (pos, vel, pre_pos) in esper.get_components(Position, Velocity, PrevPosition):
            pre_pos.px = pos.x
            pre_pos.py = pos.y
            pos.x += vel.dx * vel.speed * dt
            pos.y += vel.dy * vel.speed * dt

class BoundsProcessor(esper.Processor):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
    def process(self, _dt: float):
        
        width, height = self.screen.get_size()
        for ent, (pos) in esper.get_component(Position):
            if pos.x <= 0 \
                or pos.x >= width \
                or pos.y <= 0 \
                or pos.y >= height:
                esper.delete_entity(ent)
                entities.init_star(self.screen.get_width(), self.screen.get_height())

class RenderProcessor(esper.Processor):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
    
    def process(self, _dt: float):
        for _ent, (pos, pre_pos, detail) in esper.get_components(Position, PrevPosition, StarRenderDetails):
            start_pos = (pre_pos.px, pre_pos.py)
            end_pos = (pos.x, pos.y)
            pygame.draw.line(self.screen,
                             color=detail.color,
                             start_pos=start_pos,
                             end_pos=end_pos,
                             width=detail.width)

class VelocityUpdateProcessor(esper.Processor):
    def __init__(self, screen: pygame.Surface):
        super().__init__()
        self.screen = screen
    def process(self, _dt: float):
        # IDEA: move center based in user input
        width, height = self.screen.get_size()
        cx = width // 2
        cy = height // 2
        max_dist = math.hypot(cx, cy) # cener to top left corner
        for _ent, (pos, _detail, vel) in esper.get_components(Position, StarRenderDetails, Velocity):
            dx = pos.x - cx
            dy = pos.y - cy
            dist_center = math.hypot(dx, dy)
            ratio = max(0, min(dist_center / max_dist, 1))
            vel.speed = constants.SPEED_MIN  + (constants.SPEED_MAX - constants.SPEED_MIN) * ratio



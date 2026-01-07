"""Snowfall effects for winter season"""
import math
from random import randint, uniform
from OpenGL.GL import *
from ..config import (
    WINDOW_SIZE, SNOWFLAKE_COUNT, SNOWFLAKE_SIZE_RANGE,
    SNOWFLAKE_SPEED_RANGE, SNOW_COLOR
)


class Snowflake:
    """Single falling snowflake"""
    def __init__(self):
        self.reset(random_x=True)

    def reset(self, random_x=False):
        if random_x:
            self.x = randint(0, WINDOW_SIZE[0])
        # Start slightly above the visible area
        self.y = -randint(0, 100)
        self.size = randint(*SNOWFLAKE_SIZE_RANGE)
        self.speed = uniform(*SNOWFLAKE_SPEED_RANGE)
        # Gentle horizontal drift
        self.drift = uniform(-0.3, 0.3)

    def update(self):
        self.y += self.speed
        self.x += self.drift
        if self.x < -10:
            self.x = WINDOW_SIZE[0] + 10
        elif self.x > WINDOW_SIZE[0] + 10:
            self.x = -10
        # Reset when it goes past the bottom
        if self.y > WINDOW_SIZE[1] + 10:
            self.reset(random_x=True)

    def draw(self):
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_POLYGON)
        glColor4f(*SNOW_COLOR)
        # Draw as a small circle
        segments = 12
        r = self.size
        for i in range(segments):
            angle = 2 * math.pi * i / segments
            cx = self.x + r * math.cos(angle)
            cy = self.y + r * math.sin(angle)
            glVertex2f(cx, cy)
        glEnd()
        glDisable(GL_BLEND)


class Snowfall:
    """Manager for multiple snowflakes"""
    def __init__(self):
        self.flakes = [Snowflake() for _ in range(SNOWFLAKE_COUNT)]
        # Randomize starting positions across the screen
        for f in self.flakes:
            f.x = randint(0, WINDOW_SIZE[0])
            f.y = randint(-WINDOW_SIZE[1] // 2, WINDOW_SIZE[1] // 2)

    def draw(self):
        for f in self.flakes:
            f.draw()
            f.update()

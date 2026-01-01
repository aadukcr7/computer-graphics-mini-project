"""Natural elements: Grass and Fireflies"""
from random import randint, choices, uniform
from OpenGL.GL import *
from ..config import (
    WINDOW_SIZE, GRASS_LENGTH, GRASS_DAY_COLOR, GRASS_NIGHT_COLOR,
    FIREFLY_RANGE
)


class Grass:
    """Individual grass blade that sways"""
    def __init__(self, x, y, points):
        self.breakpoints = [0] + [x for x in choices(range(GRASS_LENGTH // points), k=points)]
        self.sway = [randint(-1, 1) for _ in range(points)]
        self.x, self.y = x, y
        self.color = GRASS_NIGHT_COLOR

    def breeze(self):
        """TODO: Implement wind effect"""
        pass

    def draw(self):
        glLineWidth(4.0)  # Make grass lines thicker
        glBegin(GL_LINE_STRIP)  # Draw connected grass blade
        glColor3f(*self.color)
        x, y = self.x, self.y
        glVertex2f(x, y)  # Start point at ground (bottom)
        for b, s in zip(self.breakpoints, self.sway):
            x += s
            y -= b  # Grass grows upward (decreasing y in screen coords)
            glVertex2f(x, y)
        glEnd()
        glLineWidth(1.0)  # Reset line width

    def switch_time(self, time):
        self.color = GRASS_NIGHT_COLOR if time == "night" else GRASS_DAY_COLOR


class Firefly:
    """Flying firefly with random movement"""
    def __init__(self, x, y, draw=True):
        self.x, self.y = x, y
        self.speed = uniform(0.002, 0.08)  # Slower movement
        self.xi = randint(0, 1)
        self.yi = randint(0, 1)
        self.entropy = randint(3, 7)
        self.pointsize = 2
        self.color = (0.63, 0.615, 0.357)
        self._draw = draw

    def fly(self):
        """Random firefly movement"""
        if self.x >= FIREFLY_RANGE[0][1]:
            self.xi = 0
        elif self.x <= FIREFLY_RANGE[0][0]:
            self.xi = 1

        if self.y >= FIREFLY_RANGE[1][1]:
            self.yi = 0
        elif self.y <= FIREFLY_RANGE[1][0]:
            self.yi = 1

        if self.entropy < 0:
            self.xi = randint(0, 1)
            self.yi = randint(0, 1)
            self.entropy = randint(3, 7)
            self.speed = uniform(0.002, 0.08)  # Slower movement
            self.color = (0.68, 0.655, 0.407)
            self.pointsize = 4
        else:
            self.entropy -= 0.01
            if self.pointsize > 2:
                self.pointsize -= 0.1
                self.color = tuple(map(lambda m: m - 0.0025, self.color))
        
        self.x += +self.speed if self.xi else -self.speed
        self.y += +self.speed if self.yi else -self.speed

    def draw(self):
        if self._draw:
            glColor3f(*self.color)
            glPointSize(self.pointsize)
            glBegin(GL_POINTS)
            glVertex2f(self.x, self.y)
            glEnd()
            self.fly()

    def switch_time(self, time):
        self._draw = True if time == "night" else False
        self.color = (0.63, 0.655, 0.407) if time == "night" else (0.1, 0.1, 0.1)

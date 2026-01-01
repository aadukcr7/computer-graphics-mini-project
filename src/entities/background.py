"""Background gradient rendering"""
from OpenGL.GL import *
from ..config import WINDOW_SIZE, GRADIENT_STEPS, NIGHT_SKY, DAY_SKY


class Background:
    def __init__(self):
        self.width, self.height = WINDOW_SIZE
        self.color = DAY_SKY  # Start with day sky
        self.bright = 0.5
        self.switching = False

    def draw(self):
        glBegin(GL_QUADS)
        h = self.height / GRADIENT_STEPS
        g = self.color[1] / GRADIENT_STEPS
        b = self.color[2] / GRADIENT_STEPS
        for i in range(1, GRADIENT_STEPS + 1):
            glColor3f(
                self.color[0],
                self.color[1] - i * g * self.bright,
                self.color[2] - i * b * self.bright
            )
            glVertex2f(0, h * i)
            glVertex2f(self.width, h * i)
            glVertex2f(self.width, h * (i - 1))
            glVertex2f(0, h * (i - 1))
        glEnd()

    def switch_time(self, time):
        self.bright = 1 if time == "night" else 0.5

    def brighten(self, g, b):
        if g < DAY_SKY[1]:
            g += 0.002
        if b < DAY_SKY[2]:
            b += 0.002
        return g, b

    def darken(self, g, b):
        if g > NIGHT_SKY[1]:
            g -= 0.01
        if b > NIGHT_SKY[2]:
            b -= 0.01
        return g, b

    def change_brightness(self, sun, time, seconds, transition_progress=0):
        import math
        r, g, b = self.color
        if time == "day":
            # Brightness based on sun's angle position (0 to π)
            brightness_factor = math.sin(sun.angle)
            
            # Interpolate between night and day colors based on sun position
            night_r, night_g, night_b = NIGHT_SKY
            day_r, day_g, day_b = DAY_SKY
            
            r = night_r + (day_r - night_r) * brightness_factor
            g = night_g + (day_g - night_g) * brightness_factor
            b = night_b + (day_b - night_b) * brightness_factor
            
            self.bright = brightness_factor
        else:
            # During night transition, gradually darken
            # Use transition_progress for smooth fade
            night_r, night_g, night_b = NIGHT_SKY
            day_r, day_g, day_b = DAY_SKY
            
            # Interpolate from current day color to night color based on transition progress
            r = day_r + (night_r - day_r) * transition_progress
            g = day_g + (night_g - day_g) * transition_progress
            b = day_b + (night_b - day_b) * transition_progress
            
            self.bright = 1
        
        self.color = r, g, b

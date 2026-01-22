"""Ground/grass base"""
from OpenGL.GL import *
from ..config import (
    WINDOW_SIZE, GRASS_DAY_COLOR, GRASS_NIGHT_COLOR,
    SNOW_COVER_HEIGHT, SNOW_COLOR, SNOW_COVER_OPACITY_DAY, SNOW_COVER_OPACITY_NIGHT
)


class Ground:
    """Green ground at the bottom of the screen"""
    def __init__(self):
        self.width, self.height = WINDOW_SIZE
        self.day_color = GRASS_DAY_COLOR      # Bright green for day
        self.night_color = GRASS_NIGHT_COLOR  # Very dark green for night
        self.current_color = self.day_color  # Start with day color
        self.ground_height = 300  # Height of ground from bottom
        self.snow_enabled = False
        self.snow_cover_opacity = SNOW_COVER_OPACITY_DAY  # Start with day opacity

    def draw(self):
        """Draw solid ground rectangle"""
        glBegin(GL_POLYGON)
        glColor3f(*self.current_color)
        
        # Draw rectangle from bottom to ground_height
        glVertex2f(0, self.height)
        glVertex2f(self.width, self.height)
        glVertex2f(self.width, self.height - self.ground_height)
        glVertex2f(0, self.height - self.ground_height)
        
        glEnd()

        # Optional snow cap overlay for winter
        if self.snow_enabled:
            self._draw_snow_cover()

    def _draw_snow_cover(self):
        """Draw a white snow overlay covering the entire ground in winter."""
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        top_y = self.height - self.ground_height
        cover_h = self.ground_height

        glBegin(GL_POLYGON)
        # Use current snow cover opacity
        glColor4f(SNOW_COLOR[0], SNOW_COLOR[1], SNOW_COLOR[2], self.snow_cover_opacity)
        # Full ground coverage
        glVertex2f(0, top_y)
        glVertex2f(self.width, top_y)
        glVertex2f(self.width, top_y + cover_h)
        glVertex2f(0, top_y + cover_h)
        glEnd()

        glDisable(GL_BLEND)

    def change_brightness(self, sun, time, seconds, transition_progress=0):
        """Change ground color based on time of day"""
        import math
        
        if time == "day":
            # During day, ground gets brighter as sun rises
            sun_height = max(0.0, math.sin(sun.angle))
            
            # Interpolate between night and day colors
            r = self.night_color[0] + (self.day_color[0] - self.night_color[0]) * sun_height
            g = self.night_color[1] + (self.day_color[1] - self.night_color[1]) * sun_height
            b = self.night_color[2] + (self.day_color[2] - self.night_color[2]) * sun_height
            
            self.current_color = (r, g, b)
        else:
            # During night, stay dark unless mid-transition
            t = transition_progress if transition_progress > 0 else 1.0
            r = self.day_color[0] + (self.night_color[0] - self.day_color[0]) * t
            g = self.day_color[1] + (self.night_color[1] - self.day_color[1]) * t
            b = self.day_color[2] + (self.night_color[2] - self.day_color[2]) * t
            
            self.current_color = (r, g, b)

    def switch_time(self, time):
        """Switch between day and night colors and snow opacity"""
        if time == "day":
            self.current_color = self.day_color
            self.snow_cover_opacity = SNOW_COVER_OPACITY_DAY
        else:
            self.current_color = self.night_color
            self.snow_cover_opacity = SNOW_COVER_OPACITY_NIGHT

    def enable_snow(self, enabled=True):
        """Enable/disable snow cover overlay (winter season)."""
        self.snow_enabled = bool(enabled)

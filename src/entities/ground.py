"""Ground/grass base"""
from OpenGL.GL import *
from ..config import WINDOW_SIZE


class Ground:
    """Green ground at the bottom of the screen"""
    def __init__(self):
        self.width, self.height = WINDOW_SIZE
        self.day_color = (0.2, 0.6, 0.2)      # Bright green for day
        self.night_color = (0.01, 0.03, 0.02)  # Very dark green for night
        self.current_color = self.day_color  # Start with day color
        self.ground_height = 300  # Height of ground from bottom

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

    def change_brightness(self, sun, time, seconds, transition_progress=0):
        """Change ground color based on time of day"""
        import math
        
        if time == "day":
            # During day, ground gets brighter as sun rises
            sun_height = math.sin(sun.angle)
            
            # Interpolate between night and day colors
            r = self.night_color[0] + (self.day_color[0] - self.night_color[0]) * sun_height
            g = self.night_color[1] + (self.day_color[1] - self.night_color[1]) * sun_height
            b = self.night_color[2] + (self.day_color[2] - self.night_color[2]) * sun_height
            
            self.current_color = (r, g, b)
        else:
            # During night transition, gradually darken ground
            r = self.day_color[0] + (self.night_color[0] - self.day_color[0]) * transition_progress
            g = self.day_color[1] + (self.night_color[1] - self.day_color[1]) * transition_progress
            b = self.day_color[2] + (self.night_color[2] - self.day_color[2]) * transition_progress
            
            self.current_color = (r, g, b)

    def switch_time(self, time):
        """Switch between day and night colors"""
        if time == "day":
            self.current_color = self.day_color
        else:
            self.current_color = self.night_color

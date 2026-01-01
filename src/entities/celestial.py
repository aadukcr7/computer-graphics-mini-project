"""
Celestial Bodies Module
Contains Sun, Moon, Star, and Cloud classes for the day-night simulation
"""
import math
from random import randint, uniform
from OpenGL.GL import *
from ..config import (
    WINDOW_SIZE, SUN_RADIUS, SUN_POSITION, SUN_COLOR,
    MOON_RADIUS, MOON_POSITION, MOON_COLOR
)

# Celestial movement constants
SUN_STEP = 0.0008
MOON_STEP = 0.0005
ORBIT_CENTER_X = WINDOW_SIZE[0] // 2
ORBIT_CENTER_Y = WINDOW_SIZE[1] // 3
ORBIT_RADIUS_X = 500
ORBIT_RADIUS_Y = 300

# Fade animation constants
FADE_INCREMENT = 0.02


class HeavenlyBody:
    """Base class for all celestial objects"""
    
    def __init__(self, radius, position, color, draw=True):
        """Initialize a celestial body
        
        Args:
            radius: Size of the body
            position: (x, y) coordinates
            color: (r, g, b) color tuple
            draw: Whether the body should be initially visible
        """
        self.radius = radius
        self.x, self.y = position
        self.color = (*color, 0.0)
        self._draw = draw
    
    def draw(self):
        """Draw the celestial body with glow effect"""
        if self._draw:
            self.shine()
            self.draw_body()
    
    def draw_body(self):
        """Draw solid body"""
        glBegin(GL_POLYGON)
        for i in range(360):
            glColor4f(*self.color)
            cosine = self.radius * math.cos(i) + self.x
            sine = self.radius * math.sin(i) + self.y
            glVertex2f(cosine, sine)
        glEnd()
    
    def shine(self):
        """Draw glowing halo around the body"""
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glBegin(GL_POLYGON)
        glColor4f(*self.color[:3], 0.3 * self.color[-1])
        
        for i in range(360):
            cosine = (self.radius * 1.5) * math.cos(i) + self.x
            sine = (self.radius * 1.5) * math.sin(i) + self.y
            glVertex2f(cosine, sine)
        glEnd()
    
    def switch_time(self):
        """Toggle visibility"""
        self._draw = not self._draw
    
    def appear(self):
        """Fade in the celestial body"""
        r, g, b, a = self.color
        if a <= 1.0:
            a += FADE_INCREMENT
        self.color = r, g, b, a
    
    def disappear(self, speed=1):
        """Fade out the celestial body"""
        r, g, b, a = self.color
        if a >= 0.0:
            a -= FADE_INCREMENT * speed
        self.color = r, g, b, a


class Sun(HeavenlyBody):
    """The sun that revolves across the sky during the day"""
    
    def __init__(self, radius, position, color, draw):
        """Initialize the sun"""
        super().__init__(radius, position, color, draw)
        self.angle = 0
        self.step = SUN_STEP
    
    def revolve(self):
        """Move the sun along its arc path
        
        Returns:
            True when the sun completes its full arc, False otherwise
        """
        # Calculate position on arc
        self.x = ORBIT_CENTER_X + ORBIT_RADIUS_X * math.cos(math.pi + self.angle)
        self.y = ORBIT_CENTER_Y - ORBIT_RADIUS_Y * math.sin(self.angle)
        
        self.angle += self.step
        
        # Check if arc is complete
        if self.angle >= math.pi:
            self.angle = 0
            return True
        
        return False
    
    def change_brightness(self, sun, time, seconds):
        """Update sun brightness based on time of day"""
        if time == "day":
            # Brightness curve: sin(angle)^1.5 for steep brightness changes
            brightness = math.sin(self.angle) ** 1.5
            r, g, b = SUN_COLOR
            self.color = (r, g, b, brightness)
        else:
            # Fade out during night
            self.disappear()


class Moon(HeavenlyBody):
    """The moon that revolves across the sky during the night"""
    
    def __init__(self, radius, position, color):
        """Initialize the moon"""
        super().__init__(radius, position, color)
        self.angle = 0
        self.step = MOON_STEP
    
    def revolve(self):
        """Move the moon along its arc path
        
        Returns:
            True when the moon completes its full arc, False otherwise
        """
        # Calculate position on arc (same as sun)
        self.x = ORBIT_CENTER_X + ORBIT_RADIUS_X * math.cos(math.pi + self.angle)
        self.y = ORBIT_CENTER_Y - ORBIT_RADIUS_Y * math.sin(self.angle)
        
        self.angle += self.step
        
        # Check if arc is complete
        if self.angle >= math.pi:
            self.angle = 0
            return True
        
        return False
    
    def change_brightness(self, sun, time, seconds):
        """Update moon brightness based on time of day"""
        if time == "day":
            # Fade out during day
            self.disappear()
        else:
            # Brightness curve: sin(angle)^1.5 for steep brightness changes
            brightness = math.sin(self.angle) ** 1.5
            r, g, b = MOON_COLOR
            self.color = (r, g, b, brightness)


class Star:
    """Twinkling star visible at night"""
    
    def __init__(self, x, y, draw=True):
        """Initialize a star
        
        Args:
            x, y: Star position
            draw: Initial visibility
        """
        self.x, self.y = x, y
        self.width, self.height = WINDOW_SIZE
        self.size = randint(1, 3)
        self.i = True  # Direction indicator (growing/shrinking)
        self.step = uniform(0.0001, 0.005)
        self._draw = draw
    
    def twinkle(self):
        """Animate star twinkling effect"""
        if self.size >= 3 and self.i:
            self.i = False
            self.step = -self.step
        elif self.size <= 1 and not self.i:
            self.i = True
            self.step = -self.step
        
        self.size += self.step
    
    def draw(self):
        """Draw and animate the star"""
        if self._draw:
            glColor3f(1.0, 1.0, 1.0)
            glPointSize(self.size)
            glBegin(GL_POINTS)
            glVertex2f(self.x, self.y)
            glEnd()
            self.twinkle()
    
    def switch_time(self, time):
        """Show stars at night, hide during day"""
        self._draw = (time == "night")


class Cloud:
    """Drifting cloud element visible during day"""
    
    def __init__(self, x, y, size=1.0):
        """Initialize a cloud
        
        Args:
            x, y: Cloud position
            size: Scale factor for cloud size
        """
        self.x = x
        self.y = y
        self.size = size
        self.speed = uniform(0.02, 0.08) * size
        self.opacity = uniform(0.7, 0.9)
        self._draw = False  # Invisible at night
    
    def draw(self):
        """Draw and animate the cloud"""
        if self._draw:
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            
            # Draw cloud as overlapping circles
            cloud_color = (1.0, 1.0, 1.0, self.opacity)
            self._draw_cloud_puff(self.x, self.y, 30 * self.size, cloud_color)
            self._draw_cloud_puff(self.x + 25 * self.size, self.y - 5 * self.size, 35 * self.size, cloud_color)
            self._draw_cloud_puff(self.x + 50 * self.size, self.y, 30 * self.size, cloud_color)
            self._draw_cloud_puff(self.x + 25 * self.size, self.y + 10 * self.size, 25 * self.size, cloud_color)
            
            glDisable(GL_BLEND)
            
            # Move cloud horizontally
            self.x += self.speed
            if self.x > WINDOW_SIZE[0] + 100 * self.size:
                self.x = -100 * self.size
    
    def _draw_cloud_puff(self, x, y, radius, color):
        """Draw a single cloud puff (circle)
        
        Args:
            x, y: Center position
            radius: Circle radius
            color: RGBA color tuple
        """
        glBegin(GL_POLYGON)
        glColor4f(*color)
        for i in range(30):
            angle = 2 * math.pi * i / 30
            cx = x + radius * math.cos(angle)
            cy = y + radius * math.sin(angle)
            glVertex2f(cx, cy)
        glEnd()
    
    def switch_time(self, time):
        """Show clouds during day, hide at night"""
        self._draw = (time == "day")

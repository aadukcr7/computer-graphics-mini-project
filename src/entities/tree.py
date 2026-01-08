"""
Improved Pine Tree Structure
"""
from OpenGL.GL import *
from ..config import TREE_POSITION, TREE_TRUNK_COLOR, TREE_FOLIAGE_COLOR


class Tree:
    """Improved Pine/Conifer Tree"""

    def __init__(self, position=None):
        if position is None:
            position = TREE_POSITION
        self.x, self.y = position
        self.trunk_color = TREE_TRUNK_COLOR
        self.foliage_color = TREE_FOLIAGE_COLOR
        self.brightness = 1.0  # Start with full brightness for day
        self.is_night = False
        self.shadows_enabled = True

    def draw_trunk(self):
        """Draw slightly tapered trunk"""
        glColor3f(
            self.trunk_color[0] * self.brightness,
            self.trunk_color[1] * self.brightness,
            self.trunk_color[2] * self.brightness
        )
        glBegin(GL_POLYGON)

        glVertex2f(self.x - 12, self.y)
        glVertex2f(self.x + 12, self.y)
        glVertex2f(self.x + 8, self.y - 90)
        glVertex2f(self.x - 8, self.y - 90)

        glEnd()

    def draw_foliage_layer(self, top_y, width, height):
        """Draw a single triangular foliage layer"""
        glBegin(GL_TRIANGLES)
        glColor3f(
            self.foliage_color[0] * self.brightness,
            self.foliage_color[1] * self.brightness,
            self.foliage_color[2] * self.brightness
        )

        glVertex2f(self.x, top_y)
        glVertex2f(self.x - width, top_y + height)
        glVertex2f(self.x + width, top_y + height)

        glEnd()

    def draw_foliage(self):
        """Draw layered pine foliage"""
        self.draw_foliage_layer(self.y - 200, 40, 60)
        self.draw_foliage_layer(self.y - 150, 55, 70)

    def draw_shadow(self, sun_x, sun_y, sun_angle):
        """Draw shadow cast by tree based on sun position"""
        import math
        
        # Disable shadows globally when not enabled (e.g., winter season)
        if not self.shadows_enabled:
            return
        
        # Skip shadows entirely at night
        if self.is_night:
            return
        
        # Shadow only visible during day when sun is visible
        if sun_angle < 0 or sun_angle > math.pi:
            return
        
        # Tree dimensions
        tree_center_x = self.x
        tree_center_y = self.y - 100  # Middle of tree height
        tree_ground_y = self.y        # Base of tree
        
        # Sun height in the sky (0 to 1)
        sun_height = math.sin(sun_angle)
        
        # Don't draw shadow if sun is too low
        if sun_height < 0.05:
            return
        
        # Calculate horizontal distance and direction from tree to sun
        dx = sun_x - tree_center_x
        dy = sun_y - tree_center_y
        
        # Shadow direction: opposite of sun direction
        # Normalize and extend to create shadow
        distance = math.sqrt(dx * dx + dy * dy) + 1
        shadow_dx = -dx / distance * 300 * (1 - sun_height)
        shadow_dy = -dy / distance * 300 * (1 - sun_height)
        
        # Shadow extends on ground plane
        shadow_end_x = tree_center_x + shadow_dx
        shadow_end_y = tree_ground_y + abs(shadow_dy) * 0.3
        
        # Draw shadow
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glBegin(GL_POLYGON)
        glColor4f(0.0, 0.0, 0.0, 0.4)
        
        # Shadow base at tree (narrow)
        glVertex2f(self.x - 35, tree_ground_y)
        glVertex2f(self.x + 35, tree_ground_y)
        
        # Shadow tip (wider)
        glVertex2f(shadow_end_x + 50, shadow_end_y)
        glVertex2f(shadow_end_x - 50, shadow_end_y)
        
        glEnd()
        
        glDisable(GL_BLEND)
    
    def switch_time(self, time):
        """Adjust tree brightness based on time of day"""
        if time == "night":
            self.is_night = True
            self.brightness = 0.3  # Darker at night
        else:
            self.is_night = False
            self.brightness = 1.0  # Full brightness during day

    def set_shadows(self, enabled: bool):
        self.shadows_enabled = bool(enabled)

    def draw(self, sun=None):
        """Draw complete tree with shadow"""
        if sun is not None:
            self.draw_shadow(sun.x, sun.y, sun.angle)

        self.draw_foliage()
        self.draw_trunk()

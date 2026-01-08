"""House structure"""
import math
from OpenGL.GL import *
from ..config import HOUSE_POSITION, HOUSE_NIGHT_COLOR, HOUSE_DAY_COLOR


class House:
    """House with windows and door that change with day/night"""
    def __init__(self):
        self.x, self.y = HOUSE_POSITION
        self.window_color = HOUSE_DAY_COLOR  # Start with day color
        self.brightness = 1.0  # Start with full brightness for day
        self.is_night = False
        self.shadows_enabled = True

    def draw_layout(self):
        """House Structure"""
        glBegin(GL_POLYGON)
        glColor3f(121/255 * self.brightness, 172/255 * self.brightness, 179/255 * self.brightness)

        glVertex2f(self.x + 140, self.y + 120)
        glVertex2f(self.x + 140, self.y)
        glVertex2f(self.x, self.y)
        glVertex2f(self.x, self.y + 250)
        glVertex2f(self.x + 320, self.y + 250)
        glVertex2f(self.x + 320, self.y + 120)
        glVertex2f(self.x + 140, self.y + 120)
        glEnd()

        ### Garden
        glBegin(GL_POLYGON)
        glColor3f(0.32 * self.brightness, 0.5 * self.brightness, 0.27 * self.brightness)

        glVertex2f(self.x + 320, self.y + 250)
        glVertex2f(self.x, self.y + 250)
        glVertex2f(self.x - 15, self.y + 270)
        glVertex2f(self.x + 335, self.y + 270)
        glVertex2f(self.x + 320, self.y + 250)
        glEnd()

    def draw_roof(self):
        glBegin(GL_POLYGON)
        glColor3f(156/255 * self.brightness, 167/255 * self.brightness, 174/255 * self.brightness)

        glVertex2f(self.x - 5, self.y - 10)
        glVertex2f(self.x + 145, self.y - 10)
        glVertex2f(self.x + 145, self.y + 10)
        glVertex2f(self.x - 5, self.y + 10)
        glVertex2f(self.x - 5, self.y - 10)
        glEnd()

        glBegin(GL_POLYGON)
        glVertex(self.x - 5, self.y + 110)
        glVertex(self.x + 325, self.y + 110)
        glVertex(self.x + 335, self.y + 150)
        glVertex(self.x - 5, self.y + 150)
        glVertex(self.x - 5, self.y + 110)
        glEnd()

    def draw_window(self, x, y):
        glBegin(GL_POLYGON)
        glColor3f(*self.window_color)

        glVertex2f(x + 20, y)
        glVertex2f(x, y)
        glVertex2f(x, y + 40)
        glVertex2f(x + 20, y + 40)
        glVertex2f(x + 20, y)
        glEnd()

    def draw_frame(self, x, y, w, h):
        glBegin(GL_POLYGON)
        glColor3f(1, 1, 1)

        glVertex2f(x + w, y)
        glVertex2f(x, y)
        glVertex2f(x, y + h)
        glVertex2f(x + w, y + h)
        glVertex2f(x + w, y)
        glEnd()

    def draw_windows(self):
        self.draw_frame(self.x + 44, self.y + 38, 52, 48)
        x, y = 48, 42
        for _ in range(2):
            self.draw_window(self.x + x, self.y + y)
            x += 24

        self.draw_frame(self.x + 180, self.y + 166, 100, 48)
        x, y = 184, 170
        for _ in range(4):
            self.draw_window(self.x + x, self.y + y)
            x += 24

    def draw_door(self):
        glBegin(GL_POLYGON)
        glColor3f(146/255, 68/255, 27/255)

        glVertex2f(self.x + 90, self.y + 180)
        glVertex2f(self.x + 50, self.y + 180)
        glVertex2f(self.x + 50, self.y + 250)
        glVertex2f(self.x + 90, self.y + 250)
        glVertex2f(self.x + 90, self.y + 180)
        glEnd()

        # Door window (circular)
        glBegin(GL_POLYGON)
        glColor3f(1, 1, 1)
        x, y = self.x + 70, self.y + 200
        for i in range(360):
            cosine = 12 * math.cos(i) + x
            sine = 12 * math.sin(i) + y
            glVertex2f(cosine, sine)
        glEnd()

        glBegin(GL_POLYGON)
        glColor3f(*self.window_color)
        x, y = self.x + 70, self.y + 200
        for i in range(360):
            cosine = 10 * math.cos(i) + x
            sine = 10 * math.sin(i) + y
            glVertex2f(cosine, sine)
        glEnd()

    def draw_shadow(self, sun_x, sun_y, sun_angle):
        """Draw shadow cast by the house based on sun position"""
        import math
        
        # Disable shadows globally when not enabled (e.g., winter season)
        if not self.shadows_enabled:
            return
        
        if self.is_night:
            return
        
        # Shadow only visible during day when sun is visible
        if sun_angle < 0 or sun_angle > math.pi:
            return
        
        # House dimensions
        house_center_x = self.x + 160
        house_center_y = self.y + 125
        house_ground_y = self.y + 250
        
        # Sun height in the sky (0 to 1)
        sun_height = math.sin(sun_angle)
        
        # Don't draw shadow if sun is too low
        if sun_height < 0.05:
            return
        
        # Calculate horizontal distance and direction from house to sun
        dx = sun_x - house_center_x
        dy = sun_y - house_center_y
        
        # Shadow direction: opposite of sun direction
        # Normalize and extend to create shadow
        distance = math.sqrt(dx * dx + dy * dy) + 1
        shadow_dx = -dx / distance * 500 * (1 - sun_height)
        shadow_dy = -dy / distance * 500 * (1 - sun_height)
        
        # Shadow extends on ground plane
        shadow_end_x = house_center_x + shadow_dx
        shadow_end_y = house_ground_y + abs(shadow_dy) * 0.5
        
        # Draw shadow
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        glBegin(GL_POLYGON)
        glColor4f(0.0, 0.0, 0.0, 0.5)
        
        # Shadow base at house (wider)
        glVertex2f(self.x + 20, house_ground_y)
        glVertex2f(self.x + 300, house_ground_y)
        
        # Shadow tip (much wider)
        glVertex2f(shadow_end_x + 150, shadow_end_y)
        glVertex2f(shadow_end_x - 150, shadow_end_y)
        
        glEnd()
        
        glDisable(GL_BLEND)
        
        glDisable(GL_BLEND)

    def switch_time(self, time):
        self.window_color = HOUSE_NIGHT_COLOR if time == "night" else HOUSE_DAY_COLOR
        # Adjust brightness based on time
        if time == "night":
            self.is_night = True
            self.brightness = 0.3  # Darker at night
        else:
            self.is_night = False
            self.brightness = 1.0  # Full brightness during day

    def set_shadows(self, enabled: bool):
        self.shadows_enabled = bool(enabled)

    def draw(self, sun=None):
        self.draw_layout()
        self.draw_roof()
        if sun is not None:
            self.draw_shadow(sun.x, sun.y, sun.angle)
        self.draw_windows()
        self.draw_door()

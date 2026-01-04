"""
Scene Manager
Orchestrates all entities and manages the day-night cycle
"""
import math
from random import choices, uniform
from OpenGL.GL import *
from OpenGL.GLUT import *
from .entities import Background, Sun, Moon, Star, Cloud, Ground, Firefly, House, Tree
from .config import (
    WINDOW_SIZE, FIREFLY_RANGE, FIREFLY_COUNT, STAR_COUNT,
    MOON_RADIUS, MOON_POSITION, MOON_COLOR,
    SUN_RADIUS, SUN_POSITION, SUN_COLOR,
    TREE_POSITION_RIGHT, CLOUD_COUNT, CLOUD_X_RANGE, CLOUD_Y_RANGE, CLOUD_SIZE_RANGE
)

# Transition constants
TRANSITION_SPEED = 0.005
INITIAL_TIME = "day"

# Day/Night schedule (simulation hours)
# Sunrise at 06:00, sunset at 18:00 for a 12h/12h split
DAY_START = 6   # sunrise
DAY_END = 18    # sunset
DAY_SPAN = DAY_END - DAY_START  # 12 hours
NIGHT_START = DAY_END
NIGHT_SPAN = 24 - DAY_SPAN      # 12 hours


class Scene:
    """Main scene containing all visual elements and their interactions"""
    
    def __init__(self, hour=12):
        """Initialize all scene entities
        
        Args:
            hour: Hour of day (0-23), default is noon
        """
        self.wsize = WINDOW_SIZE
        self.time = INITIAL_TIME
        self.seconds = 86400
        self.current_hour = hour  # 0-23 format
        self.current_minute = 0
        self.is_paused = False  # Animation is active by default
        
        # Transition state variables
        self.transition_progress = 0.0
        self.is_transitioning = False
        
        # Initialize entities
        self._init_background()
        self._init_celestial_bodies()
        self._init_stars_and_fireflies()
        self._init_landscape()
        
        # Set initial state for all entities based on starting time
        self._set_time_of_day(hour)
    
    def _init_background(self):
        """Initialize background"""
        self.background = Background()
    
    def _init_celestial_bodies(self):
        """Initialize sun and moon"""
        import math
        
        self.moon = Moon(MOON_RADIUS, MOON_POSITION, MOON_COLOR)
        self.sun = Sun(SUN_RADIUS, SUN_POSITION, SUN_COLOR, draw=True)
        
        # Start sun at zenith (highest point) for bright day
        self.sun.angle = math.pi *0
        self.sun.revolve()  # Update position based on angle
    
    def _init_stars_and_fireflies(self):
        """Initialize stars and fireflies"""
        self.stars = [
            Star(x, y, draw=False) 
            for x, y in zip(
                choices(range(0, self.wsize[0]), k=STAR_COUNT),
                choices(range(0, 650), k=STAR_COUNT)
            )
        ]
        
        self.fireflies = [
            Firefly(x, y)
            for x, y in zip(
                choices(range(*FIREFLY_RANGE[0]), k=FIREFLY_COUNT),
                choices(range(*FIREFLY_RANGE[1]), k=FIREFLY_COUNT)
            )
        ]
    
    def _init_landscape(self):
        """Initialize clouds, ground, trees, and house"""
        self.clouds = [
            Cloud(x, y, size)
            for x, y, size in zip(
                choices(range(*CLOUD_X_RANGE), k=CLOUD_COUNT),
                choices(range(*CLOUD_Y_RANGE), k=CLOUD_COUNT),
                [uniform(*CLOUD_SIZE_RANGE) for _ in range(CLOUD_COUNT)]
            )
        ]
        
        self.ground = Ground()
        self.tree = Tree()
        self.tree_right = Tree(TREE_POSITION_RIGHT)
        self.house = House()
    
    def _set_time_of_day(self, hour):
        """Set the scene to a specific hour (0-23)
        
        Args:
            hour: Hour of day (0-23)
                  0 = midnight, 6 = sunrise, 12 = noon, 18 = sunset, 23 = late night
        """
        import math
        
        self.current_hour = hour % 24
        self.current_minute = 0
        
        # Determine if it's day or night using configured spans
        if DAY_START <= self.current_hour < DAY_END:
            self.time = "day"
            self.sun._draw = True
            self.moon._draw = False
            
            # Calculate sun angle: 0 at sunrise, pi at sunset
            hour_progress = (self.current_hour - DAY_START) / float(DAY_SPAN)
            self.sun.angle = hour_progress * math.pi
            self.sun.revolve()
            
            # Update brightness based on sun angle
            brightness = max(0, math.sin(self.sun.angle)) ** 1.5
            r, g, b = SUN_COLOR
            self.sun.color = (r, g, b, brightness)
        else:
            self.time = "night"
            self.moon._draw = True
            self.sun._draw = False
            
            # Calculate moon angle for night hours over a single NIGHT_SPAN arc
            night_progress = ((self.current_hour - NIGHT_START) % 24) / float(NIGHT_SPAN)
            # Map full night to a single π arc: NIGHT_START -> rise, NIGHT_START+NIGHT_SPAN -> set
            self.moon.angle = night_progress * math.pi
            self.moon.revolve()
            
            # Update brightness based on moon angle
            brightness = max(0, math.sin(self.moon.angle)) ** 1.5
            r, g, b = MOON_COLOR
            self.moon.color = (r, g, b, brightness)
        
        # Update all entities to match time of day
        self.background.switch_time(self.time)
        self.ground.switch_time(self.time)
        self.house.switch_time(self.time)
        self.tree.switch_time(self.time)
        self.tree_right.switch_time(self.time)
        
        for cloud in self.clouds:
            cloud.switch_time(self.time)
        
        for star in self.stars:
            star.switch_time(self.time)
        
        for firefly in self.fireflies:
            firefly.switch_time(self.time)
        
        # Update brightness of environment
        self._update_brightness()
    
    def draw(self):
        """Render all scene elements in proper order"""
        # Background and ground layers
        self.background.draw()
        self.ground.draw()
        
        # Stars in the sky (drawn early so objects can appear in front)
        for star in self.stars:
            star.draw()
        
        # Atmospheric elements
        for cloud in self.clouds:
            cloud.draw()
        
        # Landscape objects with shadows
        self.tree.draw(self.sun)
        self.tree_right.draw(self.sun)
        self.house.draw(self.sun)
        
        # Fireflies (near ground level, drawn after landscape)
        for firefly in self.fireflies:
            firefly.draw()
        
        # Celestial bodies (drawn last, on top of everything)
        self.moon.draw()
        self.sun.draw()
        
        # Update state (only if not paused)
        if not self.is_paused:
            self.time_elapse()
    


    
    def _draw_time_display(self):
        """Display time information via console output instead of on-screen rendering"""
        # Time display is shown in console when user changes time
        # This avoids OpenGL font rendering issues
        pass



    
    def time_elapse(self):
        """Handle time progression and transitions"""
        self._update_transition()
        self._update_celestial_bodies()
        self._update_brightness()
        self._sync_sim_time_from_angles()
        # Clock sync removed; simulation still updates celestial bodies
    
    def _update_transition(self):
        """Update transition state when switching between day and night"""
        if self.is_transitioning:
            self.transition_progress += TRANSITION_SPEED
            if self.transition_progress >= 1.0:
                self.transition_progress = 1.0
                self.is_transitioning = False
    
    def _update_celestial_bodies(self):
        """Update sun and moon positions and handle time transitions"""
        if self.time == "day":
            if self.sun.revolve():
                self.is_transitioning = True
                self.transition_progress = 0
                self.switch_time()
        else:
            if self.moon.revolve():
                self.is_transitioning = True
                self.transition_progress = 0
                self.switch_time()
    
    def _update_brightness(self):
        """Update colors of environment based on time of day"""
        self.background.change_brightness(
            self.sun, self.time, self.seconds, self.transition_progress
        )
        self.ground.change_brightness(
            self.sun, self.time, self.seconds, self.transition_progress
        )
        self.sun.change_brightness(self.sun, self.time, self.seconds)
        self.moon.change_brightness(self.sun, self.time, self.seconds)

    def _sync_sim_time_from_angles(self):
        """Map celestial angles to simulated clock time for accurate hour/minute tracking"""
        import math
        if self.time == "day":
            progress = max(0.0, min(1.0, self.sun.angle / math.pi))
            sim_hours = DAY_START + progress * DAY_SPAN
        else:
            progress = max(0.0, min(1.0, self.moon.angle / math.pi))
            sim_hours = NIGHT_START + progress * NIGHT_SPAN
            if sim_hours >= 24:
                sim_hours -= 24

        self.current_hour = int(sim_hours) % 24
        self.current_minute = int((sim_hours - int(sim_hours)) * 60)
    
    def switch_time(self):
        """Switch between day and night and update all entities"""
        self.time = "day" if self.time == "night" else "night"
        
        # Update environment
        self.background.switch_time(self.time)
        self.ground.switch_time(self.time)
        
        # Update all entities
        for star in self.stars:
            star.switch_time(self.time)
        
        for cloud in self.clouds:
            cloud.switch_time(self.time)
        
        for firefly in self.fireflies:
            firefly.switch_time(self.time)
        
        # Update celestial bodies
        self.moon.switch_time()
        self.sun.switch_time()
        
        # Update landscape objects
        self.house.switch_time(self.time)
        self.tree.switch_time(self.time)
        self.tree_right.switch_time(self.time)
    
    def set_hour(self, hour):
        """Set the scene to a specific hour (0-23)
        
        Args:
            hour: Hour of day (0-23)
        """
        if not 0 <= hour <= 23:
            print(f"Invalid hour: {hour}. Please use 0-23.")
            return False
        
        self._set_time_of_day(hour)
        return True

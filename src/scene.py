"""
Scene Manager
Orchestrates all entities and manages the day-night cycle
"""
from random import choices, uniform
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


class Scene:
    """Main scene containing all visual elements and their interactions"""
    
    def __init__(self):
        """Initialize all scene entities"""
        self.wsize = WINDOW_SIZE
        self.time = INITIAL_TIME
        self.seconds = 86400
        
        # Transition state variables
        self.transition_progress = 0.0
        self.is_transitioning = False
        
        # Initialize entities
        self._init_background()
        self._init_celestial_bodies()
        self._init_stars_and_fireflies()
        self._init_landscape()
        
        # Set initial state for all entities based on starting time
        self._set_initial_state()
    
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
    
    def _set_initial_state(self):
        """Set correct initial state for all entities based on starting time"""
        import math
        
        # Set initial brightness for sun/moon based on their starting angle
        if self.time == "day":
            # Initialize sun brightness
            brightness = math.sin(self.sun.angle) ** 1.5
            r, g, b = SUN_COLOR
            self.sun.color = (r, g, b, brightness)
            self.sun._draw = True
            
            # Hide moon during day
            self.moon._draw = False
            
            # Set day state for all entities
            self.background.switch_time("day")
            self.ground.switch_time("day")
            self.house.switch_time("day")
            self.tree.switch_time("day")
            self.tree_right.switch_time("day")
            
            for cloud in self.clouds:
                cloud.switch_time("day")
            
            for star in self.stars:
                star.switch_time("day")
            
            for firefly in self.fireflies:
                firefly.switch_time("day")
        else:
            # Initialize moon brightness
            brightness = math.sin(self.moon.angle) ** 1.5
            r, g, b = MOON_COLOR
            self.moon.color = (r, g, b, brightness)
            self.moon._draw = True
            
            # Hide sun during night
            self.sun._draw = False
            
            # Set night state for all entities
            self.background.switch_time("night")
            self.ground.switch_time("night")
            self.house.switch_time("night")
            self.tree.switch_time("night")
            self.tree_right.switch_time("night")
            
            for cloud in self.clouds:
                cloud.switch_time("night")
            
            for star in self.stars:
                star.switch_time("night")
            
            for firefly in self.fireflies:
                firefly.switch_time("night")
    
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
        
        # Update state
        self.time_elapse()
    
    def time_elapse(self):
        """Handle time progression and transitions"""
        self._update_transition()
        self._update_celestial_bodies()
        self._update_brightness()
    
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

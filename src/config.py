"""
Configuration Settings
Centralized constants for the entire simulation
"""

# ============================================================================
# WINDOW SETTINGS
# ============================================================================
WINDOW_SIZE = (1920, 1080)  # Full screen resolution
WINDOW_POSITION = (0, 0)     # Position at top-left corner
WINDOW_TITLE = b"Day - Night Transition Simulation"

# ============================================================================
# SEASON SETTINGS
# ============================================================================
# Choose between 'summer' and 'winter'. Default set to winter per request.
SEASON = "winter"

# Day schedule per season
SUMMER_DAY_START = 6
SUMMER_DAY_END = 18
WINTER_DAY_START = 6
WINTER_DAY_END = 20

# ============================================================================
# BACKGROUND & SKY COLORS
# ============================================================================
GRADIENT_STEPS = 100
NIGHT_SKY = (0, 0.005, 0.02)
DAY_SKY = (0.02, 0.46, 0.76)

# ============================================================================
# CELESTIAL BODIES - SUN
# ============================================================================
SUN_RADIUS = 60
SUN_POSITION = (-75, 150)
SUN_COLOR = (0.98, 0.89, 0.44)

# ============================================================================
# CELESTIAL BODIES - MOON
# ============================================================================
MOON_RADIUS = 40
MOON_POSITION = (980, 120)
MOON_COLOR = (0.88, 0.9, 0.89)

# ============================================================================
# STARS
# ============================================================================
STAR_COUNT = 100

# ============================================================================
# CLOUDS
# ============================================================================
CLOUD_COUNT = 5
CLOUD_X_RANGE = (-100, 1920)  # X position range
CLOUD_Y_RANGE = (50, 200)     # Y position range (upper sky area)
CLOUD_SIZE_RANGE = (0.8, 1.5) # Size scale factor range

# ============================================================================
# FIREFLIES
# ============================================================================
FIREFLY_RANGE = ((100, 1500), (800, 900))
FIREFLY_COUNT = 25

# ============================================================================
# GROUND
# ============================================================================
GRASS_LENGTH = 250
GRASS_DAY_COLOR = (0.2, 0.6, 0.2)
# Darker night grass; aligned to tree foliage at lower brightness (~0.2x)
GRASS_NIGHT_COLOR = (0.0267, 0.0926, 0.0267)

# ============================================================================
# LANDSCAPE OBJECTS - HOUSE
# ============================================================================
HOUSE_POSITION = (650, 530)
HOUSE_NIGHT_COLOR = (254/255, 198/255, 94/255)
HOUSE_DAY_COLOR = (145/255, 196/255, 231/255)

# ============================================================================
# LANDSCAPE OBJECTS - TREES
# ============================================================================
TREE_POSITION = (200, 800)
TREE_POSITION_RIGHT = (1350, 800)
TREE_TRUNK_COLOR = (101/255, 67/255, 33/255)
TREE_FOLIAGE_COLOR = (34/255, 139/255, 34/255)

# ============================================================================
# ANIMATION
# ============================================================================
ANIMATION_SPEED = 1.0

# ============================================================================
# TIME SCALING
# ============================================================================
# Controls how fast simulated time advances relative to real-time frames.
# 1.0 keeps previous speed, values <1 slow the cycle, >1 speed it up.
# Example: 0.2 makes the whole day-night cycle ~5x slower.
TIME_SCALE = 0.2

# ============================================================================
# SNOW (WINTER ONLY)
# ============================================================================
SNOWFLAKE_COUNT = 200
SNOWFLAKE_SIZE_RANGE = (1, 3)
SNOWFLAKE_SPEED_RANGE = (0.8, 2.0)  # pixels per frame
SNOW_COLOR = (1.0, 1.0, 1.0, 0.9)
SNOW_COVER_HEIGHT = 120  # thickness of ground snow cap

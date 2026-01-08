# Day-Night Transition Simulation

A comprehensive PyOpenGL-based graphics simulation that renders realistic day-night cycles with seasonal variations, dynamic lighting, shadows, and interactive time control.

## Overview

This project simulates a complete 24-hour day-night cycle with mathematical precision, featuring:
- **Realistic celestial mechanics** with sun and moon revolving along orbital arcs
- **Dynamic shadows** that follow sun position and adjust based on sun height
- **Seasonal variations** with shorter winter days (8h) and longer summer days (12h)
- **Smooth color transitions** between day and night
- **Interactive time control** allowing instant jumps to any hour
- **Complete landscape** with trees, house, clouds, stars, fireflies, and seasonal snow

## Requirements

- Python 3.8+
- OpenGL-capable GPU with driver support
- FreeGLUT/GLUT (typically included with PyOpenGL on Windows)

### Installation

```bash
pip install -r requirements.txt
```

## Running the Simulation

```bash
python main.py
```

You will be prompted to enter a starting hour (00-23). The window will open after input.

## Controls

| Key | Function |
|-----|----------|
| **H** | Display help menu (console output) |
| **S** | Toggle season (Summer ↔ Winter) |
| **00-23** | Jump to specific hour (type 2 digits, auto-processes) |
| **Q** | Quit simulation |

## Mathematical Formulas

### 1. Celestial Body Positioning

#### Sun Angle Calculation
```
DAY_PROGRESS = (current_hour - DAY_START) / DAY_SPAN
sun_angle = DAY_PROGRESS × π
```

Where:
- `DAY_START` = 6 (summer), 8 (winter)
- `DAY_SPAN` = 12 (summer), 8 (winter)
- **Range**: 0 to π radians (0° to 180°)

#### Moon Angle Calculation
```
NIGHT_PROGRESS = (current_hour - NIGHT_START) % 24 / NIGHT_SPAN
moon_angle = NIGHT_PROGRESS × π
```

Where:
- `NIGHT_START` = DAY_END
- `NIGHT_SPAN` = 24 - DAY_SPAN
- **Range**: 0 to π radians

#### Orbital Arc Position
```
x = center_x + radius × cos(angle)
y = center_y + radius × sin(angle)
```

### 2. Brightness and Lighting

#### Sun/Moon Brightness
```
brightness = max(0, sin(angle))^1.5
```

This creates a natural brightness curve with:
- 0% brightness at sunrise/sunset (angle = 0° or 180°)
- 100% brightness at zenith (angle = 90°)

#### Sky Color Interpolation (Day)
```
color_day = night_color + (day_color - night_color) × sin(sun_angle)
```

Color values smoothly transition from night to day colors based on sun height.

#### Ground Brightness (Day)
```
sun_height = sin(sun_angle)
color_ground = night_color + (day_color - night_color) × sun_height
```

### 3. Shadow Casting

#### Shadow Visibility Condition
```
IF sun_height < 0.05:
    NO shadow rendering
```

Shadows only render when sun is high enough to create visible shadows.

#### Shadow Direction Vector
```
dx = sun_x - object_center_x
dy = sun_y - object_center_y
distance = √(dx² + dy²) + 1

shadow_direction_x = -dx / distance
shadow_direction_y = -dy / distance
```

The negative sign ensures shadow extends away from the sun (opposite direction).

#### Shadow Extension
```
shadow_extension_x = shadow_direction_x × 300 × (1 - sun_height)
shadow_extension_y = shadow_direction_y × 300 × (1 - sun_height)

shadow_end_x = object_center_x + shadow_extension_x
shadow_end_y = object_ground_y + |shadow_extension_y| × 0.3
```

**Key properties:**
- Longer shadows when sun is lower (near horizon)
- Shorter shadows when sun is higher (near zenith)
- Shadows taper from object base to endpoint
- Shadow opacity: 40-50% alpha for realistic appearance

### 4. Seasonal Day/Night Schedule

#### Summer Configuration
```
DAY_START = 6 AM
DAY_END = 18 PM (6 PM)
DAY_DURATION = 12 hours
NIGHT_DURATION = 12 hours
```

#### Winter Configuration
```
DAY_START = 8 AM
DAY_END = 16 PM (4 PM)
DAY_DURATION = 8 hours
NIGHT_DURATION = 16 hours
```

### 5. Time Advancement

#### Simulated Time Update
```
frame_delta_time = frame_duration × TIME_SCALE
current_angle += (frame_delta_time / day_or_night_span) × π

// Map angle back to hours
current_hour = start_hour + (angle / π) × span_hours
```

Where `TIME_SCALE` = 0.2 (default, configurable in config.py)

### 6. Gradient Sky Rendering

#### Sky Color Interpolation Across Height
```
FOR i = 1 to GRADIENT_STEPS:
    strip_height = screen_height / GRADIENT_STEPS
    gradient_g = color.g - (i × color.g / GRADIENT_STEPS) × brightness
    gradient_b = color.b - (i × color.b / GRADIENT_STEPS) × brightness
    glColor3f(color.r, gradient_g, gradient_b)
    draw_horizontal_quad(y = i × strip_height)
```

This creates a natural gradient from bright sky at horizon to darker sky above.

## Project Structure

```
computer-graphics-mini-project/
├── main.py                      # Application entry point & event handling
├── requirements.txt             # Python dependencies
├── README.md                    # This documentation
├── about.txt                    # Project overview
└── src/
    ├── __init__.py              # Package initialization
    ├── config.py                # Global constants & configuration
    ├── scene.py                 # Scene manager & simulation loop
    └── entities/
        ├── __init__.py
        ├── background.py        # Sky gradient rendering
        ├── celestial.py         # Sun, Moon, Stars, Clouds
        ├── ground.py            # Ground plane & snow cover
        ├── house.py             # House with windows & shadows
        ├── tree.py              # Trees with foliage & shadows
        ├── nature.py            # Grass & Fireflies
        └── snow.py              # Snowfall effects (winter only)
```

## Configuration

Customize the simulation by editing [src/config.py](src/config.py):

### Window Settings
```python
WINDOW_SIZE = (1920, 1080)
WINDOW_POSITION = (0, 0)
```

### Seasonal Schedule
```python
SUMMER_DAY_START = 6      # 6 AM
SUMMER_DAY_END = 18       # 6 PM
WINTER_DAY_START = 8      # 8 AM
WINTER_DAY_END = 16       # 4 PM
```

### Colors
```python
SUMMER_DAY_SKY = (0.02, 0.46, 0.76)      # Bright blue
WINTER_DAY_SKY = (0.7, 0.8, 0.9)         # Pale blue-gray
NIGHT_SKY = (0, 0.005, 0.02)             # Dark blue-black
```

### Simulation Speed
```python
TIME_SCALE = 0.2    # 0.2 = 5x slower than real-time
```

## Core Features

### Day-Night Cycle
- Sunrise at 6 AM (summer) or 8 AM (winter)
- Sunset at 6 PM (summer) or 4 PM (winter)
- Smooth brightness transitions over 100-step gradient
- Realistic color interpolation from day to night

### Celestial Bodies
- **Sun**: Revolves along an arc from east to west, brightness follows sin curve
- **Moon**: Appears at night, follows similar arc mechanics
- **Stars**: Appear only at night, with twinkling animation
- **Glow Effect**: Both sun and moon have brightness halos

### Landscape Elements
- **Trees**: Layered foliage with dynamic day/night brightness and sun-driven shadows
- **House**: Day/night window colors with window glow and directional shadows
- **Ground**: Grass color interpolates between day/night states
- **Clouds**: Drift horizontally during day; hidden at night (summer only)
- **Snowfall**: Winter-exclusive particle effect with ground snow coverage

### Shadows
- Cast by sun position during daylight
- Length and direction based on sun angle
- Hidden during winter season
- Fade naturally as sun approaches horizon

### Interactive Features
- Jump to any hour instantly without animation
- Toggle between summer and winter seasons
- Pause/resume animation cycle
- Console-based help and time display
- Real-time hour/minute display in console

## Notes & Limitations

- **Platform Support**: Validated on Windows. Linux/macOS may require manual FreeGLUT installation.
- **Text Rendering**: On-screen text not rendered to avoid OpenGL font complexity; all info printed to console.
- **Performance**: Optimized for 1920×1080 resolution; adjust WINDOW_SIZE for other displays.
- **Shadows**: Disabled in winter season for visual clarity; can be re-enabled in config.

## Future Enhancement Ideas

- [ ] 3D perspective camera
- [ ] Procedural terrain generation
- [ ] Weather effects (rain, fog)
- [ ] More detailed architecture (windows, doors, roof texture)
- [ ] Animated birds and additional wildlife
- [ ] Realistic atmospheric scattering
- [ ] Audio (ambient sounds, music)
- [ ] Save/load scene state

## References

- OpenGL Mathematics: https://learnopengl.com/
- PyOpenGL Documentation: https://pyopengl.sourceforge.net/
- Celestial Mechanics: Sun and Moon altitude/azimuth calculations

---

**Version**: 1.0.0  
**Last Updated**: January 2026  
**License**: MIT

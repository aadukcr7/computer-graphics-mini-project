# Day-Night Transition Simulation

A realistic day-night cycle simulation built with PyOpenGL, featuring dynamic lighting, celestial mechanics, and atmospheric effects.

## Overview

This computer graphics project simulates a complete day-night cycle with accurate shadow casting, smooth color transitions, and multiple animated elements. The simulation starts at midday and progresses through sunset, night, sunrise, and back to day in a continuous loop.

## Features

### Celestial Mechanics
- **Sun**: Revolves across the sky in an arc from left to right during daytime
  - Dynamic brightness that peaks at zenith (highest point)
  - Realistic glow effect that scales with brightness
  - Smooth fade-in/fade-out during transitions

- **Moon**: Follows the same orbital path during nighttime
  - Independent brightness curve
  - Appears only during night hours
  - Smooth transitions between day and night

### Environmental Elements
- **Background Sky**: 
  - Smooth gradient rendering with 100 layers
  - Dynamic color interpolation between day (`0.02, 0.46, 0.76`) and night (`0.0, 0.005, 0.02`)
  - Gradual transitions based on sun position

- **Ground**:
  - Solid green ground layer at the bottom
  - Color transitions from bright green during day to very dark green at night
  - 300-pixel height from bottom of screen

- **Clouds**: 
  - Procedurally generated with varying sizes (0.8x to 1.5x)
  - Horizontal drift at different speeds
  - Visible only during daytime
  - Semi-transparent rendering with opacity variation

- **Stars**: 
  - 100 randomly positioned stars
  - Twinkling animation with size variation (1-3 pixels)
  - Visible only at night
  - Located above ground level (y: 0-650)

- **Fireflies**:
  - 25 animated particles
  - Random movement within defined range
  - Golden glow effect
  - Active only during nighttime

### Landscape Objects
- **House**:
  - Multi-part structure with walls, roof, and garden
  - Dynamic window lighting (warm yellow at night, cool blue during day)
  - Brightness adjustment (30% at night, 100% during day)
  - Casts dynamic shadow based on sun position
  - Positioned at center of scene (650, 530)

- **Trees** (2x Pine/Conifer):
  - Layered triangular foliage
  - Tapered trunk design
  - Dynamic brightness (30% at night, 100% during day)
  - Accurate shadow projection based on sun angle
  - Positioned at left (200, 750) and right (1350, 750)

### Shadow System
- Physically-based shadow projection
- Length inversely proportional to sun height
- Direction calculated from sun-to-object angle
- Semi-transparent rendering (50% opacity)
- Shadows only visible during daytime when sun is above horizon

### Transition System
- Gradual color interpolation over 200 frames
- Smooth entity visibility changes
- Progressive brightness adjustments
- No abrupt state changes

## Technical Specifications

### Window Configuration
- **Resolution**: 1600 x 1000 pixels
- **Position**: (100, 100) from top-left corner
- **Coordinate System**: Origin at top-left (0,0), bottom-right (1600, 1000)

### Animation Parameters
- **Sun Movement**: 0.0008 radians per frame
- **Moon Movement**: 0.0005 radians per frame  
- **Transition Speed**: 0.005 per frame
- **Orbit Center**: (800, 333) - top third of screen
- **Orbit Radius**: 500px horizontal, 300px vertical

### Performance
- Continuous rendering using GLUT idle callback
- Double buffering for smooth animation
- Efficient polygon rendering
- No frame rate cap (runs at monitor refresh rate)

## Installation

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

## Project Structure

```
computer-graphics-mini-project/
│
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # Project documentation
├── LICENSE                # License information
│
└── src/                   # Source code directory
    ├── __init__.py
    ├── config.py          # Configuration constants
    ├── scene.py           # Scene manager and orchestration
    │
    └── entities/          # Visual element classes
        ├── __init__.py
        ├── background.py  # Sky gradient rendering
        ├── celestial.py   # Sun, Moon, Star, Cloud classes
        ├── ground.py      # Ground layer
        ├── house.py       # House structure with shadows
        ├── tree.py        # Tree with shadow casting
        └── nature.py      # Grass and Firefly classes
```

## Configuration

All visual parameters can be adjusted in `src/config.py`:

### Customizable Parameters
- Window size and position
- Sky colors (day and night)
- Celestial body sizes, positions, and colors
- Star and firefly counts
- Ground colors
- Tree and house positions
- Animation speed multiplier

### Example Customization
```python
# In src/config.py

# Change window size
WINDOW_SIZE = (1920, 1080)

# Adjust day/night colors
NIGHT_SKY = (0.0, 0.01, 0.05)  # Darker night
DAY_SKY = (0.1, 0.6, 0.9)      # Brighter blue sky

# More stars
STAR_COUNT = 200

# Faster animation
ANIMATION_SPEED = 2.0
```

## How It Works

### Day-Night Cycle
1. **Initialization**: Scene starts at midday with sun at zenith
2. **Day Phase**: Sun travels from zenith to horizon, brightness decreases
3. **Sunset Transition**: 200-frame smooth transition from day to night colors
4. **Night Phase**: Moon rises and travels across sky, stars twinkle
5. **Sunrise Transition**: 200-frame smooth transition from night to day colors
6. **Repeat**: Cycle continues indefinitely

### Rendering Order
Entities are rendered in layers (back to front):
1. Background gradient
2. Ground
3. Clouds
4. Tree shadows
5. Trees
6. House shadow
7. House
8. Moon
9. Sun
10. Stars (overlay)
11. Fireflies (overlay)

### Shadow Calculation
Shadows use physics-based projection:
```python
shadow_length = base_length * (1 - sun_height)
shadow_offset_x = -dx * shadow_length / (dy + constant)
```
Where:
- `sun_height` = sin(sun_angle)^1.5
- `dx` = horizontal distance from object to sun
- `dy` = vertical distance from object to sun

## Dependencies

- **PyOpenGL** (3.1.5+): OpenGL bindings for Python
- **PyOpenGL-accelerate** (3.1.5+): Acceleration for PyOpenGL
- **numpy** (1.21.0+): Numerical computing (used by PyOpenGL)

## Troubleshooting

### Common Issues

**"ImportError: No module named OpenGL"**
```bash
pip install PyOpenGL PyOpenGL-accelerate
```

**Window doesn't appear**
- Ensure graphics drivers are up to date
- Try running with administrator privileges
- Check if OpenGL is supported on your system

**Slow performance**
- Reduce STAR_COUNT and FIREFLY_COUNT in config.py
- Decrease GRADIENT_STEPS for faster sky rendering
- Lower WINDOW_SIZE resolution

**Colors appear wrong**
- Verify color values are in range 0.0 to 1.0
- Check monitor color calibration
- Ensure graphics drivers support proper color depth

## Credits

Developed as a Computer Graphics Mini Project using PyOpenGL.

## License

See LICENSE file for details.
python main.py
```

The window will display the animated day-night transition simulation.

## Configuration

Edit `src/config.py` to customize:
- Window size and position
- Object colors (sky, sun, moon, etc.)
- Element counts (stars, fireflies)
- Animation timings and speeds

Example:
```python
WINDOW_SIZE = (1200, 800)
DAY_SKY = (0.02, 0.46, 0.76)
NIGHT_SKY = (0.01, 0.1, 0.35)
```

## Project Structure

```
computer-graphics-mini-project/
├── main.py                 # Application entry point
├── requirements.txt        # Python dependencies
├── README.md              # This file
├── LICENSE                # MIT License
├── .gitignore            # Git ignore rules
├── CONTRIBUTING.md       # Contribution guidelines
└── src/
    ├── config.py         # Configuration settings
    ├── scene.py          # Main scene manager
    ├── __init__.py
    └── entities/
        ├── background.py # Sky gradient implementation
        ├── celestial.py  # Sun, moon, and stars
        ├── nature.py     # Clouds, grass, and fireflies
        ├── house.py      # House with lighting
        └── __init__.py
```

## Technologies Used

- **PyOpenGL**: OpenGL bindings for Python
- **PyOpenGL-accelerate**: Performance optimization
- **Pillow**: Image processing
- **NumPy**: Numerical computations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines.

## Author

Computer Graphics Mini Project - 2025

---

**Note**: This is an educational project demonstrating computer graphics concepts using OpenGL.

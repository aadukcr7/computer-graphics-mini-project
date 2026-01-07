# Day-Night Transition Simulation

PyOpenGL mini-project that renders a full day-night cycle with dynamic lighting, shadows, animated clouds, stars, fireflies, and interactive time jumps.

## Requirements
- Python 3.8+
- OpenGL-capable GPU/driver
- FreeGLUT/GLUT available on your platform (often included with PyOpenGL on Windows)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run

```bash
python main.py
```

You will be prompted for a starting hour (00-23). The window opens after input.

## Controls (window focused)
- H: help menu (printed to console)
- 00-23: type two digits to jump to that hour (auto-processes after 2 digits)
- Q: quit

## Core Features
- Day/night schedule: sunrise 06:00, sunset 18:00 with smooth brightness and color transitions
- Celestial bodies: sun and moon share an arc with glow and per-angle brightness
- Atmosphere: 100-step sky gradient, drifting daytime clouds
- Ground and landscape: trees and house with daytime shadows; all dim at night; shadows hidden at night
- Night life: stars twinkle and fireflies appear only at night
- Time control: jump to any hour instantly; configurable simulation speed

## Configuration
Tune visuals and timing in [src/config.py](src/config.py):
- Window: `WINDOW_SIZE`, `WINDOW_POSITION`, `WINDOW_TITLE`
- Colors: sky, grass, foliage, house day/night tones
- Counts: `STAR_COUNT`, `FIREFLY_COUNT`, `CLOUD_COUNT`
- Timing: `TIME_SCALE` (overall cycle speed)

Additional timing knob `TRANSITION_SPEED` lives in [src/scene.py](src/scene.py).

## Project Structure

```
computer-graphics-mini-project/
├── main.py              # Application entry and input handling
├── requirements.txt     # Python dependencies
├── README.md            # Documentation
└── src/
    ├── config.py        # Global settings
    ├── scene.py         # Scene orchestration and timekeeping
    └── entities/        # Rendered objects
        ├── background.py
        ├── celestial.py
        ├── ground.py
        ├── house.py
        ├── nature.py
        └── tree.py
```

## Notes
- Tested with PyOpenGL on Windows; other platforms may require installing freeglut separately.
- If on-screen text fails to render, console output still shows controls and time jumps.

addd the concept of the seasons
days are shorter in winter and night are longer where as days are longer in summer and nights become comparatively shorter. 

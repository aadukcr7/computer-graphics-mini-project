the sun. In addition to the daily cycle, the system supports seasonal changes, allowing the
timings, daylight duration, sky color tones, and environmental elements such as snow. By
environmental appearance.
day is mapped to a 24-hour cycle, which is further divided into day and night periods. Instead
# Day-Night Transition Simulation

## Overview
This project is a 2D computer graphics simulation built with Python and PyOpenGL. It models a
continuous 24-hour day-night cycle using mathematical motion for the sun and moon, and it
supports seasonal variation (summer and winter). The simulation dynamically updates sky and
ground colors, shadows, and environmental elements to create a realistic, time-driven scene.

The system is organized into modular entities (background, celestial bodies, ground, house,
trees, clouds, stars, fireflies, snow) that are coordinated by a central scene manager. Each
entity is responsible for its own drawing logic, while time progression and interactions are
handled by the scene.

## Project Architecture

- main.py initializes the OpenGL window, registers callbacks, and manages keyboard input.
- src/scene.py is the core controller. It creates all entities, manages time progression,
	toggles seasons, and renders the scene in the correct order each frame.
- src/config.py contains all tunable parameters such as colors, sizes, positions, and time
	schedule settings.
- src/entities/ contains the individual visual components (background, sun, moon, stars,
	clouds, ground, house, trees, grass, fireflies, snow).

## Time Modeling and Motion

- The sun and moon move along a semi-circular arc defined by cosine and sine functions.
- The angle of motion is mapped to simulated time (hours). This enables smooth transitions
	between morning, noon, evening, and night.
- The brightness factor is derived from sin(angle), which ensures gradual lighting changes
	around sunrise and sunset.

## Core Features and How They Work

### 1. Day-Night Cycle
- The scene switches between day and night based on the sun or moon arc completion.
- Sky and ground colors interpolate based on brightness derived from the sun angle.
- The sun appears during the day and the moon appears at night with a fading glow effect.

### 2. Seasonal Variation (Summer/Winter)
- Summer and winter use different day schedules, which changes sunrise and sunset times.
- Winter enables snowfall and a snow cover overlay on the ground.
- Shadows are disabled in winter for clarity and visibility.

### 3. Dynamic Shadows
- Shadows are drawn for trees and the house based on sun position.
- Shadow length increases when the sun is near the horizon and decreases near noon.
- Shadows are skipped if the sun is too low or if the season is winter.

### 4. Sky Gradient and Lighting
- The sky is rendered as a vertical gradient with multiple strips.
- The gradient colors shift continuously based on brightness.
- Ground color also transitions smoothly between day and night shades.

### 5. Environmental Elements
- Clouds drift horizontally during daytime only.
- Stars appear and twinkle during nighttime.
- Fireflies appear near ground level at night.
- Snowfall is enabled only in winter and uses multiple animated particles.

### 6. On-Screen Time HUD
- The simulation displays the current simulated hour on the screen.
- The time value updates automatically as the sun or moon moves.

## Rendering Flow (Per Frame)

1. Background gradient is drawn.
2. Ground (and snow cover if winter) is drawn.
3. Stars and clouds are drawn based on time of day.
4. Snowfall is drawn and updated in winter.
5. Trees and house are drawn with shadows when enabled.
6. Fireflies are drawn at night.
7. Sun or moon is drawn last to appear on top.
8. The time HUD is rendered in screen space.

## User Interaction

- H: Show help in the console
- S: Toggle season (summer or winter)
- 00-23: Jump to a specific hour
- Q: Quit

## Screenshots

![Summer Day](images/summer_day.png)
![Summer Night](images/summer_night.png)
![Winter Day](images/winter_day.png)
![Winter Night](images/winter_night.png)

## Tools and Libraries

- Python 3.8+
- PyOpenGL and PyOpenGL-accelerate
- GLUT (windowing and input)

## Summary
This project demonstrates a complete time-driven scene with real-time transitions, seasonal
variation, and interactive controls. It combines mathematical modeling, animation, and
OpenGL rendering to simulate natural day and night behavior with multiple environmental
effects.

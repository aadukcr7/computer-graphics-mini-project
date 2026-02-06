Kathmandu University  
Department of Computer Science and Engineering  
Dhulikhel, Kavrepalanchowk

**Project Report**  
On  
"COMP 342"

Submitted by:  
Aaditya K.C (05)  
Jagat K.C (07)  
Saurav Bhujel (23)

Level: UNG CS (III/I)

Submitted to:  
Dhiraj Shrestha  
Department of Computer Science and Engineering

Submission Date: 1/16/2026

# Day-Night Transition Simulation Using PyOpenGL

## Abstract
The Day-Night Transition Simulation is a computer graphics project that models the natural
cycle of day and night using mathematical and rendering techniques. The simulation represents
the apparent motion of the sun and moon through rotational movement along semi-circular
paths, where time is mapped to angular displacement to ensure smooth transitions. Variations
in lighting, sky color, and shadow behavior are dynamically calculated based on the height of
the sun. In addition to the daily cycle, the system supports seasonal changes, allowing the
user to switch between summer and winter. Seasonal variation affects sunrise and sunset
timings, daylight duration, sky color tones, and environmental elements such as snow. By
integrating trigonometric formulas, interpolation methods, and time-based animation, the
project demonstrates how real-world astronomical and environmental changes can be
visualized using 2D computer graphics and OpenGL.

## 1. Introduction
Natural phenomena such as the day-night cycle and seasonal variation are governed by
predictable physical and astronomical principles. In computer graphics, these phenomena can
be recreated using mathematical models that control motion, lighting, and color transitions.
Simulating such behavior helps in understanding core graphics concepts including animation,
transformations, interpolation, and lighting models.

This project presents a Day-Night Transition Simulation developed using Python and PyOpenGL,
which visually demonstrates a complete 24-hour cycle along with seasonal changes. The sun
and moon are rotated along orbital paths using trigonometric functions, while time is
continuously updated to produce smooth visual transitions. Lighting intensity, sky color, and
shadows dynamically change based on the simulated time and sun position. The simulation also
incorporates seasonal variation, enabling the user to switch between summer and winter modes.
This affects the length of daytime and nighttime, sunrise and sunset timings, and
environmental appearance.

## 2. Objective of the Project
The main objectives of this project are:
- To simulate a complete 24-hour day-night cycle
- To model sun and moon rotation using trigonometry
- To calculate dynamic lighting and brightness
- To generate realistic shadows based on sun position
- To visualize seasonal changes in daylight duration
- To demonstrate mathematical modeling in computer graphics

## 3. Technologies Used
- Programming Language: Python
- Graphics Library: PyOpenGL (OpenGL + GLUT)
- Mathematical Tools: Trigonometric functions (sin, cos), interpolation

## 4. Time Modeling and Progression
### 4.1 Representation of Time
Time in the simulation is represented as a continuous variable, not as discrete hours. A full
day is mapped to a 24-hour cycle, which is further divided into day and night periods. Instead
of rotating the Earth, the simulation rotates the sun and moon along a semi-circular path
using angles.

### 4.2 Time to Angle Conversion
For smooth animation, time is converted into an angular value.  
Day progress is calculated as:  
DAY_PROGRESS = (current_hour - DAY_START) / DAY_DURATION  
Sun angle:  
sun_angle = DAY_PROGRESS * pi

Night progress is calculated as:  
NIGHT_PROGRESS = (current_hour - NIGHT_START) / NIGHT_DURATION  
Moon angle:  
moon_angle = NIGHT_PROGRESS * pi

### 4.3 Orbital Arc Position
x = center_x + radius * cos(angle)  
y = center_y + radius * sin(angle)

## 5. Lighting and Color Model
### 5.1 Brightness
Brightness is derived from the vertical height of the sun or moon:  
brightness = max(0, sin(angle))^1.5

### 5.2 Sky and Ground Interpolation
Sky and ground colors are interpolated using the current brightness to create smooth
transitions between day and night.

## 6. Shadow Computation
Shadows are projected opposite the sun direction. Shadow length scales with the sun height
so that shadows are longer near the horizon and shorter at noon. Shadows are disabled in
winter for clarity.

## 7. Features Implemented
- Day-night cycle with smooth sky and ground color interpolation
- Sun and moon orbital motion with brightness curves
- Dynamic shadows based on sun position
- Seasonal schedule (summer: 12h day, winter: 8h day)
- Winter effects: snowfall and ground snow
- Interactive controls for time and season

## 8. User Interaction
- H: Show help
- S: Toggle season (summer/winter)
- 00-23: Jump to specific hour
- Q: Quit

## 9. System Requirements
- Python 3.8 or later
- OpenGL-capable GPU and drivers
- Libraries: PyOpenGL, PyOpenGL-accelerate, Pillow, numpy

## 10. Installation and Execution
- Install dependencies: pip install -r requirements.txt
- Run: python main.py
- Enter a starting hour when prompted

## 11. Expected Results
- Real-time rendering of a landscape that transitions between day and night
- Smooth sky gradients and ambient lighting changes
- Visible shift in day length when switching seasons
- Snowfall and snow cover in winter mode

## Screenshots
![Summer Day](images/summer_day.png)
![Summer Night](images/summer_night.png)
![Winter Day](images/winter_day.png)
![Winter Night](images/winter_night.png)

## 12. Limitations
- 2D rendering only (no perspective camera)
- No on-screen text (time shown via console)
- Shadows simplified and disabled in winter
- No weather beyond snow

## 13. Future Enhancements
- 3D camera and terrain
- Weather effects (rain, fog)
- More detailed architecture and textures
- Atmospheric scattering for realistic sky
- Ambient audio

## 14. References
- https://learnopengl.com/
- https://pyopengl.sourceforge.net/

End of report.

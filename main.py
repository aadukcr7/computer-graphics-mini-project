"""
Day-Night Transition Simulation
Main entry point for the OpenGL application
"""
from OpenGL.GL import *
from OpenGL.GLUT import *

from src.scene import Scene
from src.config import WINDOW_SIZE, WINDOW_POSITION, WINDOW_TITLE


class Application:
    """OpenGL Application for Day-Night Simulation"""
    
    def __init__(self, window_size=WINDOW_SIZE, window_position=WINDOW_POSITION):
        """Initialize application with window settings"""
        self.window_size = window_size
        self.window_position = window_position
        self.scene = None
    
    def refresh_2d(self, width, height):
        """Set up 2D orthographic projection"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, height, 0, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def draw(self):
        """Main drawing callback"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.refresh_2d(*self.window_size)
        self.scene.draw()
        glutSwapBuffers()
    
    def run(self):
        """Initialize GLUT and start main loop"""
        # Create scene
        self.scene = Scene()
        
        # Initialize GLUT
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(*self.window_size)
        glutInitWindowPosition(*self.window_position)
        glutCreateWindow(WINDOW_TITLE)
        
        # Register callbacks
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        
        # Start main loop
        glutMainLoop()


def main():
    """Entry point for the application"""
    app = Application()
    app.run()


if __name__ == "__main__":
    main()
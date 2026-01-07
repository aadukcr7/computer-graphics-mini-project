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
    
    def __init__(self, window_size=WINDOW_SIZE, window_position=WINDOW_POSITION, hour=12):
        """Initialize application with window settings
        
        Args:
            window_size: Window dimensions (width, height)
            window_position: Window position (x, y)
            hour: Initial hour to display (0-23)
        """
        self.window_size = window_size
        self.window_position = window_position
        self.scene = None
        self.initial_hour = hour
        self.time_input_buffer = ""  # Buffer for two-digit time input

    
    def refresh_2d(self, width, height):
        """Set up 2D orthographic projection"""
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0.0, width, height, 0, 0.0, 1.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
    
    def keyboard(self, key, x, y):
        """Handle keyboard input"""
        if key == b'q' or key == b'Q':
            exit()
        elif key == b'h' or key == b'H':
            print("\n" + "="*50)
            print("KEYBOARD CONTROLS")
            print("="*50)
            print("Q - Quit simulation")
            print("H - Show this help")
            print("S - Toggle season (summer/winter)")
            print("00-23 - Jump to hour (type 2 digits: 00=midnight, 06=sunrise, 12=noon, 18=sunset, 23=late night)")
            print("="*50 + "\n")
        elif key == b's' or key == b'S':
            # Toggle season in the scene
            self.scene.toggle_season()
            print(f"\r✓ Season toggled. Now: {self.scene.season.capitalize()}")
        elif key == b'\r' or key == b'\n':  # Enter key - process buffer
            if self.time_input_buffer:
                self._process_time_input()
        elif key == b'\x08':  # Backspace - clear buffer
            self.time_input_buffer = ""
            print("Input cleared")
        elif b'0' <= key <= b'9':
            # Add digit to buffer
            self.time_input_buffer += key.decode()
            print(f"Input: {self.time_input_buffer}", end="", flush=True)
            
            # Auto-process when we have 2 digits
            if len(self.time_input_buffer) == 2:
                self._process_time_input()
    
    def _process_time_input(self):
        """Process the buffered time input"""
        try:
            hour = int(self.time_input_buffer)
            if 0 <= hour <= 23:
                if self.scene.set_hour(hour):
                    hour_12 = hour % 12 or 12
                    am_pm = "AM" if hour < 12 else "PM"
                    print(f"\r✓ Jumped to {hour_12:02d}:00 {am_pm} (24h: {hour:02d}:00)")
            else:
                print(f"\r✗ Invalid: {self.time_input_buffer} is not 0-23")
        except ValueError:
            print(f"\r✗ Invalid input: {self.time_input_buffer}")
        finally:
            self.time_input_buffer = ""

    
    def _prompt_for_time(self):
        """Prompt user for time input - NOT used during simulation"""
        # input() would block the GLUT event loop, so this is kept for reference only
        pass

    
    def draw(self):
        """Main drawing callback"""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        self.refresh_2d(*self.window_size)
        self.scene.draw()
        glutSwapBuffers()
    
    def run(self):
        """Initialize GLUT and start main loop"""
        # Create scene with initial hour
        self.scene = Scene(hour=self.initial_hour)
        
        # Initialize GLUT
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DEPTH)
        glutInitWindowSize(*self.window_size)
        glutInitWindowPosition(*self.window_position)
        glutCreateWindow(WINDOW_TITLE)
        
        # Register callbacks
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        glutKeyboardFunc(self.keyboard)
        
        # Convert to 12-hour format for display
        hour_12 = self.initial_hour % 12 or 12
        am_pm = "AM" if self.initial_hour < 12 else "PM"
        
        print("\n" + "="*50)
        print("DAY-NIGHT SIMULATION WITH TIME CONTROL")
        print("="*50)
        print(f"Starting at: {hour_12:02d}:00 {am_pm} (24h: {self.initial_hour:02d}:00)")
        print("\nThe simulation is RUNNING - watch the day-night cycle!")
        print("\nPress a key while the window is active:")
        print("  H - Help menu")
        print("  S - Toggle season (summer/winter)")
        print("  00-23 - Type 2 digits to jump to hour")
        print("  Q - Quit")
        print("="*50 + "\n")
        
        # Start main loop
        glutMainLoop()


def get_user_time():
    """Get initial time from user input"""
    while True:
        try:
            user_input = input("Enter starting hour (00-23) [default 12]: ").strip()
            
            if not user_input:
                return 12
            
            hour = int(user_input)
            if 0 <= hour <= 23:
                return hour
            else:
                print("Please enter a number between 0 and 23.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def main():
    """Entry point for the application"""
    print("\n" + "="*50)
    print("DAY-NIGHT TRANSITION SIMULATION")
    print("="*50)
    
    # Get time input from user
    hour = get_user_time()
    
    app = Application(hour=hour)
    app.run()


if __name__ == "__main__":
    main()

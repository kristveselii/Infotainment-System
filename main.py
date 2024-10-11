# Importing necessary PyQt5 classes and modules
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel
from PyQt5.QtWebEngineWidgets import QWebEngineView  # For displaying YouTube videos using a web browser
from PyQt5.QtCore import QUrl, QTimer, QRectF, QPointF, Qt  # For URLs, timers, and basic geometric types (QRectF, QPointF)
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont  # For custom drawing (speedometer, fuel gauge)
import math  # To calculate angles and trigonometry for the dials

class InfotainmentSystem(QWidget):
    """
    This class represents the main infotainment system, which includes:
    - A speedometer (displays current speed).
    - A fuel gauge (displays fuel level).
    - A YouTube media player (plays a video from a provided URL).
    - Gas and brake buttons to control speed.
    - A text input field to play a YouTube video.
    """
    def __init__(self):
        super().__init__()
        self.speed = 0  # Initial speed of the car (0 km/h)
        self.fuel = 100  # Initial fuel level (100% full)
        self.initUI()  # Set up the user interface
        self.initTimer()  # Set up the timer for fuel consumption updates

    def initUI(self):
        """
        Initializes the UI layout with the speedometer, fuel gauge, YouTube player, 
        buttons for gas and brake, and an input field for the YouTube URL.
        """
        layout = QVBoxLayout()  # Vertical layout to hold all elements (main layout)

        # Create a horizontal layout for the speedometer, fuel gauge, and media player
        dashboard_layout = QHBoxLayout()

        # Add the speedometer widget to the dashboard layout
        self.speedometer = Speedometer()  # Create the speedometer instance
        dashboard_layout.addWidget(self.speedometer)  # Add the speedometer to the layout

        # Add the fuel gauge widget to the dashboard layout (next to speedometer)
        self.fuel_gauge = FuelGauge()  # Create the fuel gauge instance
        dashboard_layout.addWidget(self.fuel_gauge)  # Add the fuel gauge to the layout

        # Add the media player (YouTube video player) to the dashboard layout (right side)
        self.browser = QWebEngineView()  # Create a web browser instance for playing YouTube videos
        dashboard_layout.addWidget(self.browser)  # Add the web browser to the layout

        # Add the dashboard layout (speedometer, fuel gauge, media player) to the main layout
        layout.addLayout(dashboard_layout)

        # Add buttons for gas and brake (for speed control)
        gas_button = QPushButton('Gas', self)  # Gas button to increase speed
        layout.addWidget(gas_button)  # Add the gas button to the main layout
        gas_button.clicked.connect(self.accelerate)  # Connect button to accelerate function

        brake_button = QPushButton('Brake', self)  # Brake button to decrease speed
        layout.addWidget(brake_button)  # Add the brake button to the main layout
        brake_button.clicked.connect(self.decelerate)  # Connect button to decelerate function

        # Add label and input field for YouTube URL
        self.url_label = QLabel('Enter YouTube URL:', self)  # Label for YouTube URL input
        layout.addWidget(self.url_label)  # Add the label to the main layout

        self.url_input = QLineEdit(self)  # Input field where the user can type the YouTube URL
        layout.addWidget(self.url_input)  # Add the input field to the main layout

        # Add play button for the YouTube media player
        play_button = QPushButton('Play Video', self)  # Button to play the video from the entered URL
        layout.addWidget(play_button)  # Add the play button to the main layout
        play_button.clicked.connect(self.play_video)  # Connect button to play_video function

        # Set the main layout to the widget (Infotainment System UI)
        self.setLayout(layout)
        self.setWindowTitle('Car Infotainment System')  # Set the window title

    def initTimer(self):
        """
        Initializes a timer to update the fuel level based on the car's speed every second.
        """
        self.timer = QTimer(self)  # Create a timer
        self.timer.timeout.connect(self.updateFuel)  # Call updateFuel every time the timer times out (every 1 second)
        self.timer.start(1000)  # Start the timer to run every 1000 milliseconds (1 second)

    def accelerate(self):
        """
        Increases the car's speed by 10 km/h, with a maximum speed of 180 km/h.
        Also updates the speedometer.
        """
        if self.speed < 180:  # Max speed is 180 km/h
            self.speed += 10  # Increase speed by 10 km/h
            self.speedometer.set_speed(self.speed)  # Update the speedometer display

    def decelerate(self):
        """
        Decreases the car's speed by 10 km/h, with a minimum speed of 0 km/h.
        Also updates the speedometer.
        """
        if self.speed > 0:  # Minimum speed is 0 km/h (can't go negative)
            self.speed -= 10  # Decrease speed by 10 km/h
            self.speedometer.set_speed(self.speed)  # Update the speedometer display

    def updateFuel(self):
        """
        Reduces the fuel level based on the car's speed. The faster the speed, the more fuel is consumed.
        If the car is not moving (speed = 0), no fuel is consumed.
        """
        if self.speed > 0 and self.fuel > 0:  # Only consume fuel if the car is moving and there's fuel left
            # Simulate fuel consumption: faster speed consumes more fuel
            fuel_consumed = self.speed * 0.05  # Example: 0.05% fuel consumed per km/h per second
            self.fuel = max(0, self.fuel - fuel_consumed)  # Ensure fuel doesn't go below 0
            self.fuel_gauge.set_fuel(self.fuel)  # Update the fuel gauge

    def play_video(self):
        """
        Plays a YouTube video from the URL entered by the user.
        The video is loaded in the QWebEngineView browser widget.
        """
        url = self.url_input.text()  # Get the URL from the input field

        if not url:  # If the URL is empty, show a message in the label
            self.url_label.setText("Enter a valid YouTube URL!")
            return

        # Check if the URL contains "youtube" or "youtu.be"
        if "youtube" not in url and "youtu.be" not in url:
            self.url_label.setText("Not a valid YouTube URL!")
            return

        self.browser.setUrl(QUrl(url))  # Load the video URL in the web browser


class Speedometer(QWidget):
    """
    This class represents the speedometer, which displays the current speed of the car.
    The speed is displayed as a dial with a needle.
    """
    def __init__(self):
        super().__init__()
        self.speed = 0  # Initial speed

    def set_speed(self, speed):
        """
        Sets the current speed and triggers a redraw of the speedometer.
        """
        self.speed = speed
        self.update()  # Redraw the dial when the speed changes

    def paintEvent(self, event):
        """
        Custom painting function to draw the speedometer dial and needle.
        This function is automatically called by Qt whenever the widget needs to be updated.
        """
        painter = QPainter(self)  # Create a QPainter to draw on the widget
        rect = self.rect()  # Get the current size of the widget (for drawing)

        # Draw dial (speedometer circle)
        painter.setRenderHint(QPainter.Antialiasing)  # Enable anti-aliasing for smoother edges
        painter.setPen(QPen(Qt.black, 5))  # Set the pen to draw the dial's outline (black, width 5)
        painter.setBrush(QBrush(Qt.white))  # Set the brush to fill the dial with white
        painter.drawEllipse(rect)  # Draw the speedometer circle (ellipse)

        # Draw ticks and speed numbers (increments of 20 km/h)
        painter.setPen(QPen(Qt.black, 2))  # Set the pen for ticks and speed numbers
        painter.setFont(QFont('Arial', 10))  # Set font for speed numbers

        # Loop to draw tick marks and speed labels around the dial
        for angle, speed_value in zip(range(-120, 121, 30), range(0, 181, 20)):  # -120 to 120 degrees, 0 to 180 km/h
            x1 = rect.center().x() + math.cos(math.radians(angle)) * rect.width() * 0.4
            y1 = rect.center().y() - math.sin(math.radians(angle)) * rect.height() * 0.4
            x2 = rect.center().x() + math.cos(math.radians(angle)) * rect.width() * 0.45
            y2 = rect.center().y() - math.sin(math.radians(angle)) * rect.height() * 0.45
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))  # Draw tick marks

            # Draw speed numbers with "km/h" next to the tick marks
            x_text = rect.center().x() + math.cos(math.radians(angle)) * rect.width() * 0.55
            y_text = rect.center().y() - math.sin(math.radians(angle)) * rect.height() * 0.55
            painter.drawText(int(x_text) - 15, int(y_text) + 5, f'{speed_value} km/h')  # Draw speed labels

        # Draw the needle
        painter.setPen(QPen(QColor(255, 0, 0), 5))  # Red needle (thickness 5)
        painter.setBrush(QBrush(QColor(255, 0, 0)))  # Red color for the needle

        # Calculate the angle based on speed (0 km/h = -120 degrees, 180 km/h = 120 degrees)
        angle = -120 + (240 * self.speed / 180)  # Scale speed to angle (-120 to 120 degrees)

        # Calculate the needle's end point (x, y)
        x = rect.center().x() + math.cos(math.radians(angle)) * rect.width() * 0.4
        y = rect.center().y() - math.sin(math.radians(angle)) * rect.height() * 0.4
        painter.drawLine(rect.center(), QPointF(int(x), int(y)))  # Draw the needle


class FuelGauge(QWidget):
    """
    This class represents the fuel gauge, which displays the current fuel level.
    The fuel level is shown as a vertical bar, with labels "F" (Full) and "E" (Empty).
    """
    def __init__(self):
        super().__init__()
        self.fuel = 100  # Initial fuel level (100% full)

    def set_fuel(self, fuel):
        """
        Sets the current fuel level and triggers a redraw of the fuel gauge.
        """
        self.fuel = fuel
        self.update()  # Redraw the gauge when the fuel level changes

    def paintEvent(self, event):
        """
        Custom painting function to draw the fuel gauge (a vertical bar) with the fuel level.
        This function is automatically called by Qt whenever the widget needs to be updated.
        """
        painter = QPainter(self)  # Create a QPainter to draw on the widget
        rect = self.rect()  # Get the current size of the widget (for drawing)

        # Draw the gauge background (a vertical rectangle)
        painter.setPen(QPen(Qt.black, 3))  # Black outline for the fuel gauge (width 3)
        painter.setBrush(QBrush(Qt.lightGray))  # Light gray background for the fuel gauge
        gauge_rect = QRectF(rect.width() * 0.3, rect.height() * 0.1, rect.width() * 0.4, rect.height() * 0.8)
        painter.drawRect(gauge_rect)  # Draw the vertical fuel gauge rectangle

        # Draw the fuel level as a blue-filled rectangle
        fuel_height = gauge_rect.height() * (self.fuel / 100)  # Calculate fuel level height based on percentage
        fuel_rect = QRectF(gauge_rect.left(), gauge_rect.bottom() - fuel_height, gauge_rect.width(), fuel_height)
        painter.setBrush(QBrush(QColor(0, 0, 255)))  # Blue color for the fuel level
        painter.drawRect(fuel_rect)  # Draw the filled fuel level rectangle

        # Draw the "F" (Full) and "E" (Empty) labels for the fuel gauge
        painter.setPen(QPen(Qt.black, 2))  # Set the pen for drawing labels
        painter.setFont(QFont('Arial', 12))  # Set the font for the labels
        painter.drawText(int(rect.width() * 0.15), int(rect.height() * 0.15), "F")  # Draw "F" for Full at the top
        painter.drawText(int(rect.width() * 0.15), int(rect.height() * 0.85), "E")  # Draw "E" for Empty at the bottom


# Main function to run the PyQt5 application
if __name__ == '__main__':
    app = QApplication([])  # Create a PyQt5 application
    infotainment = InfotainmentSystem()  # Create an instance of the infotainment system
    infotainment.show()  # Show the main window
    app.exec_()  # Start the application event loop

Car Infotainment System
This project is a Python-based car infotainment system built using PyQt5. It simulates an in-car dashboard with real-time displays for:

Speedometer: Shows the current speed of the car.
Fuel Gauge: Displays the car's fuel level, which depletes over time based on the car's speed.
YouTube Media Player: Allows users to input a YouTube URL and play the audio/video directly in the infotainment system via an embedded web browser.
Features:
Speedometer Dial: The speedometer displays the car's current speed, updated in real-time when the user accelerates or decelerates using the Gas and Brake buttons.
Fuel Gauge: The fuel gauge shows the current fuel level as a vertical bar, with fuel consumption tied to the speed of the car. The faster the speed, the quicker the fuel depletes.
YouTube Video Player: Users can input a valid YouTube URL, and the system will load and play the video using an embedded browser. This simulates a modern car infotainment system's multimedia capabilities.
Gas & Brake Buttons: Control the car's speed by increasing or decreasing it with the Gas and Brake buttons, affecting both the speedometer and the fuel consumption.
Technologies Used:
PyQt5: For creating the graphical user interface, including the speedometer, fuel gauge, and control buttons.
PyQtWebEngine: Used to embed a web browser for playing YouTube videos within the infotainment system.
QPainter: For custom drawing of the speedometer dial, needle, and fuel gauge.
How It Works:
The speedometer is dynamically updated based on the user's input from the Gas and Brake buttons.
The fuel gauge decreases based on the car's speed; if the car is stationary, no fuel is consumed.
The YouTube player allows users to watch or listen to YouTube videos by simply entering the video URL.
Requirements:
Python 3.x
PyQt5 and PyQtWebEngine
You can install the dependencies using the following command:

bash
Copy code
pip install PyQt5 PyQtWebEngine
Usage:
Clone the repository to your local machine:
bash
Copy code
git clone https://github.com/your-username/InfotainmentSystem.git
Navigate to the project directory:
bash
Copy code
cd InfotainmentSystem
Run the Python script:
bash
Copy code
python main.py

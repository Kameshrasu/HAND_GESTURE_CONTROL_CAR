# HAND_GESTURE_CONTROL_CAR

## Overview

This project demonstrates a car controlled by hand gestures using an Arduino and OpenCV. The system uses a webcam to capture hand movements, which are then processed using OpenCV to recognize gestures and send corresponding commands to the Arduino, which controls the car's movements.

## Features

- Hand gesture recognition using OpenCV
- Real-time control of the car using gestures
- Integration with Arduino for hardware control

## Components

- Arduino Uno
- DC motors and motor driver (L298N)
- Webcam
- Chassis for the car
- Power supply (batteries)
- Wires and connectors

## Software Requirements

- Python 3.11
- OpenCV
- PySerial
- Arduino IDE

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/yourusername/HAND_GESTURE_CONTROL_CAR.git
    cd HAND_GESTURE_CONTROL_CAR
    ```

2. **Install the required Python packages:**

    ```bash
    pip install opencv-python pyserial
    ```

3. **Upload the Arduino code:**
    - Open the Arduino IDE.
    - Connect your Arduino board to your computer.
    - Open the `arduino_code.ino` file located in the repository.
    - Select the correct board and port from the Tools menu.
    - Upload the code to the Arduino.




#!/usr/bin/env python3

"""
Silkroad team #2 implementation of the software of the robot for lab 3.
ECSE211 - Winter 2024
"""

from utils import sound
from utils.brick import TouchSensor, EV3UltrasonicSensor, wait_ready_sensors, reset_brick
from utils.brick import Motor, TouchSensor
from time import sleep
import concurrent.futures
import sys
import simpleaudio as sa

print("Program start.\nWaiting for sensors to turn on...")

TOUCH_SENSOR = TouchSensor(1)
STOP_TS = TouchSensor(3)
Sound_Sensor = TouchSensor(4)
US_SENSOR = EV3UltrasonicSensor(2)

drum_state = False
motor = Motor("C")

wait_ready_sensors(True)  # Input True to see what the robot is trying to initialize! False to be silent.
print("Done waiting.")


def pitch_us(us_data):
    """Converts ultrasonic sensor data to a musical pitch."""
    pitch = 0
    if 40 > us_data > 30:
        pitch = "A4"
    elif 30 > us_data > 20:
        pitch = "A3"
    elif 20 > us_data > 10:
        pitch = "Gb4"
    elif 10 > us_data > 0:
        pitch = "C#5"
    return pitch


def drum(drum_state, m):
    """Controls the drum based on the drum_state."""
    if drum_state:
        m.set_position_relative(-25)
        sleep(0.5)
        m.set_position_relative(25)
        sleep(0.5)


print("READY")


def sound_loop():
    """Continuously checks the ultrasonic sensor and plays a sound based on its distance."""
    while not STOP_TS.is_pressed():
        sleep(0.01)
        us_data = US_SENSOR.get_value()
        print(us_data)
        pitch = pitch_us(us_data)

        if pitch != 0:
            s = sound.Sound(duration=0.1, volume=100, pitch=pitch)
            if Sound_Sensor.is_pressed():
                s.play().wait_done()


def drum_loop():
    """Controls the drum based on the touch sensor input."""
    motor.set_position(20)
    drum_state = False
    sleep(2)
    while not STOP_TS.is_pressed():
        if TOUCH_SENSOR.is_pressed():
            print("touch_sensor")
            drum_state = not drum_state
        drum(drum_state, motor)
    print("EMERGENCY BUTTON PRESSED")

    motor.set_position(0)
    sys.exit()


# Using ThreadPoolExecutor to run sound_loop and drum_loop concurrently
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
    executor.submit(sound_loop)
    executor.submit(drum_loop)

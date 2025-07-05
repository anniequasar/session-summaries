#!/usr/bin/env python3
r"""MeetUp 167 - Beginners' Python and Machine Learning - 30 Nov 2022 - Internet of Things for Raspberry Pi

Youtube: https://youtu.be/RviGbg8f-Es
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/289663754/
Github:  https://github.com/timcu/session-summaries/tree/master/online

Raspberry Pi program to let LED lights be turned on and off using message queue mqtt

Choose resistors for Raspberry Pi to limit current below 16 mA from 3.3V supply voltage. Below 5 mA even safer.
If in doubt use bigger resistor.

For push buttons I used 10kΩ resistors.
brown-black-orange-gold (brown=1, black=0, orange=1000, gold=±5%) => 10 x 1000Ω  ±5%
For LEDs I used 560Ω resistors.
green-blue-brown-gold (green=5, blue=6, brown=10, gold=±5%) => 56 x 10Ω  ±5%

Run meetup167_tim_internet_of_things.py to create a better schematic in svg format.

GND ──┬────────────────┬─────┬─────┬─────┬──────────────┐
      ⌇                │     │     │     │              ⌇
     10kΩ              │     ⏄↗↗  ⏄↗↗  ⏄↗↗          10kΩ
      │                │    red   blue green            │
      ├───────┐        │     │     │     │        ┌─────┤
      │       │        │     ⌇    ⌇    ⌇        │     │
      │       │        │    560Ω  560Ω  560Ω      │     │
      │    ┌──┴────────┴─────┴─────┴─────┴────────┴─┐   │
      │    │  17      GND   24    26    12        27│   │
      │    │                                        │   │
      │    │      Raspberry Pi 3B+                  │   │
      │    │                                        │   │
      │    │          3V3                           │   │
      │    └───────────┬────────────────────────────┘   │
      │                │                                │
        ╱              │                                  ╱
       ╱               │                                 ╱
3.3V ─┴────────────────┴────────────────────────────────┘

# Create a virtual environment called bpaml167
python3 -m venv bpaml167

# Activate the virtual environment
source bpaml167/bin/activate

# Create a file called requirements.txt
nano requirements.txt
paho-mqtt
rpi.gpio


"""

import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt
import logging

logging.basicConfig(level=logging.DEBUG)

GREEN = 12
BLUE = 26
RED = 24
LEFT = 17
RIGHT = 27
MQTT = "bpaml.pythonator.com"
dct_led = {"green": GREEN, "blue": BLUE, "red": RED}


def setup_leds_and_buttons():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(GREEN, GPIO.OUT)
    GPIO.setup(RED, GPIO.OUT)
    GPIO.setup(BLUE, GPIO.OUT)
    GPIO.setup(LEFT, GPIO.IN)
    GPIO.setup(RIGHT, GPIO.IN)
    print("testing leds")
    for led in [GREEN, BLUE, RED] * 3:
        for led_state in (True, False):
            GPIO.output(led, led_state)
            time.sleep(0.2)
    print("press and hold left button until blue led flashes")
    while not GPIO.input(LEFT):
        GPIO.output(GREEN, True)
        time.sleep(0.1)
        GPIO.output(GREEN, False)
        time.sleep(0.1)
    print("press and hold right button until red led flashes")
    while not GPIO.input(27):
        GPIO.output(BLUE, True)
        time.sleep(0.1)
        GPIO.output(BLUE, False)
        time.sleep(0.1)
    for i in range(3):
        GPIO.output(RED, True)
        time.sleep(0.1)
        GPIO.output(RED, False)
        time.sleep(0.1)


def on_message(client, userdata, message):
    s = message.payload.decode()
    print(f"bpaml: {s}")


def on_command_to_pi(client, userdata, message):
    s = message.payload.decode()
    cmds = s.split()
    if len(cmds) > 1:
        if cmds[0] in dct_led:
            print(f"bpaml/pi: {s} {dct_led[cmds[0]]} {cmds[1]=='on'}")
            GPIO.output(dct_led[cmds[0]], cmds[1] == "on")


def pub_and_sub_to_mqtt():
    client = mqtt.Client()
    client.enable_logger(logger=logging.getLogger())
    client.on_message = on_message
    client.message_callback_add("bpaml/pi", on_command_to_pi)
    client.connect(MQTT)
    client.publish("bpaml/pi", "raspberry pi is publishing")
    client.subscribe(topic="bpaml", qos=1)
    client.subscribe(topic="bpaml/pi", qos=1)
    client.loop_start()
    try:
        tf_left_prev = False
        tf_right_prev = False
        while True:
            tf_left = GPIO.input(LEFT)
            tf_right = GPIO.input(RIGHT)
            if tf_left and not tf_left_prev:
                client.publish("bpaml/pi", "left button pressed")
            elif not tf_left and tf_left_prev:
                client.publish("bpaml/pi", "left button released")
            if tf_right and not tf_right_prev:
                client.publish("bpaml/pi", "right button pressed")
            elif not tf_right and tf_right_prev:
                client.publish("bpaml/pi", "right button released")
            tf_left_prev = tf_left
            tf_right_prev = tf_right
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("ctrl-c has been pressed on keyboard")
    finally:
        client.loop_stop()
        print("disconnecting and cleaning up")
        client.disconnect()
        GPIO.cleanup()


if __name__ == "__main__":
    setup_leds_and_buttons()
    pub_and_sub_to_mqtt()

r"""MeetUp 167 - Beginners' Python and Machine Learning - 30 Nov 2022 - Internet of Things

Youtube: https://youtu.be/RviGbg8f-Es
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/289663754/
Github:  https://github.com/timcu/session-summaries/tree/master/online

Learning objectives:
- How to send messages to other Python programs using a message queue
- Controlling a Raspberry Pi from your PC

@author D Tim Cummings

Install Software
- Install Python 3.11.0 from https://www.python.org/downloads/
 - Python 3.8 or later will work
 - necessary for running python on your computer
 - alternatively can install anaconda which includes many third party libraries
- Optional: PyCharm Community Edition 2022.2.3 from https://www.jetbrains.com/pycharm/download/
 - Integrated Development Environment (IDE)
 - Easier to write programs

Create a file called requirements.txt with the following contents
```
paho-mqtt
schemdraw
```

Run MQTT broker
(Port forward from router to 1883 if access outside intranet required)

For example using docker
```
nano mosquitto.config
listener 1883
allow_anonymous true
log_type all

sudo docker run --rm -it --name mosquitto -p 1883:1883 -v $(pwd):/mosquitto/config:ro eclipse-mosquitto
```
"""
import paho.mqtt.client as mqtt

import datetime
import logging
import time


# logging was not covered in the session, but it is possible to use a logger with mqtt
# change the logging level from logging.WARNING to logging.INFO or logging.DEBUG to use
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def draw_schematic(show=False):
    """Draws electrical circuit for Raspberry Pi and saves in file rpi_circuit.svg viewable in a browser"""
    # https://schemdraw.readthedocs.io
    import schemdraw
    import schemdraw.elements as elm

    with schemdraw.Drawing(file="rpi_circuit.svg", show=show) as d:
        d.config(fontsize=12, bgcolor="white")
        rpi_def = elm.Ic(pins=[elm.IcPin(name='GPIO17', side='left', pin='11'),
                               elm.IcPin(name='GND', side='bot', pin='6'),
                               elm.IcPin(name='GPIO24', side='bot', pin='18'),
                               elm.IcPin(name='GPIO26', side='bot', pin='37'),
                               elm.IcPin(name='GPIO12', side='bot', pin='32'),
                               elm.IcPin(name='GPIO27', side='right', pin='13'),
                               elm.IcPin(name='3V3', side='top', pin='1'),
                               ],
                         edgepadW=1,
                         edgepadH=1,
                         pinspacing=3,
                         leadlen=2,
                         label='Raspberry Pi 3B+')
        d += (T := rpi_def)
        d += elm.Dot().at(T.inT1)
        d += elm.Dot().at(T.GPIO17)
        d += elm.Dot().at(T.GPIO27)
        d += elm.Resistor().at(T.GPIO24).down().label('560Ω')
        d += (RED_LED := elm.LED().label('red'))
        d += elm.Dot()
        d += elm.Resistor().at(T.GPIO26).label('560Ω')
        d += elm.LED().label('blue')
        d += elm.Dot()
        d += elm.Resistor().at(T.GPIO12).label('560Ω')
        d += elm.LED().label('green')
        d += elm.Dot()
        d += elm.Line().at(T.GND).toy(RED_LED.end)
        d += elm.Dot()
        d += elm.Ground()
        d += (LEFT := elm.Resistor().at(T.GPIO17).down().toy(RED_LED.end).label("10kΩ"))
        d += elm.Dot()
        d += elm.Resistor().at(T.GPIO27).down().toy(RED_LED.end).label("10kΩ")
        d += elm.Dot()
        d += elm.Line().left().tox(LEFT.end - 0.5).label("GND", "left")
        d += elm.Button().up().at(T.GPIO17).label("left\nbutton").toy(T.inT1)
        d += elm.Dot()
        d += elm.Button().up().flip().at(T.GPIO27).label("right\nbutton", "bottom").toy(T.inT1)
        d += elm.Dot()
        d += elm.Line().left().tox(LEFT.start - 0.5).label("3.3V", "left")


# call draw_schematic(show=True) to see how to wire up Raspberry Pi if you want to create this whole experiment
draw_schematic(show=False)
# Leave following line commented out so that rest of script will run
# quit()


def now():
    """useful function for timestamping messages"""
    return datetime.datetime.now().strftime("%H:%M:%S.%f")


# To complete the following challenges use as a guide
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/

# Challenge 1: Install Python package paho-mqtt. Write a Python script to
# 1. connect to mqtt message broker bpaml.pythonator.com
# 2. send a message to topic "bpaml" which is your name

broker_url = "bpaml.pythonator.com"
broker_port = 1883
topic = "bpaml"
topic_window = topic + "/window"
topic_wall = topic + "/wall"
topic_pi = topic + "/pi"

# Create an object of class mqtt.Client.
client1 = mqtt.Client()
# Initiate a connection to the server "bpaml.pythonator.com".
client1.connect(broker_url)
# send a message for everyone subscribed to topic "bpaml"
# Quality of service qos:
# 0: not guaranteed to get through. Lowest overhead
# 1: guaranteed to get through but may get duplicates. Moderate overhead
# 2: guaranteed to get through exactly once per client. Highest overhead
# retain=False -> only show message to those subscribers currently connected
# retain=True  -> retain message on server so people who connect later can see it
client1.publish(topic=topic, payload=f"Tim's challenge 1 message at {now()}", qos=0, retain=True)
# Disconnect from server
client1.disconnect()
# quit()

# Challenge 2: Subscribe to other people's messages by setting call back functions on your mqtt.Client object


def on_connect(client, userdata, flags, rc):
    """Callback function for mqtt.Client to call when a connection to server is made"""
    logger.info(f"{userdata} connected with result code {rc}")


def on_disconnect(client, userdata, rc):
    """Callback function for mqtt.Client to call when a connection to server is dropped"""
    logger.info(f"{userdata} got disconnected with result code {rc}")


def on_message(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpaml"""
    logger.info(f"{userdata} {now()} message received: {message.payload.decode()}")


# Create an object of class mqtt.Client. "userdata" allows me to identify which client in the call back functions
client2 = mqtt.Client(userdata="Challenge 2:")
# Assign callback functions to object client2. Notice we are referring to function names without parentheses ()
client2.on_connect = on_connect
client2.on_disconnect = on_disconnect
client2.on_message = on_message
# Initiate a connection to the server "bpaml.pythonator.com". When successful callback on_connect will be called
client2.connect(broker_url)
# Subscribe to topic bpaml. If a message comes on this channel, the function on_message will be called
client2.subscribe(topic=topic, qos=0)
# Publish a message to topic bpaml. As we are previously subscribed we should get the message back ourselves
client2.publish(topic=topic, payload=f"Tim's challenge 2 message at {now()}", qos=0, retain=True)
# If this was the last lines of my script I could call client2.loop_forever()
# However I want to only loop for 5 seconds listening for other messages and during that time I want to
# count down from 5 to 1
client2.loop_start()
for counter in range(5, 0, -1):
    time.sleep(1)
    print(counter, end=' ')
    # important to call sleep so that my main thread can sleep while other threads are running
print()
# Stop the loop so that no more messages are retrieved
client2.loop_stop()
client2.disconnect()
# quit()

# Challenge 3: Subscribe to more than one topic with different on_message callbacks for each one.
# Topics: bpaml, bpaml/window, bpaml/wall, bpaml/pi


def on_message_from_window(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpaml/window"""
    logger.info(f"{userdata} {now()} message received window: {message.payload.decode()}")


def on_message_from_wall(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpaml/wall"""
    logger.info(f"{userdata} {now()} message received wall: {message.payload.decode()}")


def on_message_from_pi(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpaml/pi"""
    logger.info(f"{userdata} {now()} message received pi: {message.payload.decode()}")


# Although not required by this challenge, I have set clean_session to False in the constructor.
# clean_session=False means the server will provide me all data received since I last connected
# clean_session=True  means the server will clean out any outstanding data and just return the last retained message
# To use sessions you will need a unique client_id. To get a client_id which will almost always be unique
# type the following line (after the #) into Python Console
# import uuid; print(uuid.uuid4())
client3 = mqtt.Client(client_id="02d961ed-2a4d-4bb8-a12e-755e26ebcf18", clean_session=False, userdata="Challenge 3:")
client3.enable_logger(logger=logging.getLogger(__name__))
# will is only executed if connection dies without being disconnected
client3.will_set(topic=topic, payload=f"Tim's connection6 has left the building {now()}", qos=1, retain=True)
# client6 will use the same on_connect, on_disconnect and on_message as client5
client3.on_connect = on_connect
client3.on_disconnect = on_disconnect
client3.on_message = on_message
# However to use different callbacks based on which topic the message was published on I use message_callback_add
client3.message_callback_add(topic_window, on_message_from_window)
client3.message_callback_add(topic_wall, on_message_from_wall)
client3.message_callback_add(topic_pi, on_message_from_pi)
client3.connect(broker_url, broker_port)
client3.subscribe(topic=topic, qos=1)
client3.subscribe(topic=topic_window, qos=1)
client3.subscribe(topic=topic_wall, qos=1)
client3.subscribe(topic=topic_pi, qos=1)
client3.publish(topic=topic, payload=f"Tim's challenge 3 message at {now()}", qos=1)
client3.publish(topic=topic_window, payload=f"Message to the window group from Tim at {now()}", qos=1)
client3.loop_start()
for counter in range(5, 0, -1):
    time.sleep(1)
    print(counter, end=' ')
    # important to call sleep so that my main thread can sleep while other threads are running
print()
client3.loop_stop()
client3.disconnect()
# quit()


# Challenge 4: Connect with client_id and publish several messages to broker.
# Then connect with clean_session=False to recover messages which have arrived since last connected
# Use will_set() to ensure a message gets sent if connection lost


# We will use client3 as our client to receive all messages published since last connection
# Hence client4 only has to publish several messages (more than 1) and then next time we run client3 we
# can see if it gets them all
client4 = mqtt.Client(userdata="Challenge 4:")
client4.will_set(topic=topic, payload=f"Tim's connection4 has left the building {now()}", qos=1, retain=True)
client4.on_disconnect = on_disconnect
client4.connect(broker_url, broker_port)
for i in range(10):
    client4.publish(topic=topic_window, payload=f"Msg {i} to the window group from Tim at {now()}", qos=1, retain=True)
for led in ['green', 'blue', 'red']:
    client4.publish(topic=topic_pi, payload=f"{led} on")
    time.sleep(1)
    client4.publish(topic=topic_pi, payload=f"{led} off")

client4.disconnect()
# We have disconnected properly so shouldn't get the client4.will_set message

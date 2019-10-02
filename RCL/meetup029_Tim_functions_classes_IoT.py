#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MeetUp 029 - Beginners Python Support Sessions - Tue 24 Sep 2019 - Functions, Classes and Internet of Things

Learning objectives:
    functions: define, call, pass
    classes: create, use
    IoT: How to use MQTT message queues for IoT communications

@author D Tim Cummings

"""
# Following needs paho-mqtt in requirements.txt
# Or alternatively in your virtual environment 'pip3 install paho-mqtt'
import paho.mqtt.client as mqtt

import datetime
import time
import logging

# logging was not covered in the session but it is possible to use a logger with mqtt
# change the logging level from logging.INFO to logging.DEBUG to use
logging.getLogger().setLevel(logging.INFO)

# Demo: functions


def show_now():
    """Simple example of a function which prints the current time"""
    print("The time is now", datetime.datetime.now())


# call a function by using function name followed by parentheses ()
show_now()
show_now()

# Challenge 1: Write a function which shows how much time is left in this session
# Hint: datetime.datetime.combine(dt1, dt2) combines date from dt1 with time from dt2
# Hint: Time 8pm  datetime.time(hour=20)


def show_time_left():
    """prints the amount of time from now until 8pm"""
    now = datetime.datetime.now()
    end = datetime.datetime.combine(now, datetime.time(hour=20))
    logging.debug(f"now: {now}, end: {end}")
    print("Challenge 1: Time left in session is", end-now)


show_time_left()

# Demo: functions returning values


def str_now():
    """Example of a function which returns the current time as a str hours:minutes:seconds.microseconds"""
    return datetime.datetime.strftime(datetime.datetime.now(), "%H:%M:%S.%f")


# example of using the return value of a function in a print command
print("The time is now", str_now())
# docstrings in a function can be read using the help command.
# Notice how he pass the function name without parentheses if we don't want to run it but get a reference to it.
# Uncomment the next line to see in action
# help(str_now)


def flt_f_from_c(deg_celsius):
    """Example of a function which takes a parameter (Temperature in degrees Celsius)
    and returns a value (Temperature in degrees Fahrenheit)"""
    return deg_celsius * 1.8 + 32


# Example of calling a function many times and printing results in a table
print("Celsius  Fahrenheit")
for c in (0, 100, -40):
    print(f"{c:>7.2f}  {flt_f_from_c(c):>10.2f}")

# Challenge 2: Write a function which capitalises every word in a sentence.
# Test on "don't be surPrised"


def capitalise_as_per_session(sentence):
    """Returns the sentence in lower case but with every first letter in upper case"""
    words = sentence.split()
    capitalised_words = []
    for word in words:
        capitalised_words.append(word[0].upper() + word[1:].lower())
    return ' '.join(capitalised_words)


def capitalise(sentence):
    """Returns the sentence in lower case but with every first letter in upper case
    Different from previous example by using list comprehension to build capitalised_words """
    words = sentence.split()
    capitalised_words = [w[0].upper() + w[1:].lower() for w in words]
    return ' '.join(capitalised_words)


print("Challenge 2:", capitalise_as_per_session("don't be surPrised"))
print("Challenge 2 (using list comprehension):", capitalise("don't be surPrised"))

# Demo: class


class DemoClass1:
    pass


# create an object of the new class
dc = DemoClass1()
print(dc)
print(type(dc))
# new or existing attributes on class objects can be assigned using dot notation
dc.my_attribute = 'new attributes can be added'
print(dc.my_attribute)


class DemoClass2:
    """Class with 3 attributes, a, b, a_plus_b"""
    a = 'predefined attribute'

    def __init__(self, value):
        """function called when class constructor used"""
        self.b = value

    # class functions need a parameter for the object itself. Can be called anything but everyone calls it self
    def a_plus_b(self):
        """class function to concatenate attributes a and b"""
        return self.a + self.b


dc = DemoClass2('from constructor')
# class functions can be called two ways
print(dc.a_plus_b())  # common way
print(DemoClass2.a_plus_b(dc))  # equivalent way

# Challenge 3: Write a class MyClass with a docstring and an attribute 'created' which stores
# the time object was created
# and a function 'age' which returns how old the object is.


class MyClass:
    """Challenge 3 solution"""
    def __init__(self):
        self.created = datetime.datetime.now()

    def age(self):
        return datetime.datetime.now() - self.created


my_class_obj = MyClass()
print("Challenge 3: first call to my_class_obj.age()", my_class_obj.age())
print("Challenge 3: a bit older when second call to my_class_obj.age()", my_class_obj.age())

# To complete the following challenges use as a guide
# https://mntolia.com/mqtt-python-with-paho-mqtt-client/

# Challenge 4: Install Python package paho-mqtt. Write a Python script to
# 1. connect to mqtt message broker sas-select.triptera.com.au
# 2. send a message to topic "bpss" which is your name

broker_url = "sas-select.triptera.com.au"
broker_port = 1883
topic = "bpss"
topic_window = topic + "/window"
topic_wall = topic + "/wall"
topic_pi = topic + "/pi"

# Create an object of class mqtt.Client.
client4 = mqtt.Client()
# Initiate a connection to the server "sas-select.triptera.com.au".
client4.connect(broker_url)
# send a message for everyone subscribed to topic "bpss"
# Quality of service qos:
# 0: not guaranteed to get through. Lowest overhead
# 1: guaranteed to get through but may get duplicates. Moderate overhead
# 2: guaranteed to get through exactly once per client. Highest overhead
# retain=False -> only show message to those subscribers currently connected
# retain=True  -> retain message on server so people who connect later can see it
client4.publish(topic=topic, payload=f"Tim's challenge 4 message at {str_now()}", qos=0, retain=True)
# Disconnect from server
client4.disconnect()

# Challenge 5: Subscribe to other people's messages by setting call back functions on your mqtt.Client object


def on_connect(client, userdata, flags, rc):
    """Callback function for mqtt.Client to call when a connection to server is made"""
    print(f"{userdata} connected with result code ", rc)


def on_disconnect(client, userdata, rc):
    """Callback function for mqtt.Client to call when a connection to server is dropped"""
    print(f"{userdata} got disconnected rc: {rc}")


def on_message(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpss"""
    print(f"{userdata} {str_now()} message received: {message.payload.decode()}")


# Create an object of class mqtt.Client. "userdata" allows me to identify which client in the call back functions
client5 = mqtt.Client(userdata="Challenge 5:")
# Assign callback functions to object client5. Notice we are referring to function names without parentheses ()
client5.on_connect = on_connect
client5.on_disconnect = on_disconnect
client5.on_message = on_message
# Initiate a connection to the server "sas-select.triptera.com.au". When successful callback on_connect will be called
client5.connect(broker_url)
# Subscribe to topic bpss. If a message comes on this channel, the function on_message will be called
client5.subscribe(topic=topic, qos=0)
# Publish a message to topic bpss. As we are previously subscribed we should get the message back ourselves
client5.publish(topic=topic, payload=f"Tim's challenge 5 message  at {str_now()}", qos=0, retain=True)
# If this was the last lines of my script I could call client5.loop_forever()
# However I want to only loop for 5 seconds listening for other messages and during that time I want to
# count down from 5 to 1
client5.loop_start()
for counter in range(5, 0, -1):
    time.sleep(1)
    print(counter, end=' ')
    # important to call sleep so that my main thread can sleep while other threads are running
print()
# Stop the loop so that no more messages are retrieved
client5.loop_stop()
client5.disconnect()

# Challenge 6: Subscribe to more than one topic with different on_message callbacks for each one.
# Topics: bpss, bpss/window, bpss/wall, bpss/pi


def on_message_from_window(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpss/window"""
    print(f"{userdata} {str_now()} message received window: {message.payload.decode()}")


def on_message_from_wall(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpss/wall"""
    print(f"{userdata} {str_now()} message received wall: {message.payload.decode()}")


def on_message_from_pi(client, userdata, message):
    """Callback function for mqtt.Client to call when a message received from server on topic bpss/pi"""
    print(f"{userdata} {str_now()} message received pi: {message.payload.decode()}")


# Although not required by this challenge, I have set clean_session to False in the constructor.
# clean_session=False means the server will provide me all data received since I last connected
# clean_session=True  means the server will clean out any outstanding data and just return the last retained message
# To use sessions you will need a unique client_id. To get a client_id which will almost always be unique
# type the following two lines into Python Console
# import uuid
# uuid.uuid(4)
client6 = mqtt.Client(client_id="02d961ed-2a4d-4bb8-a12e-755e26ebcf18", clean_session=False, userdata="Challenge 6:")
client6.enable_logger(logger=logging.getLogger())
# will is only executed if connection dies without being disconnected
client6.will_set(topic=topic, payload=f"Tim's connection6 has left the building {str_now()}", qos=1, retain=True)
# client6 will use the same on_connect, on_disconnect and on_message as client5
client6.on_connect = on_connect
client6.on_disconnect = on_disconnect
client6.on_message = on_message
# However to use different callbacks based on which topic the message was published on I use message_callback_add
client6.message_callback_add(topic_window, on_message_from_window)
client6.message_callback_add(topic_wall, on_message_from_wall)
client6.message_callback_add(topic_pi, on_message_from_pi)
client6.connect(broker_url, broker_port)
client6.subscribe(topic=topic, qos=1)
client6.subscribe(topic=topic_window, qos=1)
client6.subscribe(topic=topic_wall, qos=1)
client6.subscribe(topic=topic_pi, qos=1)
client6.publish(topic=topic, payload=f"Tim's challenge 6 message  at {str_now()}", qos=1)
client6.publish(topic=topic_window, payload=f"Message to the window group from Tim at {str_now()}", qos=1)
client6.loop_start()
for counter in range(5, 0, -1):
    time.sleep(1)
    print(counter, end=' ')
    # important to call sleep so that my main thread can sleep while other threads are running
print()
client6.loop_stop()
client6.disconnect()

# Challenge 7: Connect with client_id and publish several messages to broker.
# Then connect with clean_session=False to recover messages which have arrived since last connected
# Use will_set() to ensure a message gets sent if connection lost


# We will use client6 as our client to receive all messages published since last connection
# Hence client7 only has to publish several messages (more than 1) and then next time we run client6 we
# can see if it gets them all
client7 = mqtt.Client(userdata="Challenge 7:")
client7.will_set(topic=topic, payload=f"Tim's connection7 has left the building {str_now()}", qos=1, retain=True)
client7.on_disconnect = on_disconnect
client7.connect(broker_url, broker_port)
for i in range(10):
    client7.publish(topic=topic_window, payload=f"Message {i} to the window group from Tim at {str_now()}", qos=1, retain=True)
for led in ['green', 'blue', 'red']:
    client7.publish(topic=topic_pi, payload=f"{led} on")
    time.sleep(1)
    client7.publish(topic=topic_pi, payload=f"{led} off")

client7.disconnect()
# We have disconnected properly so shouldn't get the client7.will_set message

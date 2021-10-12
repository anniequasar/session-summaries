#! /usr/bin/env python3
r"""MeetUp 119 - Beginners' Python and Machine Learning - 12 Oct 2021 - Network sockets in Python

Youtube: https://youtu.be/LYDeML_x_Tc
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/281213657/
Github:  https://github.com/anniequasar/session-summaries.git

Learning objectives:
- Communicating between programs over the network in Python

@author D Tim Cummings

Task 1: Implement echo-server.py and echo-client.py from https://realpython.com/python-sockets/

Task 2: What happens if echo-client only receives 4 bytes instead of 1024 bytes

Task 3: Change message to 11 bytes and ensure client receives all bytes, 4 at a time

Task 4: In client set recv timeout using s.settimeout(3.0) and catch exception socket.timeout

Task 5: Change server to receive data 3 bytes at a time

Task 6: Modify echo-server to return data in reverse. Use recv buffer 4096 bytes

Task 7: Send unicode characters from echo-client.py eg 🐍 🐢 🇭🇲. Use recv buffer 4096 bytes, str.encode bytes.decode

Task 8: Modify echo-server to become print-server. Doesn't echo, only prints. Receives multiple consecutive
(not concurrent) connections. Finishes when connection says b'shutdown'
"""
import logging
import socket
import sys

from pathlib import Path

host = '127.0.0.1'  # Standard loopback interface address (localhost)
port = 65432  # port to listen on (non-privileged ports are > 1023)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sol_1_server():
    """Task 1: Implement echo-server.py and echo-client.py from https://realpython.com/python-sockets/"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            logger.info(f'Connected by {addr}')
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                conn.sendall(data)


def sol_1_client():
    """Task 1: Implement echo-server.py and echo-client.py from https://realpython.com/python-sockets/"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello, world')
        data = s.recv(1024)
    logger.info(f'Received {data!r} {len(data)} {bool(data)}')


def sol_2_client():
    """Task 2: What happens if echo-client only receives 4 bytes instead of 1024 bytes"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello, world')
        data = s.recv(4)

    logger.info(f'Received {data!r}')


def sol_3_client():
    """Task 3: Change message to 11 bytes and ensure client receives all bytes, 4 at a time"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello world')
        while True:
            data = s.recv(4)
            logger.info(f'Received {data!r} {len(data)} {bool(data)}')
            if not data:
                # BUG Doesn't detect end of data stream because server won't (and shouldn't) initiate disconnect
                break


def sol_4_client():
    """Task 4: In client set recv timeout using s.settimeout(3.0) and catch exception socket.timeout"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'Hello world')
        s.settimeout(3.0)
        while True:
            try:
                data = s.recv(4)
                logger.info(f'Received {data!r} {len(data)} {bool(data)}')
            except socket.timeout:
                logger.info('Timed out')
                data = None
            if not data:
                break


def sol_5_server():
    """Task 5: Change server to receive data 3 bytes at a time"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            logger.info(f'Connected by {addr}')
            while True:
                data = conn.recv(3)
                logger.info(f'Received {data!r} {len(data)} {bool(data)}')
                if not data:
                    break
                conn.sendall(data)


def sol_6_server():
    """Task 6: Modify echo-server to return data in reverse. Use recv buffer 4096 bytes"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            logger.info(f'Connected by {addr}')
            all_data = b''
            while True:
                data = conn.recv(4096)
                all_data += data
                logger.info(f'Received {data!r} {len(data)} {bool(data)}')
                if not data:
                    break
                conn.sendall(all_data[::-1])


def sol_7_server():
    """Task 7: Send unicode characters from client eg 🐍 🐢 🇭🇲. Use recv buffer 4096 bytes, str.encode bytes.decode"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()
        with conn:
            logger.info(f'Connected by {addr}')
            while True:
                data = conn.recv(4096)
                logger.info(f'Received {data!r} {data.decode("UTF-8")!r} {len(data)} {bool(data)}')
                if not data:
                    break
                conn.sendall(data.decode('UTF-8')[::-1].encode('UTF-8'))


def sol_7_client():
    """Task 7: Send unicode characters from client eg 🐍 🐢 🇭🇲. Use recv buffer 4096 bytes, str.encode bytes.decode"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall('Hello 🐍 🐢 🇭🇲 world'.encode('UTF-8'))
        s.settimeout(3.0)
        while True:
            try:
                data = s.recv(4096)
                logger.info(f'Received {data!r} {data.decode("UTF-8")!r} {len(data)} {bool(data)}')
            except socket.timeout:
                logger.info('Timed out')
                data = None
            if not data:
                break


def sol_8_server():
    """Task 8: Modify echo-server to become print-server. Doesn't echo, only prints.

    Receives multiple consecutive (not concurrent) connections.
    Finishes when connection says 'shutdown'"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        my_buf = b''
        while my_buf != b'shutdown':
            logging.info('waiting for a connection')
            conn, addr = s.accept()
            with conn:
                logger.info(f'Connected by {addr}')
                my_buf = b''
                while True:
                    data = conn.recv(4096)
                    my_buf += data
                    if not data:
                        break
                my_buf = my_buf.replace(b'\r\n', b'\n')
                lines = my_buf.decode('UTF-8').split('\n')
                for i, line in enumerate(lines):
                    print(f"{i:>3d}: {line}")
                print('\n\n\n')
                if my_buf == b'shutdown':
                    break


def sol_8_client():
    """Task 8: Modify echo-server to become print-server. Doesn't echo, only prints.

    Receives multiple consecutive (not concurrent) connections.
    Finishes when connection says 'shutdown'"""
    for p in Path('.').glob('*.py'):
        with open(p, 'rb') as file:
            logger.info(f"File: {p}")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                # Use different buffer sizes for file and socket to show they don't need to be the same
                while b := file.read(8192):
                    s.sendall(b)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b'shutdown')


if len(sys.argv) != 3:
    print("usage:", sys.argv[0], "<client/server> <solution>")
    print("example: ", sys.argv[0], "s", 3)
    sys.exit(1)

sol = int(sys.argv[2]) - 1
cs = sys.argv[1]
if cs == 's':
    solutions = [sol_1_server, sol_1_server, sol_1_server, sol_1_server,
                 sol_5_server, sol_6_server, sol_7_server, sol_8_server]
else:
    solutions = [sol_1_client, sol_2_client, sol_3_client, sol_4_client,
                 sol_4_client, sol_4_client, sol_7_client, sol_8_client]
solutions[sol]()

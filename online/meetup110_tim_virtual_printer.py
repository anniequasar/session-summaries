#!/usr/bin/env python3
r"""MeetUp 110 - Beginners' Python and Machine Learning - 10 Aug 2021 - Print to xlsx printer in Python

Youtube: https://youtu.be/rEf4H6_FJ94
Meetup:  https://www.meetup.com/Beginners-Python-Machine-Learning/events/279540703/
Github:  https://github.com/timcu/bpaml-sessions.git

Learning objectives:
- Create a Print-to-xlsx virtual printer

@author D Tim Cummings

Task 1. Download Beginners' Python and Machine Learning repository

Install git from https://git-scm.com
Open bash command line (Git-Bash on Windows, Terminal in Mac or Linux) and move to good folder
I have a folder called github for all my cloned repos
    mkdir github
    cd github
    git clone https://github.com/timcu/bpaml-sessions.git
    cd session-summaries/online


Task 2. In a separate window write a simple Python socket server listening on port 9100

Task 2a: Windows - Create a virtual environment
    python -m venv bpaml110
    bpaml110\Scripts\Activate
    pip install xlsxwriter

Task 2b: Mac / Linux - Create a virtual environment
    python3 -m venv bpaml110
    source bpaml110/bin/activate
    pip install xlsxwriter

Task 3 Run this script or see example at https://realpython.com/python-sockets/
python meetup110_tim_virtual_printer.py --mode CLIENT
python meetup110_tim_virtual_printer.py --mode SERVER

https://blog.emojipedia.org/emoji-flags-explained/

Task 4a. Create a generic text-only printer - Windows

Create a generic text-only printer connecting by network to port 9100
Windows printing:
Settings > Add printer > My printer isn't listed
Add a printer using TCP/IP address or hostname
Device type: TCP/IP Device, Hostname: 127.0.0.1, Portname: 127.0.0.1 (IP address of computer running python)
Device Type: Standard: Generic network card
Manufacturer: Generic, Printers: Generic / Text Only
Use installed driver
Printer name: print-to-xlsx
Share

Task 4b. Create a generic text-only printer - Mac / Linux

CUPS printing (Mac or Linux):
# Administering locally
cupsctl WebInterface=yes  # probably already the case on Linux
# Browser http://localhost:631 or https://localhost:631

# Administering remotely. Example assumes:
# cups server ip address is 192.168.0.3
# python virtual printer ip address is 192.168.0.2
# Tunnel local computer (-L) port 6631 to localhost:631 on remote computer
ssh -L 6631:localhost:631 192.168.0.3
# In browser
https://localhost:6631

Click [Add printer], AppSocket/HP JetDirect, socket://192.168.0.2:9100, Name: print-to-xlsx (don't need to share), Raw, Raw Queue [Add printer]

Task 5: Print one python file to printer and see if it saves it

python meetup110_tim_virtual_printer.py --mode SERVER-RECEIVE

print /D:\\my-computer\print-to-xlsx meetup109_tim_coding_introduction.py
lp -d print-to-xlsx meetup109_tim_coding_introduction.py

Task 6a: Windows. Run a commandline script to print all python scripts in online directory

https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/forfiles
https://docs.microsoft.com/en-us/windows-server/administration/windows-commands/print

# in one window
python meetup110_tim_virtual_printer.py --mode SERVER-XLSX

# in another window which has virtual environment active
forfiles /m *.py /c "cmd /c print /D:\\my-computer\print-to-xlsx @path"
python meetup110_tim_virtual_printer.py --mode SAVE-XLSX

Task 6b: Mac / Linux. Run a commandline script to print all python scripts in online directory

# in one window
python3 meetup110_tim_virtual_printer.py --mode SERVER-XLSX

# in another window which has virtual environment active
for f in *.py ; do cat $f | lp -d print-to-xlsx ; done
python3 meetup110_tim_virtual_printer.py --mode SAVE-XLSX
"""

import argparse
import datetime
import logging
import re
import socket
import sys
import xlsxwriter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="MeetUp110 Virtual Printer in Python")
    parser.add_argument('--log', default='INFO', action='store', help='set log level. eg: --log INFO',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])
    parser.add_argument('--mode', default='SERVER', action='store', help='CLIENT connects to existing server.\n'
                        'SERVER waits for connection from client, returns text to client then quits.\n'
                        'SERVER-XLSX receives multiple connections from client, stop with ctrl-c.',
                        choices=['CLIENT', 'SERVER', 'SERVER-RECEIVE', 'SERVER-XLSX', 'SAVE-XLSX'])
    args = parser.parse_args()
    numeric_level = getattr(logging, args.log.upper(), None)
    # logging.BASICFORMAT = '%(levelname)s:%(name)s:%(message)s'
    logging.basicConfig(level=numeric_level, format='%(levelname)s:%(name)s:%(funcName)s:%(message)s')
    mode = args.mode.upper()
else:
    # This module has been imported so don't run anything automatically. Just define the functions
    mode = "IMPORTED"

logger = logging.getLogger(__name__)

# specify Host and Port
HOST = '127.0.0.1'
PORT = 9100
API_SAVE_XLSX = b'save-xlsx'


def server_one():
    """Sends what it receives in reverse and quits after one connection"""
    logger.info("Running as a network socket server")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))  # host must refer to localhost. can be empty str
        logger.info(f"Bound to port {PORT} successfully. no other app using this port.")
        s.listen()
        logger.info(f"Listening on port {PORT}")
        conn, client_address = s.accept()
        with conn:
            logger.info(f"Connected by {client_address}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                logger.info(f"Received:\n{data}\nwhich decodes to \n{data.decode('UTF-8')}")
                conn.sendall(data.decode('UTF-8')[::-1].encode('UTF-8'))
        logger.info("Connection closed automatically because no longer in 'with conn' code block")
    logger.info("Socket closed automatically because no longer in 'with socket' code block")


def client_one():
    """Sends a message and then receives a message and then quits"""
    logger.info("Running as a network socket client")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall('Hello 🇭🇲'.encode('UTF-8'))
        data = s.recv(1024)
    logger.info(f"Received:\n{data}\nwhich decodes to\n{data.decode('UTF-8')}")


def client_save_xlsx():
    """Sends a message to print server which signals to save the data as a xlsx"""
    logger.info("Telling print server to save xlsx file")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(API_SAVE_XLSX)


def server_receive():
    """Receives data and quits after one connection"""
    logger.info("Running as a network socket server (receive only)")
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        logger.info(f"Listening on port {PORT}")
        connection, client_address = s.accept()
        with connection:
            logger.info(f"Connected by {client_address}")
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                data = data.replace(b'\r\n', b'\n')
                lines = data.decode("UTF-8").split("\n")
                for i, line in enumerate(lines):
                    print(f"{i:>3d}: {line!r}")


def parse_py(py_bytes, lst_title):
    """Find first of each title in python file (as bytes)"""
    first = {}
    lines = py_bytes.decode("UTF-8").replace("\r\n", "\n").split("\n")
    # docstrings start with """ or ''' but can have f and/or r in front of them
    ptn_docstring = re.compile(r"""^[fr]{0,2}['\"]{3}(.*)""")

    for line in lines:
        if "docstring" not in first and (m := ptn_docstring.match(line)):
            first["docstring"] = m.group(1)
        for title in lst_title:
            if title not in first and line.lower().startswith(f"{title.lower()}:"):
                first[title] = line[len(title) + 1:].strip()
    return first


def server_xlsx():
    logger.warning(f"Creating socket {PORT=}")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        # With the help of bind() function
        # binding host and port
        sock.bind((HOST, PORT))

    except socket.error as se:

        # if any error occurs then with the
        # help of sys.exit() exit from the program
        print('Bind failed. Error Code : ' + str(se[0]) + ' Message ' + se[1])
        sys.exit()

    # print if Socket binding operation completed
    logger.info('Socket binding operation completed')

    sock.listen()
    lst_parse = []
    my_buf = b''
    while my_buf != API_SAVE_XLSX:
        # Wait for a connection
        logger.info('waiting for a connection')
        connection, client_address = sock.accept()
        with connection:
            now = datetime.datetime.now()
            text_file_name = f"log_file_{now.strftime('%Y-%m-%d_%H%M%S%f')}.txt"
            logger.warning(f"{text_file_name=}")
            with open(text_file_name, "wb") as f:
                logger.info(f'connection from {client_address}')

                # Receive the data in small chunks and retransmit it
                my_buf = b''
                while True:
                    data = connection.recv(4096)
                    logger.debug(f'received "{data}"')
                    f.write(data)
                    if data:
                        logger.info(f'saving data from {client_address}')
                        # connection.sendall(data)
                        my_buf += data
                    else:
                        if my_buf != API_SAVE_XLSX:
                            lst_parse.append(parse_py(my_buf, ("Youtube", "Colab", "Meetup")))
                        logger.info(f"Number of documents received {len(lst_parse)}")
                        break
    # Save results to excel workbook
    with xlsxwriter.Workbook("bpaml-links.xlsx") as workbook:
        worksheet = workbook.add_worksheet("links")
        worksheet.set_column('A:D', 50)
        for i, dct_parse in enumerate(lst_parse):
            worksheet.write_string(i, 0, dct_parse.get("docstring", ""))
            worksheet.write_string(i, 1, dct_parse.get("Youtube", ""))
            worksheet.write_string(i, 2, dct_parse.get("Colab", ""))
            worksheet.write_string(i, 3, dct_parse.get("Meetup", ""))


if __name__ == "__main__":
    if mode == "SERVER":
        server_one()
    elif mode == "SERVER-RECEIVE":
        server_receive()
    elif mode == "SERVER-XLSX":
        server_xlsx()
    elif mode == "CLIENT":
        client_one()
    elif mode == "SAVE-XLSX":
        client_save_xlsx()

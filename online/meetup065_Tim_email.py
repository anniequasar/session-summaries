#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MeetUp 065 - Beginners' Python and Machine Learning - Tue 23 Jun 2020 - email

Youtube: https://youtu.be/YNOf4YNocWc
Source code:
https://raw.githubusercontent.com/anniequasar/session-summaries/master/TCB/meetup065_tim_email.py

Learning objectives:
- sending emails automatically from within Python program

@author D Tim Cummings

Refs:
https://aiosmtpd.readthedocs.io/
https://docs.python.org/3/library/email.examples.html
https://docs.python.org/3/library/smtplib.html
https://developers.google.com/gmail/api/quickstart/python      (sample code is compatible with both Python 2 and 3)
https://developers.google.com/gmail/api/guides/sending#python  (sample code is Python 2 not Python 3)
"""

import base64
import collections
import datetime
import imghdr
import os.path
import pickle
import smtplib
import unicodedata

from email.message import EmailMessage
from email.utils import make_msgid

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

EMAIL_TO = ""
IMAGE_FILE = "bpaml.jpg"

# Task 1. Set up Python project
"""
# If not using IDE such as PyCharm Community Edition, type the following on the command line
mkdir bpaml-email-pdf
cd bpaml-email-pdf
# Copy this file into that directory
"""
# Task 2. Create virtual environment
r"""
# If not using IDE type the following on the command line
python -m venv venv                         # Windows
python3 -m venv venv                        # Mac or Linux
conda create --name venv-email-pdf python   # Anaconda

# activate virtual environment
source venv/bin/activate                    # Mac or Linux or Windows Git-Bash
conda activate venv-email-pdf               # Anaconda
venv\Scripts\activate.bat                   # Windows command prompt
venv\Scripts\Activate.ps1                   # Windows powershell
"""
# Task 3: Install requirements
"""
# Add the following to requirements.txt in the project directory
google-api-python-client
google-auth-httplib2
google-auth-oauthlib
aiosmtpd

# If you are not using an IDE, install requirements from command line
pip install -r requirements.txt                                   # Windows, Mac or Linux without Anaconda
conda install --name venv-email-pdf --file requirements.txt       # Anaconda
# or if you don't want to use the requirements.txt file
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib aiosmtpd
"""


# Task 4: Create an email message using email.message.EmailMessage
def message_from_str(subject="Creating a plain text email"):
    str_body = f"""\
Greetings from Beginners' Python and Machine Learning.

This email is the result of demonstrating: "{subject}"
It was created by a python bot at {datetime.datetime.now()}.

Email message created using email.message.EmailMessage().
https://docs.python.org/3/library/email.examples.html
https://docs.python.org/3/library/email.message.html
    """
    email_message = EmailMessage()
    email_message.set_content(str_body)
    email_message['Subject'] = subject
    email_message['To'] = EMAIL_TO
    email_message.preamble = "You will not see this preamble in a MIME-aware mail reader.\n"
    return email_message


# print(message_from_str())
# print(my_message_from_str())


# Task 5: Run debugging email server aiosmtpd
# https://aiosmtpd.readthedocs.io/
"""
python -m aiosmtpd -n --listen localhost:8025 --debug
# Stop with ctrl-c
"""


# Task 6: Send a message to the debug server. Try including a non-ascii unicode character
def send_message_via_aiosmtpd(email_message):
    email_message['From'] = "debugger@my_computer.python"
    # Ports 8025 debugging server, 25 SMTP(), 465 SMTP_SSL(), 587 .starttls()
    smtp_port = 8025  # For debugging server
    smtp_host = "127.0.0.1"
    with smtplib.SMTP(smtp_host, smtp_port) as smtp_server:
        smtp_server.set_debuglevel(1)
        smtp_server.send_message(email_message)


# send_message_via_aiosmtpd(message_from_str("Task 6: Test to debugging server"))
# send_message_via_aiosmtpd(message_from_str("Task 6: Test to debugging server 😃"))


# Task 7: Send a message via ISP server.
# Telstra/Bigpond: smtp.telstra.com
# Optus: mail.optusnet.com.au
# TPG: mail.tpg.com.au
def send_message_via_isp(email_message):
    email_message['From'] = "bpaml@pythonator.com"
    with smtplib.SMTP("smtp.telstra.com") as server:
        server.set_debuglevel(1)
        server.send_message(email_message)


# send_message_via_isp(message_from_str("Task 7: Test to ISP server 😃"))


# Task 8: Set up a gmail account for sending email
# 8. https://developers.google.com/gmail/api/quickstart/python
# 8a. Turn on Gmail API
# 8a1. Configure your OAuth client : Desktop app or Web server
# 8a2. Save file credentials.json in project directory
# 8b. Install Google Client Library using pip install or requirements.txt
# 8c. Create function like quickstart.py and add scope gmail.send and remove labels demo
# 8d. Call function although may not work with Firefox as default browser on Mac. Try Chrome
def gmail_service():
    """Gmail API to get the Gmail service.

    If token.pickle doesn't exist then the user's browser will open for them to authenticate
    before service is able to send emails.

    :returns: Authorized Gmail API service instance.
    """
    # if you change scopes then you will need to delete token.pickle and get another one
    scopes = ['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send']

    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build('gmail', 'v1', credentials=credentials)


# print(gmail_service())


# Task 9: Send email via gmail
# https://developers.google.com/gmail/api/guides/sending#python  (sample code is Python 2 not Python 3)
def send_message_via_gmail(email_message: EmailMessage):
    """Send an email message via Gmail."""
    email_message['From'] = 'pythonatordev@gmail.com'
    # user_id: User's email address. The special value "me" can be used to indicate the authenticated user.
    # gmail_body: {"raw": base64 encoded message as a Python 3 str}
    # for other ways of constructing a gmail_body see help(gmail_service().users().messages().send)
    gmail_body = {"raw": base64.urlsafe_b64encode(email_message.as_bytes()).decode(encoding='utf-8')}
    gmail_response = gmail_service().users().messages().send(userId="me", body=gmail_body).execute()
    print("Gmail response", gmail_response)


# send_message_via_gmail(message_from_str("Task 9: Send email via gmail"))


# Task 10: Attach image to email
# https://docs.python.org/3/library/email.examples.html
def message_with_image_attachment():
    email_message = message_from_str("Task 10: Attaching a JPG image to an email")
    # Place image in same directory as this Python script and put name in next line
    with open(IMAGE_FILE, 'rb') as fp:
        img_data = fp.read()
    # img_data is a bytes object
    # MIME type will be image/jpg which comes from maintype/subtype
    # imghdr determines type of image by looking at the first few bytes of the image
    # filename is optional. It provides a default name should the recipient save the attachment
    subtype = imghdr.what(None, img_data)
    email_message.add_attachment(img_data, maintype='image', subtype=subtype, filename=f'image.{subtype}')
    return email_message


# send_message_via_aiosmtpd(message_with_image_attachment())
# send_message_via_isp(message_with_image_attachment())
# send_message_via_gmail(message_with_image_attachment())


# Task 11: Send an html email
def html_table_of_unicode_digits():
    dict_for_group = collections.defaultdict(dict)
    for i in range(7258):
        c = chr(i)
        if unicodedata.category(c) == "Nd":
            unicode_name = unicodedata.name(c)
            try:
                idx = unicode_name.index("DIGIT") + 5
            except ValueError:
                print(f"ValueError with i={i} c={c} unicode_name={unicode_name}. Doesn't contain 'DIGIT'")
            else:
                group_name = unicode_name[:idx]
                group_dict = dict_for_group[group_name]
                group_dict[int(c)] = c
    html = "<table>\n"
    for group, group_dict in dict_for_group.items():
        html += f"<tr><td>{group}</td>"
        for k in range(10):
            html += f"<td class='digit'>{group_dict.get(k, ' ')}</td>"
        html += "</tr>\n"
    html += "</table>"
    return html


def message_using_html():
    style = "<style type='text/css'>.digit {width: 30px; border: 1px solid #ccffcc; text-align: center;}</style>"
    html = f"<html><head>{style}</head><body>\n"
    html += "<p>Our <em>favourite</em> numbers.</p>"
    # html += html_table_of_unicode_digits()
    html += "</body></html>"
    message = message_from_str("Task 11: Adding html to email")
    message.add_alternative(html, subtype='html')
    return message


# send_message_via_gmail(message_using_html())


# Task 12: Embed an image in html message
def message_using_html_with_embedded_image():
    style = """<style type='text/css'>
    .digit {width: 30px; border: 1px solid #ccffcc; text-align: center;}
    table {border-collapse: collapse;}
    </style>"""
    html = f"<html><head>{style}</head><body>\n"
    html += "<p>Our <em>esteemed</em> team.</p>"
    cid_image = make_msgid()
    html += f'<img src="cid:{cid_image[1:-1]}">'
    html += "<p>My <strong>favourite</strong> numbers.</p>"
    html += html_table_of_unicode_digits()
    html += "</body></html>"
    message = message_from_str("Task 12: Adding html to email")
    message.add_alternative(html, subtype='html')
    with open(IMAGE_FILE, "rb") as img:
        img_data = img.read()
    message.get_payload()[1].add_related(img_data, maintype='image', subtype=imghdr.what(None, img_data), cid=cid_image)
    return message


# send_message_via_gmail(message_using_html_with_embedded_image())

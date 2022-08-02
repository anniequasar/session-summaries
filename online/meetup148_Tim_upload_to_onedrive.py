"""MeetUp 148 - Beginners' Python and Machine Learning - 12 July 2022 - Upload to onedrive using MS Graph - delegation

Youtube: https://youtu.be/Ijj_a09rwio
Github:  https://github.com/timcu/session-summaries/raw/master/online/meetup148_tim_upload_to_onedrive_using_graph_delegation.py
Meetup:  https://www.meetup.com/beginners-python-machine-learning/events/286892519/

Learning objectives
 - REST API
 - Authentication
 - Microsoft Graph and OneDrive libraries
 - Programmatic control of OneDrive, Sharepoint, Microsoft Email

@author D Tim Cummings

Requires Python 3.8 or later and Jetbrains Pycharm Community Edition (free) installed on your computer
https://www.python.org/downloads/
https://www.jetbrains.com/pycharm/download/

Task 1: Manually perform the following tasks using graph-explorer

https://developer.microsoft.com/en-us/graph/graph-explorer

Demonstrate Getting Started GET my profile
Demonstrate Getting Started GET all the items in my drive
Demonstrate OneDrive POST create a folder (requires login)
Demonstrate modifying create a folder to create a folder called bpaml148

Task 2: Use API menu in graph-explorer to look up API for creating a folder in OneDrive
https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
POST https://graph.microsoft.com/v1.0/me/drive/root/children
Log in to graph-explorer to do this. Try changing folder name to 'bpaml from graph-explorer'

Task 3: Create a python program which implements Graph API calls
Use API menu in graph-explorer to go to quick start and "build and run the sample"
Open in Pycharm
Create virtual environment
Set content root to graphtutorial (because requirements.txt is in that subfolder)
Add reportlab to requirements.txt as we will use it later
Install requirements
Run code, try a couple of API calls and exit

Task 4: Analyse program flow using Pycharm debugger
Set breakpoint in main.py to last line
Debug code and step through to see where it goes

Task 5: Add this file into folder graphtutorial, so you can run solutions to list files in root

Add to graph.py
import meetup148_tim_upload_to_onedrive_using_graph_delegated as bpaml148

Add to graph.py, function make_graph_call()
    bpaml148.list_drive_items(this.user_client)

Task 6: Create folder in onedrive root
    add scope files.readwrite to config.cfg
    bpaml148.create_folder_in_onedrive(this.user_client)

Task 7: Find id of Documents folder
    documents_id = bpaml148.fetch_documents_id(this.user_client)

Task 8: Push a file to Documents folder on onedrive
    bpaml148.put_pdf_in_documents(this.user_client)

"""
import datetime
import io
import json
import logging
import pprint

logger = logging.getLogger(__name__)


def list_drive_items(user_client):
    # https://docs.microsoft.com/en-us/graph/api/driveitem-list-children?view=graph-rest-1.0&tabs=http
    request_url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'
    response = user_client.get(request_url)
    for item in response.json()['value']:
        logger.warning(f"{item['id']=} {item['name']=}")
    return response


def create_folder_in_onedrive(user_client):
    # https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
    import pprint
    request_url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'
    request_body = {
        "name": "bpaml148 in root",
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }
    response = user_client.post(request_url,
                                data=json.dumps(request_body),
                                headers={'Content-Type': 'application/json'})
    logger.warning(f"response=\n{pprint.pformat(response.json())}")
    return response


documents_id = None


def fetch_documents_id(user_client):
    # https://docs.microsoft.com/en-us/graph/api/driveitem-list-children?view=graph-rest-1.0&tabs=http
    global documents_id
    if documents_id is None:
        request_url = 'https://graph.microsoft.com/v1.0/me/drive/root/children'
        response = user_client.get(request_url)
        for item in response.json()['value']:
            logger.warning(f"{item['id']=} {item['name']=}")
            if item['name'] == 'Documents':
                documents_id = item['id']
                break
    logger.warning(f"{documents_id=}")
    return documents_id


def create_folder_in_documents(user_client):
    # https://docs.microsoft.com/en-us/graph/api/driveitem-post-children?view=graph-rest-1.0&tabs=http
    request_url = f'https://graph.microsoft.com/v1.0/me/drive/items/{fetch_documents_id(user_client)}/children'
    request_body = {
        "name": "bpaml148 in Documents",
        "folder": {},
        "@microsoft.graph.conflictBehavior": "rename"
    }
    response = user_client.post(request_url, data=json.dumps(request_body),
                                headers={'Content-Type': 'application/json'})
    logger.warning(f"response=\n{pprint.pformat(response.json())}")
    return response


def put_pdf_in_documents(user_client):
    # https://docs.microsoft.com/en-us/graph/api/driveitem-put-content?view=graph-rest-1.0&tabs=http
    # see bpaml meetup066 for how to create a pdf
    # https://github.com/timcu/session-summaries/blob/master/online/meetup066_tim_pdf.py
    # add `reportlab` to `requirements.txt` or install in virtual environment with `pip install reportlab`
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Preformatted
    from reportlab.lib.styles import getSampleStyleSheet
    with io.BytesIO() as pdf_buffer:
        doc = SimpleDocTemplate(pdf_buffer)
        story = [
            Paragraph(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            Preformatted(r"""
         ____             _                           _
        |  _ \           (_)                         ( )
        | |_) | ___  __ _ _ _ __  _ __   ___ _ __ ___|/
        |  _ < / _ \/ _` | | '_ \| '_ \ / _ \ '__/ __|
        | |_) |  __/ (_| | | | | | | | |  __/ |  \__ \
        |____/ \___|\__, |_|_| |_|_| |_|\___|_|  |___/
                     __/ |
                    |___/

         _____       _   _
        |  __ \     | | | |
        | |__) |   _| |_| |__   ___  _ __
        |  ___/ | | | __| '_ \ / _ \| '_ \
        | |   | |_| | |_| | | | (_) | | | |
        |_|    \__, |\__|_| |_|\___/|_| |_|
                __/ |
               |___/
        """, getSampleStyleSheet()["Code"])]
        doc.build(story)
        bytes_pdf = pdf_buffer.getvalue()

    filename = "pdf_banner_bpaml148.pdf"
    request_url = f'https://graph.microsoft.com/v1.0/me/drive/items/{fetch_documents_id(user_client)}:/{filename}:/content'

    response = user_client.put(request_url, data=bytes_pdf,
                               headers={'Content-Type': 'application/pdf'})
    logger.warning(f"response=\n{pprint.pformat(response.json())}")
    return response


from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from django.contrib import messages
import time
import os
from configparser import ConfigParser
from django.conf import settings

SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

class GoogleDrive:
    def __init__(self): 
        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        self.service = build('drive', 'v3', credentials=creds)


    def list_files(self,page_token = None):
        while True:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(q=f"'{self.owner}' in owner",fields='nextPageToken, items(id, title)',pageToken=page_token).execute()
            for item in files['items']:
                yield item
            page_token = files.get('nextPageToken')
            if not page_token:
                break

    def get_file_metadata(self,service, file_id):
        page_token = None
        file = service.files().get(fileId=file_id).execute()


    def print_files_in_folder(self,service, folder_id):
        page_token = None
        while True:
            try:
                param = {}
                if page_token:
                    param['pageToken'] = page_token
                children = service.children().list(folderId=folder_id, **param).execute()

                for child in children.get('items', []):
                    yield child
                page_token = children.get('nextPageToken')
                if not page_token:
                    break
            except Exception as e:
                print(e)
                break
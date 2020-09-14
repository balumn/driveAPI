from oauth2client.client import OAuth2WebServerFlow
from oauth2client.file import Storage
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow
from django.contrib import messages
import time
import os
from configparser import ConfigParser


class GoogleDrive:
    def auth(self): 
        config = ConfigParser()
        config.read('.env')
        OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
        REDIRECT_URI ='urn:ietf:wg:oauth:2.0:oob'
        OUT_PATH = os.path.join(os.path.dirname(__file__), 'out')
        CREDS_FILE = os.path.join(os.path.dirname(__file__), 'credentials.json')

        if not path.exists(OUT_PATH):
            os.makedirs(OUT_PATH)

        storage = Storage(CREDS_FILE)
        credentials = storage.get()
        if credentials is None:
            messages.error(request, "Please enable Goolge Drive APIs")
            messages.error(request, "And download your credentials.json onto this Project Root Directory")
            time.sleep(3)
            return None

        http = httplib2.Http()
        http = credentials.authorize(http)
        d_s = build('drive', 'v2', http=http)
        return d_s


    def list_files(self,service):
        page_token = None
        while True:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            files = service.files().list(**param).execute()
            for item in files['items']:
                yield item
            page_token = files.get('nextPageToken')
            if not page_token:
                break

    def print_file_metadata(self,service, file_id):
        page_token = None
        while True:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            file = service.files().get(fileId=file_id).execute()
            return file

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
            except errors.HttpError, error:
                break
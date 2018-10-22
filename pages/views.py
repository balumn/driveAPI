# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import render_to_response
import datetime
import os,json
import httplib2
import os.path
from os import path
import webbrowser
from oauth2client.file import Storage
from googleapiclient.discovery import build
from oauth2client.client import OAuth2WebServerFlow


# from .forms import PostForm

# Create your views here.
from django.http import HttpResponse


def homePageView(request):
    return HttpResponse('Hello, World!!')

    # integrating

def auth(): 
    # client IDs
    CLIENT_ID='500291203402-7vp5mndmfikul17fojcpk152f61vdeup.apps.googleusercontent.com'
    CLIENT_SECRET='DSalAwqk8sp9u_yH--LLrxS1'
    OAUTH_SCOPE = 'https://www.googleapis.com/auth/drive'
    REDIRECT_URI ='urn:ietf:wg:oauth:2.0:oob'
    OUT_PATH = os.path.join(os.path.dirname(__file__), 'out')
    CREDS_FILE = os.path.join(os.path.dirname(__file__), 'credentials_gow.json')

    if not path.exists(OUT_PATH):
        os.makedirs(OUT_PATH)

    storage = Storage(CREDS_FILE)
    credentials = storage.get()
    if credentials is None:
        # Run through the OAuth flow and retrieve credentials
        flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, OAUTH_SCOPE, REDIRECT_URI)
        authorize_url = flow.step1_get_authorize_url()
        pastedCode='4/ZABdayNUfm_EN0ehvQed6m3bGdUXVqX2y7DEsTHAI9j3H-9XGHcG92E'
        code = pastedCode
        credentials = flow.step2_exchange(code)
        storage.put(credentials)

    http = httplib2.Http()
    http = credentials.authorize(http)
    d_s = build('drive', 'v2', http=http)
    return d_s

def list_files(service):
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

def print_file_metadata(service, file_id):
    page_token = None
    while True:
        param = {}
        if page_token:
            param['pageToken'] = page_token
        file = service.files().get(fileId=file_id).execute()
        return file

def print_files_in_folder(service, folder_id):
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


def homme(request):
    drive_service = auth()  
    # exporting json
    xx=[]
    for x in list_files(drive_service):
        if x.get('title') and x.get('alternateLink'):
            fid="https://drive.google.com/uc?export=download&id="+x['id']
            xx.append({'title':x['title'],
            'altLink':x['alternateLink'],
            'dL':fid,
            'iLink':x['iconLink'],
            'ctype':x['mimeType'],
            'id':x['id']
            })
    # dumping to JSON --for Ember if needed.
    with open("data_file.json", "w") as fList: 
        json.dump(xx, fList)
    fList.close()
    # reading from JSON file -- Expermental feature
    with open('data_file.json') as json_file:
        dataP = json.load(json_file)
    json_file.close()
    
    return render_to_response("home.html",{"fList" : dataP})

def about(request,folder=None):
    fid = request.GET.get('folder')
    fid = str(fid)
    
    drive_service = auth()
    # try
    xx=[]
    yy=[]
    metaData=[]
    for x in print_files_in_folder(drive_service,fid):
        ffid="https://drive.google.com/uc?export=download&id="+x['id']
        xx.append(x)
        yy.append(x['id'])
    # write contents to JSON file
    with open("data_files_in_folder.json","w") as fList: 
        json.dump(yy, fList)
    
    for f in yy:
        meta=print_file_metadata(drive_service,f)
        fid="https://drive.google.com/uc?export=download&id="+meta['id']
        metaData.append({'title':meta['title'],
            'altLink':meta['alternateLink'],
            'dL':fid,
            'iLink':meta['iconLink'],
            'ctype':meta['mimeType'],
            'id':meta['id']})
    
    with open("data_full_in_folder.json","w") as fList: 
        json.dump(metaData, fList)
    fList.close()
    # moment of truth
    with open("data_full_in_folder.json","r") as ffList:
        dataF = json.load(ffList)
    ffList.close()
    return render(request, "about.html",{'app':dataF})

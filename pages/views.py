# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

import datetime
import os,json
# import dropbox
import unicodedata

@login_required(login_url='/login')
def homePageView(request):
    print("hello")
    return render(request,"admin_app/dashboard.html",{})

@login_required(login_url='/login')
def googleDrive(request):
    print("google files")
    return render(request,"admin_app/googleDrive.html",{})

@login_required(login_url='/login')
def dropBox(request):
    print("google files")
    return render(request,"admin_app/dropBox.html",{})
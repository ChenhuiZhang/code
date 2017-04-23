from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
import os

def hello(request):
    return HttpResponse("Hello world")

def time(request):
    now = datetime.datetime.now()
    return render_to_response('time.html', {'current_date': now})

def search(request):
    #item_list = ["192.168.0.1", "123.34.21.3"]
    item_list = os.popen('ls').readlines()
    return render_to_response('time.html', locals())
    

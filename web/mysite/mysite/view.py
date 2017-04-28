from django.http import HttpResponse
from django.shortcuts import render_to_response
import datetime
from pexpect import pxssh
import os

def hello(request):
    return HttpResponse("Hello world")

def time(request):
    now = datetime.datetime.now()
    return render_to_response('time.html', {'current_date': now})

def search(request):
    #item_list = ["192.168.0.1", "123.34.21.3"]
    item_list = os.popen('xcam-scan | grep "192.168.77."').readlines()
    for i, item in enumerate(item_list):
        print item.split();
        item_list[i] = [item.split()[0], item.split()[1] + item.split()[2]];

    return render_to_response('time.html', locals())
    
def device(request):
    print request.GET['ip']
    s = pxssh.pxssh()
    s.login(request.GET['ip'], 'root', 'pass')
    s.sendline('bootblocktool -l')   # run a command
    s.prompt()             # match the prompt
    print(s.before)        # print everything before the prompt.
    rsp = s.before.split('\r')
    bb_list = [];
    for i, item in enumerate(rsp):
        #print item.split('=');
        #item = item.replace("\n", "");
        item.strip()
        if '=' in item:
            bb_list.append([item.split('=')[0], item.split('=')[1]]);

    print bb_list;
    return render_to_response('device.html', locals())

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
from pexpect import pxssh
import os
import re
import ast

def search(request):
    item_list = os.popen('xcam-scan | grep "192.168.77."').readlines()
    for i, item in enumerate(item_list):
        print item.split();
        item_list[i] = [item.split()[0],                                                # ip
                re.search('AXIS [AQPM][0-9]{4}(?:-[A-Z]{1,3})?[^-]*', item).group(),    # Product name
                re.search('[0-9A-F]{12}', item).group()];                               # Mac

    return render_to_response('search.html', locals())
    
def device(request):
    if request.method == 'GET':
        print "Geeeeeeeeeeeeeeeeeet"
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
        return render(request, 'device.html', locals())
    else:
        print "Poooooooooooooooooost"
        new = request.POST.get("new_bb");
        #assert False

        print "sssssssss %s" % new
        pattern = re.compile('({.+?})');
        list = pattern.findall(new)

        bb_list = [];
        for i, item in enumerate(list):
            print item;
            ditem = ast.literal_eval(item);

            ditem['name'] = ditem['name'].strip('\n');
            print ditem['name'];
            print ditem['value'];

            bb_list.append(ditem);
            
        print bb_list;

        return render_to_response('time.html')


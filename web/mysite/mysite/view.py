from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.shortcuts import render
import paramiko
import os
import time
import re
import ast
import requests
from requests.auth import HTTPDigestAuth


def search(request):
    item_list = os.popen('xcam-scan | grep "192.168.77."').readlines()
    for i, item in enumerate(item_list):
        print item.split();
        item_list[i] = [item.split()[0],                                                # ip
                re.search('AXIS [AFMPQ][0-9]{2,4}(?:-[A-Z]{1,3})?[^-]*', item).group(), # Product name
                re.search('[0-9A-F]{12}', item).group()];                               # Mac

    return render_to_response('search.html', locals())
    
def device(request):
    if request.method == 'GET':
        print "Geeeeeeeeeeeeeeeeeet"
        print request.GET['ip']
        bb_list = [];


        url = 'http://' + request.GET['ip'] + '/axis-cgi/admin/param.cgi?action=update&Network.SSH.Enabled=yes'
        r = requests.get(url, auth=HTTPDigestAuth('root', 'pass'))
        print r.status_code

        time.sleep(5)

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(request.GET['ip'], 22, "root", "pass")
        stdin, stdout, stderr = ssh.exec_command("bootblocktool -l")
        rsp_list = stdout.readlines()
        ssh.close()

        for i, item in enumerate(rsp_list):
            print item.split('=');
            item.strip();
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
        command = 'bootblocktool -w ';
        for i, item in enumerate(list):
            print item;
            ditem = ast.literal_eval(item);

            ditem['name'] = ditem['name'].strip('\n');
            ditem['value'] = ditem['value'].strip('\n');
            print ditem['name'];
            print ditem['value'];

            command += '%s="%s":' % (ditem['name'], ditem['value'])

            bb_list.append(ditem);
            
        print bb_list;
        print command;

        print command[:-1];

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        print request.GET['ip'];
        ssh.connect(request.GET['ip'], 22, "root", "pass")
        stdin, stdout, stderr = ssh.exec_command("ubirmvol /dev/ubi1 -n 15")
        ret = stdout.readlines()
        print ret;
        stdin, stdout, stderr = ssh.exec_command(command[:-1])
        ret = stdout.readlines()
        print ret;
        ssh.close()

        url = 'http://' + request.GET['ip'] + '/axis-cgi/hardfactorydefault.cgi'
        print url
        r = requests.get(url, auth=HTTPDigestAuth('root', 'pass'))
        print r.status_code

        return render_to_response('search.html')


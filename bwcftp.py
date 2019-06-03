#!/home/chenhuiz/.pyenv/shims/python3.6

from ftplib import FTP
import re
import os

mkvInfoList = []
mkvLinkList = []

def xxxx(dirinfo):
    if re.search("mkv$", dirinfo):
        print(dirinfo)
        mkvInfoList.append(dirinfo)


def yyyy():
    print("Retrive below record files from:")
    for f in mkvInfoList:
        print("1) ", f)
    num = input("Choose the one you want to download: ")
    print(num)

ftp = FTP("fe80::aecc:8eff:fed2:497f%eth1")
ftp.login(user="root", passwd="pass")
ftp.cwd('/var/spool/storage/SD_DISK/current/recordings')
ftp.retrlines('LIST')
#print(ftp.dir())
print(ftp.nlst())

res = [x for x in ftp.nlst() if re.search("^[0-9]{8}$", x)] 
ftp.cwd(res[0])
res = [x for x in ftp.nlst() if re.search("^[0-9]{2}$", x)] 
res.sort(reverse=True)
ftp.cwd(res[0])
res = [x for x in ftp.nlst() if re.search("^[0-9]{8}_[0-9]{6}_.*", x)] 
res.sort(reverse=True)
print(res[0], res[1])

for rec in res:
    res = [x for x in ftp.nlst(rec) if re.search("^[0-9]{8}_[0-9]{2}$", x)] 
    ftp.dir(f'{rec}/{res[0]}', xxxx)

    mkvs = [x for x in ftp.nlst(f'{rec}/{res[0]}') if re.search("mkv$", x)] 
    mkvLinkList.append(f'{rec}/{res[0]}/{mkvs[0]}')

print(mkvInfoList)
print(mkvLinkList)


print("Retrive below record files from:")
for f in mkvInfoList:
    print("1) ", f)
val = input("Choose the one you want to download: ")
print(val)

try:
    num = int(val)
except ValueError:
    print("That's not an int!")

path = mkvLinkList[num-1]

print(path)
ftp.retrbinary(f'RETR {path}', open(os.path.basename(path), 'wb').write)

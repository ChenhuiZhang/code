#!/home/chenhuiz/.pyenv/shims/python3.6

from ftplib import FTP
import re
import os
import sys

MKV_INFO_LIST = []
MKV_LINK_LIST = []

def xxxx(dirinfo):
    if re.search("mkv$", dirinfo):
        MKV_INFO_LIST.append(dirinfo)

def records_fetch(ftp):

    res = [x for x in ftp.nlst() if re.search("^[0-9]{8}$", x)]
    ftp.cwd(res[0])
    res = [x for x in ftp.nlst() if re.search("^[0-9]{2}$", x)]
    res.sort(reverse=True)
    ftp.cwd(res[0])
    res = [x for x in ftp.nlst() if re.search("^[0-9]{8}_[0-9]{6}_.*", x)]
    res.sort(reverse=True)

    for rec in res:
        res = [x for x in ftp.nlst(rec) if re.search("^[0-9]{8}_[0-9]{2}$", x)]
        ftp.dir(f'{rec}/{res[0]}', xxxx)

        mkvs = [x for x in ftp.nlst(f'{rec}/{res[0]}') if re.search("mkv$", x)]
        MKV_LINK_LIST.append(f'{rec}/{res[0]}/{mkvs[0]}')

    #print(MKV_INFO_LIST)
    #print(MKV_LINK_LIST)

def main():
    ftp = FTP(sys.argv[1])
    ftp.login(user="root", passwd="pass")
    ftp.cwd('/var/spool/storage/SD_DISK/current/recordings')

    records_fetch(ftp)

    print("Retrive below record files from:", sys.argv[1])
    for line in MKV_INFO_LIST:
        print(MKV_INFO_LIST.index(line), ") ", line)
    val = input("Choose the one you want to download: ")

    try:
        num = int(val)
    except ValueError:
        print("Input not valid!")

    path = MKV_LINK_LIST[num]

    ftp.retrbinary(f'RETR {path}', open(os.path.basename(path), 'wb').write)

    print("Done")

if __name__ == "__main__":
    main()

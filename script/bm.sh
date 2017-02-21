#! /bin/sh -e

bootblocktool -l > /tmp/bootblock.txt
sed -i -e 's/HWID=617.2/HWID=61B.2/g' /tmp/bootblock.txt

ubirmvol /dev/ubi1 -n 15

while read l; do
        bootblocktool -w "$l" > /dev/null
done < /tmp/bootblock.txt

bootblocktool -l

exit 0

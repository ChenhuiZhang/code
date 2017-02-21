#! /bin/sh -e

HOST="192.168.0.90"
BB_LIST="list"
SCRIPT="bootblocktool -l | grep \"SERNO\" > /tmp/bootblock.txt"

sshRun()
{
    sshpass -p pass ssh root@${HOST} "${1}" < /dev/null
}

while getopts "h:c:" arg
do
    case $arg in
	h)
	    $HOST=$OPTARG
	    ;;
	c)
	    $BB_LIST=$OPTARG
	    ;;
	?)
	    echo "unknow"
	    ;;
    esac
done

#sshpass -p pass ssh root@${HOST} ${SCRIPT} < /dev/null
#sshpass -p pass ssh root@${HOST} " < /dev/null

sshRun "bootblocktool -l | grep \"SERNO\" > /tmp/bootblock.txt"
sshRun "ubirmvol /dev/ubi1 -n 15"
			
while read l; do
    echo $l
    sshpass -p pass ssh root@${HOST} "bootblocktool -w "${l}"" < /dev/null > /dev/null
done < ${BB_LIST}

sshpass -p pass ssh root@${HOST} "while read l; do "bootblocktool -w "\${l}"" > /dev/null; done < /tmp/bootblock.txt" < /dev/null > /dev/null


sshpass -p pass ssh root@${HOST} "echo JFFSID=\"SOFT_RESET\" > /etc/release" > /dev/null

#sshpass -p pass ssh root@${HOST} "echo JFFSID=\"SOFT_RESET\" > /etc/release" > /dev/null

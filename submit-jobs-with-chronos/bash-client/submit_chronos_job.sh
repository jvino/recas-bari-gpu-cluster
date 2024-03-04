#!/bin/bash
FILE=$1
USERNAME=$USER
PASSWORD=$PASSWD
HOSTNAME=$RECAS_HOSTNAME
PORT=$CHRONOS_PORT
curl -u $USERNAME:$PASSWORD -L -H 'Content-Type: application/json' -X POST --data-binary "@$FILE" http://$HOSTNAME:$PORT/v1/scheduler/iso8601

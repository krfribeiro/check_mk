#!/bin/sh
# Dummy ACK Notification
# Author : ricardoftribeiro@gmail.com @krfribeiro

if [ "$NOTIFY_WHAT" = HOST ]
then
    lq "COMMAND [$(date +%s)] ACKNOWLEDGE_HOST_PROBLEM;$NOTIFY_HOSTNAME;2;1;1;ASI;Host Problem - Auto Acknowledment"
else
    lq "COMMAND [$(date +%s)] ACKNOWLEDGE_SVC_PROBLEM;$NOTIFY_HOSTNAME;$NOTIFY_SERVICEDESC;2;1;1;ASI;Service Problem - Auto Acknowledment"
fi
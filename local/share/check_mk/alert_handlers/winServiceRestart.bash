#!/bin/bash
# Windows Services Restart

# $ALERT_PARAMETER_1 - Domain Name
# $ALERT_PARAMETER_2 - UserName
# $ALERT_PARAMETER_3 - Password

winService=`echo $ALERT_SERVICEDESC | awk '{print $2}'`
net rpc service start $winService -S $ALERT_HOSTNAME -U $ALERT_PARAMETER_1/$ALERT_PARAMETER_2%$ALERT_PARAMETER_3
#!/bin/sh
# Author : ricardoftribeiro@gmail.com @krfribeiro
echo "<<<bmc_control_m_status>>>"
su - ctmadmin -c 'ag_diag_comm | grep -B4 -A4 "====" | grep -v "Agent processes" | grep -v "====" | tr -s "\n" ' | while read i
do
    my_item=`echo $i | awk -F ":" '{print $1}' | sed -e 's/ /_/g' | awk -F ":" '{print $1}' | sed -e 's/ /_/g' | sed -e 's/__//g' | sed -e 's/_$//g' | sed -e 's/^_//g'`
    my_status=`echo $i | awk -F ":" '{print $2}' | awk -F " " '{print $1}' | sed -e 's/ /_/g'`
    echo "$my_item $my_status"
done
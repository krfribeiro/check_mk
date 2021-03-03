#!/bin/sh
# Author : ricardoftribeiro@gmail.com @krfribeiro
# [root@servername plugins]# /opt/software/sas/config/Lev1/sas.servers status
# SAS servers status:
# SAS Remote Services 1 is UP
echo "<<<sas_rmi_server>>>"
/opt/software/sas/config/Lev1/sas.servers status | tail -n 1
#!/bin/sh
# VMAX CMK Plugin
# Author : ricardoftribeiro@gmail.com @krfribeiro

echo "<<<vmax_ra>>>"
/opt/emc/SYMCLI/bin/symcfg -sid 723 list -ra all | grep -A3 "Ident" | grep -v "Ident" | grep -v "^$" | awk '{print $1" "$10}'
echo "<<<vmax_sa>>>"
/opt/emc/SYMCLI/bin/symcfg -sid 723 list -sa all | tac | sed '/Ident/q' | tac | grep -v "Ident" | grep -v "^$" | awk '{print $1" "$6}'
echo "<<<vmax_envdata>>>"
for a in `/opt/emc/SYMCLI/bin/symcfg -sid 723 list -env_data | grep "Bay Name" | awk '{print $4}'`
do
    /opt/emc/SYMCLI/bin/symcfg -sid 723 list -env_data | sed -n "/$a/,/Bay Name/p" | grep -v "Bay Name" | grep "All" | sed -e "s/^/$a!/g" | sed -e 's/All//g' | \
    sed -e 's/ /_/g' | sed -e 's/:/!/g' | sed -e 's/_//g' | awk -F "!" '{print $1" "$2" "$3}'
done
echo "<<<vmax_pools>>>"
/opt/emc/SYMCLI/bin/symcfg -sid 723 list -pool -thin -tb | sed -n '/Name/,/TBs/p' | grep -v "Name" | grep -v "Total" | grep -v "\----" | grep -v "^$" | grep -v "TBs" | awk '{print $1" "$6}'
#!/bin/bash 
source /root/.bashrc

echo "00: buildup crontab for 'routinely download HFR data from UCSD...'" >> abc.out

crontab /TxTrack/cron/TxTrack
cron -f 

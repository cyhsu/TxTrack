#!/bin/bash 
source /root/.bashrc

echo "01: init -- download.  " >> abc.out

python3 /TxTrack/src/api/hload.py >> /TxTrack/run_init_download_logs.log


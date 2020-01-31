#!/bin/bash 
source /root/.bashrc

./run_cron.sh &
#./run_download_init.sh &

echo "last: run flask." >> abc.out

WORKDIR=/TxTrack
python3 run.py >> flask.out
#export FLASK_APP=$WORKDIR/run.py
#export FLASK_APP=$WORKDIR/src/app.py
#flask run #>> flask.out
#flask run -p 8012 >> flask.out

echo "End: shouldn't see this." >> abc.out


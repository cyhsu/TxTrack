#!/bin/bash

#--- USER INTERFACE
local_port=8012
local_path=$PWD
background=True


#-- Download TxTrack-flask package. 
git clone https://github.com/cyhsu/leaflet.timedimention.trajectory.git

#-- release directory: leaflet.timedimention.trajectory
mv ./leaflet.timedimention.trajectory/* .
rmdir leaflet.timedimention.trajectory

#-- Build my private Docker Image
docker build -t txtrack-flask .

#-- Run Docker Image
if [ "$background" == True ]; then 
	docker run -d -p ${local_port}:8012 --volume=${local_path} txtrack-flask:latest
else
	docker run -p ${local_port}:8012 --volume=${local_path} txtrack-flask:latest
fi


#!/bin/bash

#--- USER INTERFACE
local_port=5000
local_path=$PWD
background=True

tar xvf txtrack-flask.tar

if [ "$background" == True ]; then 
	docker run -d -p ${local_port}:8012 --volume=${local_path} txtrack-flask:latest
else
	docker run -p ${local_port}:8012 --volume=${local_path} txtrack-flask:latest
fi

#!/bin/bash

WORKDIR=$PWD
export FLASK_APP=$WORKDIR/run.py
flask run

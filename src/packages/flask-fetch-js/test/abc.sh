#!/bin/bash

curl --header "Content-Type: application/json" --request POST --data '{"name":"Julian","message":"Posting JSON data to Flask!"}' http://127.0.0.1:5000/json


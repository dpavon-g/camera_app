#!/bin/bash

docker build -t my_app .
firefox --new-window http://127.0.0.1:8080/
docker-compose up 
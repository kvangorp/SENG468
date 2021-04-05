#!/bin/sh
sudo docker-compose -f docker-compose.vm.yml build
sudo docker-compose -f docker-compose.vm.yml up --scale server=10
exec "$@"

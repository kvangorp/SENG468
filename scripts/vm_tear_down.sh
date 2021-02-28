#!/bin/sh
sudo docker-compose -f docker-compose.vm.yml down
exec "$@"

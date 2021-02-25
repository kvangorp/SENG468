#!/bin/sh
sudo docker stop transaction_server
sudo docker rm transaction_server
sudo docker stop mongodb
sudo docker rm mongodb
exec "$@"

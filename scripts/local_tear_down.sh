#!/bin/sh
docker stop transaction_server
docker rm transaction_server
docker stop quote_server
docker rm quote_server
docker stop mongodb
docker rm mongodb
exec "$@"

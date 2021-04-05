#!/bin/sh
docker-compose -f docker-compose.local.yml build
docker-compose -f docker-compose.local.yml up --scale server=10
exec "$@"

#!/bin/sh
docker-compose -f docker-compose.local.yml down
exec "$@"

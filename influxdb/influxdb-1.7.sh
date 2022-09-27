#!/bin/sh
# Quickly launch the InfluxDB 1.7 with pre-configured user and database.

set -eux

docker run --tty --interactive --rm \
    --net host \
    --env INFLUXDB_HTTP_AUTH_ENABLED="true" \
    --env INFLUXDB_HTTP_FLUX_ENABLED="true" \
    --env INFLUXDB_DB="testing" \
    --env INFLUXDB_ADMIN_USER="admin" \
    --env INFLUXDB_ADMIN_PASSWORD="1.8mys3cret" \
    --name influxdb-1.7 \
    influxdb:1.7

#!/bin/sh
# Quickly launch the latest InfluxDB 2.x with pre-configured access

# Quick shortcut to launch the latest influxdb version with some pre-configured
# user, org, and bucket. This will use the user's host network to expose the
# database API and UI over the default port of 8086. On stop, the container
# is deleted.
#
# ## Users
#
# With InfluxDB 2.x, a user is created with a username and password to gain
# access to the web UI only. To access via the API a token is used.
# Additionally, access is restricted to a specific org and bucket.
#
# ## Configuration
#
# Any InfluxDB configuration setting can be specified as an environment
# variable. he variables must be named using the format
# INFLUXD_${SNAKE_CASE_NAME}. The SNAKE_CASE_NAME for an option will be the
# option's name with all dashes (-) replaced by underscores (_), in all caps.
#
# If more complicated, a user could also mount a configuration file via:
#        -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro
#
# ## Initialization Scripts
#
# The image allows for mounting and then running arbitrary scripts to help
# initialize InfluxDB. These scripts need to use the .sh extension and need to
# be mounted in /docker-entrypoint-initdb.d directory. They are executed in
# lexical sort order by name.
#
# ## Docs
#
# See the docs for the full list of configuraiton settings:
# https://docs.influxdata.com/influxdb/latest/reference/config-options/
#
# See entrypoint.sh for more environmental set up options:
# https://github.com/influxdata/influxdata-docker/blob/master/influxdb/
#
# See the official docker image docs for more image usage information:
# https://github.com/docker-library/docs/blob/master/influxdb/README.md#influxdb
#

set -eux

docker run --tty --interactive --rm \
    --net host \
    --env DOCKER_INFLUXDB_INIT_MODE="setup" \
    --env DOCKER_INFLUXDB_INIT_ORG="my-org" \
    --env DOCKER_INFLUXDB_INIT_BUCKET="my-bucket" \
    --env DOCKER_INFLUXDB_INIT_USERNAME="my-user" \
    --env DOCKER_INFLUXDB_INIT_PASSWORD="my-password" \
    --env DOCKER_INFLUXDB_INIT_ADMIN_TOKEN="my-token" \
    --name influxdb-2.x \
    influxdb:latest

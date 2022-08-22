#!/bin/sh
# Quickly launch the InfluxDB 1.8 with pre-configured user and database
#
# Launches InfluxDB 1.8 with an admin user and a testing database. Uses the
# systems's host network to expose the database API over the default port of
# 8086. On stop, the container is deleted. There is no UI for InfluxDB 1.x.
# This also enables the flux query support.
#
# ## Users
#
# With InfluxDB 1.x, users were created with a traditional username and
# password and either had admin, write, or read access. By default, this
# creates an admin user who has access to everything in the database.
#
# There are three additional permisison levels available:
#
#  - user: full privileges to the created database
#       --env INFLUXDB_USER=""
#       --env INFLUXDB_USER_PASSWORD=""
#
#  - write: only write access to the created database
#       --env INFLUXDB_WRITE_USER=""
#       --env INFLUXDB_WRITE_USER_PASSWORD=""
#
#  - read: only read access to the created database
#       --env INFLUXDB_READ_USER=""
#       --env INFLUXDB_READ_USER_PASSWORD=""
#
# ## Configuration
#
# Any InfluxDB configuration setting can be specified as an environment
# variable. The format is INFLUXDB_$SECTION_$NAME. All dashes (-) are replaced
# with underscores (_). If the variable is not in a section, then omit that
# part.
#
# If more complicated, a user could also mount a configuration file via:
#        -v $PWD/influxdb.conf:/etc/influxdb/influxdb.conf:ro
# and then append the configuraiton location to the command:
#       influxdb:1.8 -config /etc/influxdb/influxdb.conf
#
# ## Docs
#
# See the docs for the full list of configuraiton settings:
# https://docs.influxdata.com/influxdb/v1.8/administration/config/
#
# See init-influxdb.sh for more environmental set up options:
# https://github.com/influxdata/influxdata-docker/tree/master/influxdb/1.8
#
# See the official 1.8 docker image docs for more image usage information:
# https://github.com/docker-library/docs/blob/master/influxdb/README.md#using-this-image---influxdb-1x
#

set -eux

docker run --tty --interactive --rm \
    --net host \
    --env INFLUXDB_HTTP_AUTH_ENABLED="true" \
    --env INFLUXDB_HTTP_FLUX_ENABLED="true" \
    --env INFLUXDB_DB="testing" \
    --env INFLUXDB_ADMIN_USER="admin" \
    --env INFLUXDB_ADMIN_PASSWORD="1.8mys3cret" \
    --name influxdb-1.8 \
    influxdb:1.8

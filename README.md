# InfluxDB Client Tools

This is my collection of helper scripts to interact with InfluxDB via the
client libraries.

## Client Libraries

Each language specific folder contains examples using the InfluxDB client
library in that language:

* `go`: [influxdb-client-go](https://github.com/influxdata/influxdb-client-go)
* `java`: [influxdb-client-java](https://github.com/influxdata/influxdb-client-java)
* `python`: [influxdb-client-python](https://github.com/influxdata/influxdb-client-python)

## Helpers

These folders contain some helpful re-useable items when working with the
client libraries:

* `data`: some example data in CSV, JSON, and line protocol formats
* `flux`: pre-written [Flux](https://docs.influxdata.com/flux/v0.x/) scripts
  for easy re-use
* `influxdb`: Scripts to start up a local InfluxDB instance with a known set
  of credentials

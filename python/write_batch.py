#!/usr/bin/env python3
# Demonstrate most basic batch write. While this method is the default, it is
# not the suggested method due to the lack of easy error handling.
from influxdb_client import InfluxDBClient

BUCKET = "my-bucket"
DATA = """
cpu,core=0 temp=25.3 1657729063
cpu,core=0 temp=25.4 1657729078
cpu,core=0 temp=25.2 1657729093
"""

with InfluxDBClient.from_config_file("config.toml") as client:
    with client.write_api() as write_api:
        write_api.write(bucket=BUCKET, record=DATA)

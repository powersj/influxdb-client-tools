#!/usr/bin/env python3
# Demonstrate a basic synchronous write.
from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS

BUCKET = "my-bucket"
DATA = """
cpu,core=0 temp=25.3 1657729063
cpu,core=0 temp=25.4 1657729078
cpu,core=0 temp=25.2 1657729093
"""

try:
    with InfluxDBClient.from_config_file("config.toml") as client:
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            try:
                writer.write(bucket=BUCKET, record=DATA)
            except InfluxDBError as e:
                print(e)
except InfluxDBError as er:
    print(er)

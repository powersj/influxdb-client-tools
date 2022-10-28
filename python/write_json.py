#!/usr/bin/env python3
"""Example to read JSON data and send to InfluxDB."""

from dateutil import parser
import json

from influxdb_client import InfluxDBClient, Point, WriteOptions
from influxdb_client.client.write_api import SYNCHRONOUS

point = Point("weather")
with open("../data/weather.json", "r") as json_file:
    data = json.load(json_file)

    point.tag("station", data["name"])
    point.time(parser.parse(data["updated"]))
    for key, value in data["sensors"].items():
        point.field(key, value)

with InfluxDBClient.from_config_file("config.toml") as client:
    with client.write_api(write_options=SYNCHRONOUS) as writer:
        try:
            writer.write(bucket="my-bucket", record=[point])
        except InfluxDBError as e:
            print(e)

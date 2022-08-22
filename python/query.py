#!/usr/bin/env python3
# Demonstrate a few ways to query data from InfluxDB.
from influxdb_client import InfluxDBClient

BUCKET = "my-bucket"
QUERY = f'from(bucket: "{BUCKET}") |> range(start: -1h)'

with InfluxDBClient.from_config_file("config.toml") as client:
    query_api = client.query_api()

    # Generic query, that can easily be turned inot JSON string or filter out
    # specific columns
    result = query_api.query(QUERY)
    print(result.to_json())
    print(result.to_values(columns=["core", "_time", "_value"]))

    # Demonstrate uisng the CSV specific query function
    csv_result = query_api.query_csv(QUERY)
    print(csv_result.to_values())

    # Demonstrate uisng the Pandas DataFrame specific query function
    data_frame_result = query_api.query_data_frame(QUERY)

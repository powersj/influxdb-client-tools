#!/usr/bin/env python3

from influxdb_client_3 import InfluxDBClient3


client = InfluxDBClient3(
    token="...",
    host="....a.influxdb.io",
    database="...",
)

query = "select * from cpu"
reader = client.query(query=query, language="influxql")
print(reader.to_pandas())

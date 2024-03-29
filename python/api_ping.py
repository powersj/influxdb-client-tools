#!/usr/bin/env python3
"""
API Call method to run ping against the InfluxDB server.
"""
from influxdb_client import InfluxDBClient

client = InfluxDBClient(
    url='http://localhost:8086',
    token="my-token",
    org='my-org',
    timeout=30000,
    debug=True
)
import ipdb
ipdb.set_trace()

client.api_client.call_api('/ping', 'GET', None, None)

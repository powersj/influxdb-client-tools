#!/usr/bin/env python3

import json

from pyarrow.flight import FlightClient, Ticket, FlightCallOptions

token="mytoken"
host="us-east-1-1.aws.cloud2.influxdata.com"
port=443
database="test"
language = "sql"
query = """
SELECT array_to_string(array_agg(instance),',')
FROM (
    SELECT DISTINCT instance
    FROM repro
    WHERE time >= now() - INTERVAL '1 hours'
)
"""

flight_client = FlightClient(f"grpc+tls://{host}:{port}")

opts = {
    "headers": [(b"authorization", f"Bearer {token}".encode('utf-8'))],
    "timeout": 300
}
options = FlightCallOptions(**opts)

ticket_data = {
    "database": database,
    "sql_query": query,
    "query_type": language
}
ticket = Ticket(json.dumps(ticket_data).encode('utf-8'))

flight_reader = flight_client.do_get(ticket, options)
flight_reader.read_all()

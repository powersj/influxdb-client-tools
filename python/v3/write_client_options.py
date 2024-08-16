 #!/usr/bin/env python3
 #

import influxdb_client_3 as InfluxDBClient3
from influxdb_client_3 import flight_client_options
import certifi

fh = open(certifi.where(), "r")
cert = fh.read()
fh.close()

client = InfluxDBClient3.InfluxDBClient3(
     token="",
     host="b0c7cce5-8dbc-428e-98c6-7f996fb96467.a.influxdb.io",
     org="myorg",
     database="mydb",
     flight_client_options=flight_client_options(tls_root_certs=cert))

table = client.query(
     query="SELECT * FROM flight WHERE time > now() - 4h",
     language="influxql")

print(table.to_pandas())

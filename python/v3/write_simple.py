#!/usr/bin/env python

from influxdb_client_3 import write_client_options, WriteOptions, InfluxDBError, InfluxDBClient3, WritePrecision

class BatchingCallback(object):
    def __init__(self):
        self.success_count = 0
        self.error_count = 0

    def success(self, conf, data: str):
        self.success_count += 1
        print(self)

    def error(self, conf, data: str, exception: InfluxDBError):
        self.error_count += 1
        print(self)

    def retry(self, conf, data: str, exception: InfluxDBError):
        print(f"Retryable error occurred for batch: {conf}, data: {data}, retry: {exception}")

    def __str__(self):
        return f"Success: {self.success_count}, Error: {self.error_count}, Total: {self.success_count + self.error_count}"

callback = BatchingCallback()

write_options = write_client_options(
    success_callback=callback.success,
    error_callback=callback.error,
    retry_callback=callback.retry,
    write_options=WriteOptions(batch_size=2)
)

with InfluxDBClient3(
    host="us-east-1-1.aws.cloud2.influxdata.com",
    database="test",
    token="token",
    write_client_options=write_options,
    debug=False,
) as client:
    # Write first data batch
    records_1 = [
        "mem,host=host1 used_percent=23.43234543 1718621150",
        "mem,host=host2 used_percent=23.43234543 1718621150",
        "mem,host=host3 used_percent=23.43234543 1718621150"
    ]
    client.write(records_1, write_precision=WritePrecision.S)

    # Write second data batch
    records_2 = [
        "mem,host=host1 used_percent=23.43234543 1718621155",
        "mem,host=host2 used_percent=23.43234543 1718621155",
        "mem,host=host3 used_percent=23.43234543 1718621155"
    ]
    client.write(records_2, write_precision=WritePrecision.S)

    # Write error batch
    records_3 = ["mem,not_valid=true 1718621155"]
    client.write(records_3, write_precision=WritePrecision.S)

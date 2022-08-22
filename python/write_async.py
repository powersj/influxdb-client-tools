#!/usr/bin/env python3
# Demonstrate a asynchronous write.
import asyncio

from influxdb_client.client.influxdb_client_async import InfluxDBClientAsync

BUCKET = "my-bucket"
DATA = """
cpu,core=0 temp=25.3 1657729063
cpu,core=0 temp=25.4 1657729078
cpu,core=0 temp=25.2 1657729093
"""


async def main():
    async with InfluxDBClientAsync.from_config_file("config.toml") as client:
        write_api = client.write_api()
        successfully = await write_api.write(bucket=BUCKET, record=DATA)
        print(f" > successfully: {successfully}")


if __name__ == "__main__":
    asyncio.run(main())

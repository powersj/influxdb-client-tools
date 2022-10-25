#!/usr/bin/env python3
import time

from influxdb import InfluxDBClient


client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')

results = []
for index in range(10):
    # generate data
    data = []
    for metric in range(0, 1000000):
        unix_ns = time.time_ns()
        data.append(f"bench,iteration={index} metric={metric} {unix_ns}")
    payload = "\n".join(data).encode('utf-8')

    start = time.perf_counter_ns()
    client.request(url='write', method='POST', data=payload, expected_response_code=204)
    #client.write(data, protocol='line')
    end = time.perf_counter_ns()

    exec_time = round((end - start) / 1000000, 3)
    print(exec_time)
    results.append(exec_time)

print("Average of 10 runs:")
print(sum(results) / len(results))

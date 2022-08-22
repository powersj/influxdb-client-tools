#!/usr/bin/env python3
"""
Benchmark InfluxDB v2 Python Client Write API

Write data to InfluxDB v2 and capture the time the client library API takes to
complete a write.

By default, a configuraiton file, `config.toml`, is expected to have the url,
org, and token to use for writting.

The script will generate data or let the user pass in data to use. If the user
passes in data, they must ensure the data consists of unique data! The
generated data will take the format:

`bench,iteration={index} metric={metric} {unix_ns}`

Iteration is the iteration number currently executed, and metric is an
counter for every metric. Finally, the timestamp is unique to each point. This
metric, while not the smallest, consists of the minimum for every field.

All times are reported in milliseconds.
"""
import argparse
import json
import logging
import sys
import time
from os.path import exists

from influxdb_client import InfluxDBClient
from influxdb_client.client.exceptions import InfluxDBError
from influxdb_client.client.write_api import SYNCHRONOUS

LOG = logging.getLogger(__name__)


def pretty_num(number):
    """Formats numbers with commas (e.g. '100000' to '100,000')."""
    return "{:,}".format(number)


def nano_to_milliseconds(timedelta):
    """Converts nanoseconds to milliseconds to 3 decimal places."""
    return round(timedelta / 1000000, 3)


def std_dev(timedelta):
    """Calculate the standard deviation of a list of numbers."""
    n = len(timedelta)
    mean = sum(timedelta) / n
    var = sum((x - mean) ** 2 for x in timedelta) / n
    std_dev = var**0.5
    return std_dev


def read_file(data_file):
    """Read line protocol from a file."""
    with open(data_file, "r") as file:
        data = file.read()

    return data


def generate_data(index, num_metrics):
    """Generates a list of line protocol with unique nanosecond timestamps."""
    data = []
    for metric in range(0, num_metrics):
        unix_ns = time.time_ns()
        data.append(f"bench,iteration={index} metric={metric} {unix_ns}")

    return data


def write_sync(config, bucket, index, metrics):
    """Write to InfluxDBv2 /api/v2/write synchronously."""
    exec_time = 0
    with InfluxDBClient.from_config_file(config) as client:
        with client.write_api(write_options=SYNCHRONOUS) as writer:
            try:
                start = time.perf_counter_ns()
                writer.write(bucket=bucket, record=metrics)
                end = time.perf_counter_ns()

                exec_time = nano_to_milliseconds(end - start)
                LOG.debug(f"{index}: {exec_time}")
            except InfluxDBError as e:
                sys.exit("%s: %s" % (e.status, e.message))

    return exec_time


def setup_logging(debug):
    """Set up logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )


def parse_args():
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(
        description="""Benchmark InfluxDB v2 Python Client Write API""",
    )
    parser.add_argument(
        "--method",
        required=True,
        choices=["sync", "async", "batch"],
        help="method to write against /api/v2/write",
    )
    parser.add_argument(
        "--num-metrics",
        type=int,
        default=100_000,
        help="number of metrics to generate and write per iteration (default: 100_000)",
    )
    parser.add_argument(
        "--num-iterations",
        type=int,
        default=1,
        help="number of iterations to write data (default: 1)",
    )
    parser.add_argument(
        "--bucket",
        default="my-bucket",
        help='bucket to write metrics to (default: "my-bucket")',
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help='configuraiton file with url, org, and token (default: "config.toml")',
    )
    parser.add_argument(
        "--data", help="file with line protocol to send instead of generating data"
    )
    parser.add_argument("--json", action="store_true", help="print result in JSON")
    parser.add_argument(
        "--debug", action="store_true", help="additional logging output"
    )

    return parser.parse_args()


def preflight(args):
    """Check arguments and connectivity to InfluxDB."""
    # pre-flight checks
    if args.num_metrics < 1:
        sys.exit("number of metrics must be greater than zero")
    if args.num_iterations < 1:
        sys.exit("number of iterations must be greater than zero")

    if not exists(args.config):
        sys.exit(f'config file "{args.config}" does not exist')
    if args.data and not exists(args.data):
        sys.exit(f'data file "{args.config}" does not exist')

    with InfluxDBClient.from_config_file(args.config) as client:
        host = client.url
        if not client.ping():
            sys.exit(f'unable to connect to "{host}"')

    return host


def print_results(host, args, result):
    """Pretty print the final results."""
    # 328,109.179 metrics per second to http://localhost:8086
    LOG.info(
        "%s metrics per second to %s"
        % (
            pretty_num(result["metrics/sec"]),
            host,
        )
    )

    if args.num_iterations == 1:
        # 1,000,000 metrics in 40022.766ms
        LOG.info(
            "%s metrics in %sms"
            % (
                pretty_num(result["metrics"]),
                result["timing"]["total"],
            )
        )
    else:
        # 1,000,000 metrics in 10,000 iterations of 100 metrics in 40022.766ms
        LOG.info(
            "%s metrics (%s iterations of %s metrics) in %sms"
            % (
                pretty_num(result["total_metrics"]),
                pretty_num(result["iterations"]),
                pretty_num(result["metrics"]),
                result["timing"]["total"],
            )
        )

        # min/avg/max/stdev = 3.728/4.6/11.987/0.663 ms
        LOG.info(
            "min/avg/max/stdev = %s/%s/%s/%s ms"
            % (
                result["timing"]["min"],
                result["timing"]["avg"],
                result["timing"]["max"],
                result["timing"]["stdev"],
            )
        )


def main():
    """Generate and write data, then calculate and print timing information."""
    args = parse_args()
    host = preflight(args)
    setup_logging(args.debug)

    # generate and write data
    timedeltas = []
    for index in range(0, args.num_iterations):
        if args.data:
            data = read_file(args.data)
            # line protocol spec says to end with '\n', use that to count metrics
            args.num_metrics = data.count("\n")
        else:
            data = generate_data(index, args.num_metrics)

        if args.method == "sync":
            timedeltas.append(write_sync(args.config, args.bucket, index, data))
        elif args.method == "async":
            sys.exit("method 'async' not implimented")
        elif args.method == "batch":
            sys.exit("method 'batch' not implimetned")

    # calculate results and print
    result = {
        "total_metrics": args.num_iterations * args.num_metrics,
        "iterations": args.num_iterations,
        "metrics": args.num_metrics,
        "server": host,
        "metrics/sec": round(
            (args.num_iterations * args.num_metrics) / (sum(timedeltas) / 1000), 3
        ),
        "timing": {
            "total": round(sum(timedeltas), 3),
            "min": min(timedeltas),
            "avg": round(sum(timedeltas) / len(timedeltas), 3),
            "max": max(timedeltas),
            "stdev": round(std_dev(timedeltas), 3),
        },
    }

    if args.json:
        LOG.info(json.dumps(result, indent=4))
    else:
        print_results(host, args, result)


if __name__ == "__main__":
    sys.exit(main())

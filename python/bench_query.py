#!/usr/bin/env python3
"""
Benchmark InfluxDB v2 Python Client Query API

Query data from InfluxDB v2 and capture the time the client library API takes
to collect the data.

By default, a configuraiton file, `config.toml`, is expected to have the url,
org, and token to use for writting.

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

LOG = logging.getLogger(__name__)


def pretty_num(number):
    """Formats numbers with commas (e.g. '100000' to '100,000')."""
    return "{:,}".format(number)


def nano_to_milliseconds(timedelta):
    """Converts timedelta nanoseconds to milliseconds to 3 decimal places."""
    return round(timedelta / 1000000, 3)


def read_file(data_file):
    """Read line protocol from a file."""
    with open(data_file, "r") as file:
        data = file.read()

    return data


def print_results(host, result):
    """Pretty print the final results."""
    # 328,109.179 metrics per second from http://localhost:8086
    LOG.info(
        "%s metrics per second from %s"
        % (
            pretty_num(result["metrics/sec"]),
            host,
        )
    )

    # 1,000,000 metrics in 40022.766ms
    LOG.info(
        "%s metrics in %sms"
        % (
            pretty_num(result["metrics"]),
            result["time"],
        )
    )

def query(config, query, serializer):
    """Write to InfluxDBv2 /api/v2/write synchronously."""
    exec_time = 0
    num_metrics = 0

    with InfluxDBClient.from_config_file(config) as client:
        query_client = client.query_api()
        try:
            if serializer == "none":
                start = time.perf_counter_ns()
                result = query_client.query(query)
                end = time.perf_counter_ns()
                if len(result) > 0:
                    num_metrics = len(result[0].records)
            elif serializer == "json":
                start = time.perf_counter_ns()
                result = query_client.query(query)
                result.to_json()
                end = time.perf_counter_ns()
                if len(result) > 0:
                    num_metrics = len(result[0].records)
            elif serializer == "csv":
                # CSV query function returns an iterator, and as such not all
                # the values untill the user runs to_values(), so that is
                # included in the total time
                start = time.perf_counter_ns()
                result = query_client.query_csv(query).to_values()
                end = time.perf_counter_ns()
                # There are 5 extra rows included in results, these rows
                # include the datatype, group, default, header, and empty line
                if len(result) > 1:
                    num_metrics = len(result) - 5
            elif serializer == "data-frame":
                import warnings
                from influxdb_client.client.warnings import MissingPivotFunction
                warnings.simplefilter("ignore", MissingPivotFunction)

                start = time.perf_counter_ns()
                result = query_client.query_data_frame(query)
                end = time.perf_counter_ns()
                num_metrics = len(result)

            exec_time = nano_to_milliseconds(end - start)
        except InfluxDBError as e:
            sys.exit("%s: %s" % (e.status, e.message))

    return num_metrics, exec_time


def setup_logging(debug):
    """Set up logging."""
    logging.basicConfig(
        stream=sys.stdout,
        format="%(message)s",
        level=logging.DEBUG if debug else logging.INFO,
    )


def preflight(args):
    """Check arguments and connectivity to InfluxDB."""
    # pre-flight checks
    if not exists(args.config):
        sys.exit(f'config file "{args.config}" does not exist')
    if args.query and not exists(args.query):
        sys.exit(f'query file "{args.query}" does not exist')

    with InfluxDBClient.from_config_file(args.config) as client:
        host = client.url
        if not client.ping():
            sys.exit(f'unable to connect to "{host}"')

    return host


def parse_args():
    """Set up command line arguments."""
    parser = argparse.ArgumentParser(
        description="""Benchmark InfluxDB v2 Python Client Query API""",
    )
    parser.add_argument("--query", required=True, help="file with flux query")
    parser.add_argument(
        "--serializer",
        default="none",
        choices=["none", "json", "csv", "data-frame"],
        help="method to serialize data to",
    )
    parser.add_argument(
        "--config",
        default="config.toml",
        help='configuraiton file with url, org, and token (default: "config.toml")',
    )
    parser.add_argument("--json", action="store_true", help="print result in JSON")
    parser.add_argument(
        "--debug", action="store_true", help="additional logging output"
    )

    return parser.parse_args()


def main():
    """Generate and write data, then calculate and print timing information."""
    args = parse_args()
    # TODO: get the cardinality
    # https://docs.influxdata.com/flux/v0.x/stdlib/influxdata/influxdb/cardinality/
    host = preflight(args)
    setup_logging(args.debug)

    queryStr = read_file(args.query)

    # generate and write data
    num_metrics, timedelta = query(args.config, queryStr, args.serializer)

    # calculate results and print
    result = {
        "server": host,
        "serializer": args.serializer,
        "metrics": num_metrics,
        "metrics/sec": round(num_metrics / (timedelta / 1000), 3),
        "time": round(timedelta, 3),
    }

    if args.json:
        LOG.info(json.dumps(result, indent=4))
    else:
        print_results(host, result)


if __name__ == "__main__":
    sys.exit(main())

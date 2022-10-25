import pandas as pd
from influxdb_client import InfluxDBClient, WriteOptions

with InfluxDBClient.from_env_properties() as client:
    for df in pd.read_csv("../data/vix.csv", chunksize=10_000):
        with client.write_api() as write_api:
            try:
                write_api.write(
                    record=df,
                    bucket="my-bucket",
                    data_frame_measurement_name="stocks",
                    data_frame_tag_columns=["symbol"],
                    data_frame_timestamp_column="date",
                )
            except InfluxDBError as e:
                print(e)

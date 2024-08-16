#!/usr/bin/env python

import influxdb_client_3 as InfluxDBClient3
import pandas as pd
import numpy as np

client = InfluxDBClient3.InfluxDBClient3(
    token="token",
    host="us-east-1-1.aws.cloud2.influxdata.com",
    database="test"
)

df = pd.DataFrame({'a': [1, 2, 3], 'b': [4, 5, 6]})

dates = pd.date_range(start='2023-03-01', end='2023-03-29', freq='5min')

df = pd.DataFrame(
    np.random.randn(len(dates), 3),
    index=dates,
    columns=[
        'Column 1',
        'Column 2',
        'Column 3'
    ]
)
df['tagkey'] = 'Hello World'

print(df)

foo = client.write(
    df,
    data_frame_measurement_name='table',
    data_frame_tag_columns=['tagkey']
)

print(foo)

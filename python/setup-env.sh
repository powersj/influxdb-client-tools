#!/bin/bash
set -eu

python3 -m virtualenv venv
./venv/bin/pip install "influxdb-client[extra,ciso,async]"

echo "Virtual enviornment set up complete! Run the following to activate:"
echo "$ source ./venv/bin/activate"

#!/usr/bin/env node

import {readFileSync} from 'fs'

import {InfluxDB, Point, HttpError} from '@influxdata/influxdb-client'
import {url, token, org, bucket} from './env.mjs'

const data = JSON.parse(readFileSync('../data/weather.json', 'utf8'))

const point = new Point('weather')
    .tag('station', data.name)
    .intField('temperature', data.sensors.temperature)
    .intField('dew_point', data.sensors.dew_point)
    .intField('humidity', data.sensors.humidity)
    .intField('wind', data.sensors.wind)
    .stringField('direction', data.sensors.direction)
    .floatField('pressure', data.sensors.pressure)
    .timestamp(new Date(data.updated))

const writeApi = new InfluxDB({url, token}).getWriteApi(org, bucket, 'ns')
writeApi.writePoint(point)

try {
    await writeApi.close()
} catch (e) {
    if (e instanceof HttpError) {
        console.error(e.statusCode)
        console.error(e.statusMessage)
    }
}

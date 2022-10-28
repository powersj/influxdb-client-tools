const url = process.env['INFLUX_URL'] || 'http://localhost:8086'
const token = process.env['INFLUX_TOKEN'] || 'my-token'
const org = process.env['INFLUX_ORG'] || 'my-org'
const bucket = process.env['INFLUX_BUCKET'] || 'my-bucket'

export {url, token, org, bucket}

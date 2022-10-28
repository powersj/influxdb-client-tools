package main

import (
	"encoding/json"
	"os"
	"time"

	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
)

type Weather struct {
	Name      string         `json:"name"`
	Timestamp string         `json:"updated"`
	Location  Location       `json:"location"`
	Sensors   map[string]any `json:"sensors"`
}

type Location struct {
	Lat  string `json:"lat"`
	Lon  string `json:"lon"`
	Elev int    `json:"elev"`
}

type Sensor struct {
	Temperature int     `json:"temperature"`
	DewPoint    int     `json:"dew_point"`
	Humdity     int     `json:"humidity"`
	Wind        int     `json:"wind"`
	Direction   string  `json:"direction"`
	Pressure    float64 `json:"pressure"`
}

func main() {
	bytes, err := os.ReadFile("../../data/weather.json")
	if err != nil {
		panic(err)
	}

	data := Weather{}
	if err := json.Unmarshal(bytes, &data); err != nil {
		panic(err)
	}

	timestamp, err := time.Parse("2006 02 Jan 03:04 PM -0700", data.Timestamp)
	if err != nil {
		panic(err)
	}

	p := influxdb2.NewPoint(
		"weather",
		map[string]string{
			"station": data.Name,
		},
		data.Sensors,
		timestamp,
	)

	client := influxdb2.NewClient("http://localhost:8086/", "my-token")
	writer := client.WriteAPI("my-org", "my-bucket")
	writer.WritePoint(p)
	client.Close()
}

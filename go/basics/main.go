package main

import (
	"context"
	"fmt"
	"time"

	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
)

var (
	URL    = "http://localhost:8086"
	TOKEN  = "my-token"
	ORG    = "my-org"
	BUCKET = "my-bucket"
)

// Demonstrate basic write examples, including a string and NewPoint helper.
func write(client influxdb2.Client) {
	writeAPI := client.WriteAPIBlocking(ORG, BUCKET)

	line := fmt.Sprintf("stat,unit=temperature avg=%f,max=%f", 23.5, 45.0)
	err := writeAPI.WriteRecord(context.Background(), line)
	if err != nil {
		fmt.Println(err)
	}

	p := influxdb2.NewPoint("stat",
		map[string]string{"unit": "temperature"},
		map[string]interface{}{"avg": 24.5, "max": 45.0},
		time.Now(),
	)
	err = writeAPI.WritePoint(context.Background(), p)
	if err != nil {
		fmt.Println(err)
	}

	p = influxdb2.NewPointWithMeasurement("stat").
		AddTag("unit", "temperature").
		AddField("avg", 23.2).
		AddField("max", 45.0).
		SetTime(time.Now())
	err = writeAPI.WritePoint(context.Background(), p)
	if err != nil {
		fmt.Println(err)
	}
}

// Demonstrate basic flux query with streaming the results.
func query(client influxdb2.Client) {
	queryAPI := client.QueryAPI(ORG)

	fluxQuery := `
	from(bucket:"testing")|> range(start: -1h) |> filter(fn: (r) => r._measurement == "stat")
	`
	result, err := queryAPI.Query(context.Background(), fluxQuery)
	if err == nil {
		for result.Next() {
			if result.TableChanged() {
				fmt.Printf("table: %s\n", result.TableMetadata().String())
			}
			fmt.Printf("row: %s\n", result.Record().String())
		}
		if result.Err() != nil {
			fmt.Printf("Query error: %s\n", result.Err().Error())
		}
	}
}

func main() {
	client := influxdb2.NewClient(URL, TOKEN)
	write(client)
	query(client)

	client.Close()
}

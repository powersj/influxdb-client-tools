package main

import (
	"context"
	"crypto/tls"
	"encoding/json"
	"fmt"

	"github.com/apache/arrow/go/v17/arrow/flight"
	"github.com/apache/arrow/go/v17/arrow/ipc"
	"github.com/apache/arrow/go/v17/arrow/memory"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials"
	"google.golang.org/grpc/metadata"
)

var (
	token    = "token"
	host     = "us-east-1-1.aws.cloud2.influxdata.com"
	port     = "443"
	database = "test"
	language = "sql"
	query    = `
SELECT array_to_string(array_agg(instance),',')
FROM (
	SELECT DISTINCT instance
	FROM repro
	WHERE time >= now() - INTERVAL '1 hours'
)`
)

func main() {
	ticketJSON, err := json.Marshal(map[string]interface{}{
		"database":   database,
		"sql_query":  query,
		"query_type": language,
	})
	if err != nil {
		panic(fmt.Errorf("unable to serialize ticket data to JSON: %w", err))
	}
	ticket := &flight.Ticket{Ticket: ticketJSON}

	opts := []grpc.DialOption{
		grpc.WithTransportCredentials(credentials.NewTLS(&tls.Config{})),
	}
	client, err := flight.NewClientWithMiddleware(fmt.Sprintf("%s:%s", host, port), nil, nil, opts...)
	if err != nil {
		panic(fmt.Errorf("unable to create flight client: %w", err))
	}

	ctx := metadata.AppendToOutgoingContext(context.Background(), "authorization", "Bearer "+token)
	stream, err := client.DoGet(ctx, ticket)
	if err != nil {
		panic(fmt.Errorf("failed calling client: %w", err))
	}
	reader, err := flight.NewRecordReader(stream, ipc.WithAllocator(memory.DefaultAllocator))
	if err != nil {
		panic(fmt.Errorf("unable to get flight reader: %w", err))
	}
	defer reader.Release()

	for reader.Next() {
		fmt.Println(reader.Record())
	}
	if reader.Err() != nil {
		panic(fmt.Errorf("unable to read flight data: %w", reader.Err()))
	}

	fmt.Println("Query executed successfully!")
}

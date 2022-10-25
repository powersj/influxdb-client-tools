package example;

import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.Iterator;

import com.influxdb.client.InfluxDBClient;
import com.influxdb.client.InfluxDBClientFactory;
import com.influxdb.client.WriteApiBlocking;
import com.influxdb.client.domain.WritePrecision;

import com.opencsv.bean.CsvToBean;
import com.opencsv.bean.CsvToBeanBuilder;
import com.opencsv.exceptions.CsvValidationException;

public class CSV2InfluxDB {
	private static char[] token = "my-token".toCharArray();
	private static String org = "my-org";
	private static String bucket = "my-bucket";

	public static void main(final String[] args) throws CsvValidationException, FileNotFoundException, IOException {
		InfluxDBClient influxDBClient = InfluxDBClientFactory.create("http://localhost:8086", token, org, bucket);
		WriteApiBlocking writeApi = influxDBClient.getWriteApiBlocking();

		FileReader reader = new FileReader("../../data/vix-small.csv");
		CsvToBean<StockData> csvToBean = new CsvToBeanBuilder(reader)
			.withType(StockData.class)
			.build();

		Iterator<StockData> stockIterator = csvToBean.iterator();
		while (stockIterator.hasNext()) {
			StockData data = stockIterator.next();
			data.setTimestamp();
			writeApi.writeMeasurement(WritePrecision.S, data);
		}

		influxDBClient.close();
	}
}

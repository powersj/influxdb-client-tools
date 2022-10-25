package example;

import java.time.Instant;

import com.influxdb.annotations.Column;
import com.influxdb.annotations.Measurement;

import com.opencsv.bean.CsvBindByName;

@Measurement(name = "stock")
public class StockData {
    @Column(tag = true)
    @CsvBindByName(column = "symbol")
    private String symbol;

    @Column
    @CsvBindByName(column = "open")
    private String open;

    @Column
    @CsvBindByName(column = "high")
    private String high;

    @Column
    @CsvBindByName(column = "low")
    private String low;

    @Column
    @CsvBindByName(column = "close")
    private String close;

    @CsvBindByName(column = "timestamp")
    private String nanoTimestamp;

    @Column(timestamp = true)
    private Instant timestamp;

    // Transform our nanosecond precision timestamp into a second
    // precision timestamp and convert to Instant.
    public void setTimestamp(){
        String shortTimestamp = nanoTimestamp.substring(0, nanoTimestamp.length() - 8);
        timestamp = Instant.ofEpochSecond(Long.parseLong(shortTimestamp));
    }
}

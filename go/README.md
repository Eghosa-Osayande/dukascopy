# 🏦 dukascript (Go)

Download and stream historical price data for a variety of financial instruments (e.g., Forex, Commodities, and Indices) from Dukascopy Bank SA, including support for tick-level and aggregated intervals.

---

## 📦 Installation

```bash
go get github.com/Eghosa-Osayande/dukascript/go/dukascript
```

---

## 🛠️ Usage

### Importing

```go
import (
	"context"
	"time"
	"github.com/Eghosa-Osayande/dukascript/go/dukascript"
)
```

---

## 🧠 Key Concepts

Both `Fetch` and `LiveFetch` share similar parameters:

| Parameter      | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| `Start`        | `time.Time`, required. The start time of the data.                         |
| `End`          | `*time.Time`, optional. If `nil`, fetches data up to "now" or indefinitely.|
| `Instrument`   | e.g., `INSTRUMENT_FX_MAJORS_GBP_USD`.                                      |
| `OfferSide`    | `OFFER_SIDE_BID` or `OFFER_SIDE_ASK`.                                      |
| `MaxRetries`   | Optional. If `0`, disables retries.                                         |
| `Debug`        | Optional. If `true`, prints debug logs.                                     |

### 🖌️ `Fetch()` only:

| Parameter    | Description                  |
|--------------|------------------------------|
| `Interval`   | e.g., `INTERVAL_HOUR_1`      |

### 🔥 `LiveFetch()` only:

| Parameter         | Description                                 |
|-------------------|---------------------------------------------|
| `IntervalValue`   | e.g., `1`                                    |
| `TimeUnit`        | e.g., `TIME_UNIT_HOUR`                      |

---

## 📊 DataFrame Columns

### When interval or time_unit is based on ticks:

```go
Interval: dukascript.INTERVAL_TICK
```

or

```go
IntervalValue: 1
TimeUnit: dukascript.TIME_UNIT_TICK
```

| Column      | Description              |
|-------------|--------------------------|
| `timestamp` | UTC datetime             |
| `bidPrice`  | Bid price                |
| `askPrice`  | Ask price                |
| `bidVolume` | Bid volume               |
| `askVolume` | Ask volume               |

### When interval/time_unit is not tick-based:

e.g., 5-minute OHLC candle data:

```go
IntervalValue: 5
TimeUnit: dukascript.TIME_UNIT_MIN
```

| Column      | Description              |
|-------------|--------------------------|
| `timestamp` | UTC datetime             |
| `open`      | Opening price            |
| `high`      | Highest price            |
| `low`       | Lowest price             |
| `close`     | Closing price            |
| `volume`    | Volume in units          |

---

## 📂 Saving Results

Use `ToCSV()` or `ToJSON()` methods:

```go
file, err := os.Create("data.csv")
df.ToCSV(file)
```

```go
file, err := os.Create("data.json")
df.ToJSON(file)
```

---

## 🚀 Examples

### Example 1: Fetch Historical Data

```go
ctx := context.Background()
start, _ := time.Parse(time.DateOnly, "2025-04-21")
end := start.Add(24 * time.Hour)

df := dukascript.Fetch(ctx, dukascript.FetchArgs{
	Instrument: dukascript.INSTRUMENT_FX_MAJORS_AUD_USD,
	OfferSide:  dukascript.OFFER_SIDE_BID,
	Start:      start,
	End:        &end,
	Interval:   dukascript.INTERVAL_TICK,
})

file, _ := os.Create("out.csv")
defer file.Close()
df.ToCSV(file)
```

### Example 2: Live Fetch with End Time

```go
ctx := context.Background()
start, _ := time.Parse(time.DateOnly, "2025-04-21")
end := start.Add(24 * time.Hour)

dfChan := dukascript.LiveFetch(ctx, dukascript.LiveFetchArgs{
	Instrument:    dukascript.INSTRUMENT_FX_MAJORS_AUD_USD,
	OfferSide:     dukascript.OFFER_SIDE_BID,
	Start:         start,
	End:           &end,
	IntervalValue: 1,
	TimeUnit:      dukascript.TIME_UNIT_HOUR,
})

var df dukascript.Dataframe
for df = range dfChan {
}

file, _ := os.Create("out.json")
defer file.Close()
df.ToJSON(file)
```

### Example 3: Live Fetch Indefinitely (No End Time)

```go
ctx, cancel := context.WithTimeout(context.Background(), time.Second*10)
defer cancel()
start, _ := time.Parse(time.DateOnly, "2025-04-21")

var df dukascript.Dataframe

dfChan := dukascript.LiveFetch(ctx, dukascript.LiveFetchArgs{
	Instrument:    dukascript.INSTRUMENT_FX_MAJORS_AUD_USD,
	OfferSide:     dukascript.OFFER_SIDE_BID,
	Start:         start,
	End:           nil,
	IntervalValue: 1,
	TimeUnit:      dukascript.TIME_UNIT_HOUR,
})

file, _ := os.Create("out2.json")
defer file.Close()
for df = range dfChan {
}
df.ToJSON(file)
```

---

## 📄 License

MIT

---

## 👋 Contributing

Pull requests and suggestions are highly welcome!


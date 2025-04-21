package dukascript

import (
	"context"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"log"
	"math"
	"math/rand"
	"net/http"
	"net/url"
	"os"
	"strings"
	"time"
)

const (
	TIME_UNIT_MONTH = "MONTH"
	TIME_UNIT_WEEK  = "WEEK"
	TIME_UNIT_DAY   = "DAY"
	TIME_UNIT_HOUR  = "HOUR"
	TIME_UNIT_MIN   = "MIN"
	TIME_UNIT_SEC   = "SEC"
	TIME_UNIT_TICK  = "TICK"

	INTERVAL_MONTH_1 = "1" + TIME_UNIT_MONTH
	INTERVAL_WEEK_1  = "1" + TIME_UNIT_WEEK
	INTERVAL_DAY_1   = "1" + TIME_UNIT_DAY
	INTERVAL_HOUR_4  = "4" + TIME_UNIT_HOUR
	INTERVAL_HOUR_1  = "1" + TIME_UNIT_HOUR
	INTERVAL_MIN_30  = "30" + TIME_UNIT_MIN
	INTERVAL_MIN_15  = "15" + TIME_UNIT_MIN
	INTERVAL_MIN_10  = "10" + TIME_UNIT_MIN
	INTERVAL_MIN_5   = "5" + TIME_UNIT_MIN
	INTERVAL_MIN_1   = "1" + TIME_UNIT_MIN
	INTERVAL_SEC_30  = "30" + TIME_UNIT_SEC
	INTERVAL_SEC_10  = "10" + TIME_UNIT_SEC
	INTERVAL_SEC_1   = "1" + TIME_UNIT_SEC
	INTERVAL_TICK    = TIME_UNIT_TICK

	OFFER_SIDE_BID = "B"
	OFFER_SIDE_ASK = "A"
)

var intervalUnits = map[string]string{
	INTERVAL_MONTH_1: TIME_UNIT_MONTH,
	INTERVAL_WEEK_1:  TIME_UNIT_WEEK,
	INTERVAL_DAY_1:   TIME_UNIT_DAY,
	INTERVAL_HOUR_4:  TIME_UNIT_HOUR,
	INTERVAL_HOUR_1:  TIME_UNIT_HOUR,
	INTERVAL_MIN_30:  TIME_UNIT_MIN,
	INTERVAL_MIN_15:  TIME_UNIT_MIN,
	INTERVAL_MIN_10:  TIME_UNIT_MIN,
	INTERVAL_MIN_5:   TIME_UNIT_MIN,
	INTERVAL_MIN_1:   TIME_UNIT_MIN,
	INTERVAL_SEC_30:  TIME_UNIT_SEC,
	INTERVAL_SEC_10:  TIME_UNIT_SEC,
	INTERVAL_SEC_1:   TIME_UNIT_SEC,
	INTERVAL_TICK:    TIME_UNIT_TICK,
}

type loggerKeyType string

var loggerkey = loggerKeyType("logger")

func setCustomLogger(ctx context.Context, debug bool) context.Context {
	var output io.Writer = os.Stdout
	prefix := "DUKASCRIPT: "
	flags := log.Ldate | log.Ltime

	logger := log.New(output, prefix, flags)

	if !debug {
		// TODO
	}

	return context.WithValue(ctx, loggerkey, logger)

}

func getCustomLogger(ctx context.Context) *log.Logger {
	logger, ok := ctx.Value(loggerkey).(*log.Logger)

	if !ok || logger == nil {
		return log.Default()
	}

	return logger
}

func resampleToNearest(timestamp time.Time, timeUnit string, intervalValue int) (time.Time, error) {
	switch timeUnit {
	case TIME_UNIT_SEC:
		sub := timestamp.Second() % intervalValue
		return timestamp.
			Add(-time.Duration(sub) * time.Second).
			Add(-time.Duration(timestamp.Nanosecond())), nil

	case TIME_UNIT_MIN:
		sub := timestamp.Minute() % intervalValue
		return timestamp.
			Add(-time.Duration(timestamp.Second()) * time.Second).
			Add(-time.Duration(timestamp.Nanosecond())).
			Add(-time.Duration(sub) * time.Minute), nil

	case TIME_UNIT_HOUR:
		sub := timestamp.Hour() % intervalValue
		return timestamp.
			Add(-time.Duration(timestamp.Minute()) * time.Minute).
			Add(-time.Duration(timestamp.Second()) * time.Second).
			Add(-time.Duration(timestamp.Nanosecond())).
			Add(-time.Duration(sub) * time.Hour), nil

	case TIME_UNIT_DAY:
		sub := (timestamp.Day() - 1) % intervalValue
		return time.Date(
			timestamp.Year(), timestamp.Month(), timestamp.Day()-sub,
			0, 0, 0, 0, timestamp.Location(),
		), nil

	case TIME_UNIT_WEEK:
		weekday := int(timestamp.Weekday())
		sub := (weekday + 1) % (intervalValue * 7)
		return time.Date(
			timestamp.Year(), timestamp.Month(), timestamp.Day()-sub,
			0, 0, 0, 0, timestamp.Location(),
		), nil

	case TIME_UNIT_MONTH:
		month := ((int(timestamp.Month())-1)/intervalValue)*intervalValue + 1
		return time.Date(
			timestamp.Year(), time.Month(month), 1,
			0, 0, 0, 0, timestamp.Location(),
		), nil

	case TIME_UNIT_TICK:
		return timestamp, nil

	default:
		return time.Time{}, fmt.Errorf("resampling not implemented for %s", timeUnit)
	}
}

func getColumnsForTimeUnit(timeUnit string) []string {

	ohlc_df := []string{"timestamp", "open", "high", "low", "close", "volume"}
	tick_df := []string{"timestamp", "bidPrice", "askPrice", "bidVolume", "askVolume"}

	cols := map[string][]string{
		TIME_UNIT_WEEK:  ohlc_df,
		TIME_UNIT_DAY:   ohlc_df,
		TIME_UNIT_HOUR:  ohlc_df,
		TIME_UNIT_MIN:   ohlc_df,
		TIME_UNIT_MONTH: ohlc_df,
		TIME_UNIT_SEC:   ohlc_df,
		TIME_UNIT_TICK:  tick_df,
	}[timeUnit]

	return cols
}

func fetch(
	ctx context.Context,
	instrument string,
	interval string,
	offerSide string,
	lastUpdate int64,
	limit int,
) ([][]any, error) {

	// logger := getCustomLogger(ctx)

	characters := "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
	var builder strings.Builder
	for i := 0; i < 9; i++ {
		builder.WriteByte(characters[rand.Intn(len(characters))])
	}
	jsonp := "_callbacks____" + builder.String()

	queryParams := url.Values{
		"path":           {"chart/json3"},
		"splits":         {"true"},
		"stocks":         {"true"},
		"time_direction": {"N"},
		"jsonp":          {jsonp},
		"last_update":    {fmt.Sprintf("%d", lastUpdate)},
		"offer_side":     {offerSide},
		"instrument":     {instrument},
		"interval":       {interval},
	}
	if limit > 0 {
		queryParams.Set("limit", fmt.Sprintf("%d", limit))
	}

	headers := map[string]string{
		"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36 Edg/135.0.0.0",
		"Host":       "freeserv.dukascopy.com",
		"Referer":    "https://freeserv.dukascopy.com/2.0/?path=chart/index&showUI=true&showTabs=true&showParameterToolbar=true&showOfferSide=true&allowInstrumentChange=true&allowPeriodChange=true&allowOfferSideChange=true&showAdditionalToolbar=true&showExportImportWorkspace=true&allowSocialSharing=true&showUndoRedoButtons=true&showDetachButton=true&presentationType=candle&axisX=true&axisY=true&legend=true&timeline=true&showDateSeparators=true&showZoom=true&showScrollButtons=true&showAutoShiftButton=true&crosshair=true&borders=false&freeMode=false&theme=Pastelle&uiColor=%23000&availableInstruments=l%3A&instrument=EUR/USD&period=5&offerSide=BID&timezone=0&live=true&allowPan=true&width=100%25&height=700&adv=popup&lang=en",
	}

	uri := url.URL{
		Scheme:   "https",
		Host:     "freeserv.dukascopy.com",
		Path:     "/2.0/index.php",
		RawQuery: queryParams.Encode(),
	}

	reqURL := uri.String()
	req, err := http.NewRequest("GET", reqURL, nil)
	if err != nil {
		return nil, err
	}
	for k, v := range headers {
		req.Header.Set(k, v)
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	var builderResp strings.Builder
	buf := make([]byte, 4096)
	for {
		n, err := resp.Body.Read(buf)
		builderResp.Write(buf[:n])
		if n == 0 || err != nil {
			break
		}
	}

	responseText := builderResp.String()
	jsonText := strings.TrimSuffix(strings.TrimPrefix(responseText, jsonp+"("), ");")

	result := [][]any{}
	if err := json.Unmarshal([]byte(jsonText), &result); err != nil {
		return nil, err
	}

	if len(result) == 1 && len(result[0]) == 0 {
		result = [][]any{}
	}

	return result, nil
}

func stream(
	ctx context.Context,
	instrument string,
	interval string,
	offerSide string,
	start time.Time,
	end time.Time,
	maxRetries int,
	limit int,
) <-chan []any {
	logger := getCustomLogger(ctx)

	out := make(chan []any)

	go func() {
		defer close(out)

		noOfRetries := 0
		cursor := start.UnixMilli()
		var endTimestamp int64
		if !end.IsZero() {
			t := end.UnixMilli()
			endTimestamp = t
		}

		isFirstIteration := true

		logger.Printf("Start Date: %s", start.Format(time.RFC3339))
		if !end.IsZero() {
			logger.Printf("End Date: %s", end.Format(time.RFC3339))
		} else {
			logger.Printf("End Date:")
		}

		for {

			select {
			case <-ctx.Done():
				err := ctx.Err()
				if err == context.Canceled {
					logger.Println("Context was canceled")
				} else if err == context.DeadlineExceeded {
					logger.Println("Context deadline exceeded")
				} else if err != nil {
					logger.Println("Context done with error:", err)
				}
				return
			default:
				// logger.Println("Context still active")
			}

			lastUpdates, err := fetch(ctx, instrument, interval, offerSide, cursor, limit)
			if err != nil {
				noOfRetries++
				if maxRetries != -1 && noOfRetries > maxRetries {
					logger.Printf("Error fetching (max retries reached): %v", err)
					return
				}
				logger.Printf("An error occurred: %v", err)
				logger.Println("Retrying...")
				time.Sleep(1 * time.Second)
				continue
			}

			if !isFirstIteration && len(lastUpdates) > 0 && int64(lastUpdates[0][0].(float64)) == cursor {
				lastUpdates = lastUpdates[1:]
			}

			if len(lastUpdates) < 1 {
				if !end.IsZero() {
					return
				}
				continue
			}

			for _, row := range lastUpdates {
				timestamp := int64(row[0].(float64))
				if endTimestamp != 0 && timestamp > endTimestamp {
					return
				}
				if interval == INTERVAL_TICK {
					row[len(row)-1] = row[len(row)-1].(float64) / 1_000_000
					row[len(row)-2] = row[len(row)-2].(float64) / 1_000_000
				}
				out <- row
				cursor = timestamp
			}

			logger.Printf("Current timestamp: %s", time.UnixMilli(cursor).Format(time.RFC3339))

			noOfRetries = 0
			isFirstIteration = false
		}
	}()
	return out
}

type Dataframe interface {
	AddRows(values ...[]any)
	ToCSV(w io.Writer) error
	ToJSON(w io.Writer) error
	Shape() [2]int
	Rows() [][]any
	Columns() []string
}

type dataframe struct {
	rowIndex    int
	rows        [][]any
	columns     []string
	rowIndexMap map[any][]any
}

func (df *dataframe) Rows() [][]any {
	return df.rows
}

func (df *dataframe) Columns() []string {
	return df.columns
}

func (df *dataframe) Shape() [2]int {
	return [2]int{len(df.rows), len(df.columns)}
}

func (df *dataframe) AddRows(values ...[]any) {
	if df.rowIndexMap == nil {
		df.rowIndexMap = map[any][]any{}
	}

	for _, value := range values {
		index := value[df.rowIndex]

		_, exists := df.rowIndexMap[index]
		if !exists {
			df.rows = append(df.rows, value)
		}

		df.rowIndexMap[index] = value
	}

}

func (df *dataframe) ToCSV(w io.Writer) error {

	writer := csv.NewWriter(w)
	defer writer.Flush()

	// Write headers
	if err := writer.Write(df.columns); err != nil {
		return err
	}

	// Write each row
	for _, row := range df.rows {
		strRow := make([]string, len(row))
		for i, val := range row {
			strRow[i] = stringify(val)
		}
		if err := writer.Write(strRow); err != nil {
			return err
		}
	}

	return nil
}

func (df *dataframe) ToJSON(w io.Writer) error {

	records := map[string][]any{}
	for _, row := range df.rows {
		for index, column := range df.columns {
			cols := records[column]

			if cols == nil {
				records[column] = []any{}
				cols = records[column]
			}

			cols = append(cols, row[index])
			records[column] = cols
		}

	}

	encoder := json.NewEncoder(w)
	encoder.SetIndent("", "  ")
	return encoder.Encode(records)
}

// Helper to stringify any value (for CSV)
func stringify(v any) string {
	if v == nil {
		return ""
	}
	return fmt.Sprintf("%v", v)
}

type FetchArgs struct {
	Instrument string
	OfferSide  string
	Start      time.Time
	End        time.Time
	MaxRetries int
	Limit      int
	Debug      bool
	//
	Interval string
}

func Fetch(
	ctx context.Context,
	arg FetchArgs,
) Dataframe {
	ctx = setCustomLogger(ctx, arg.Debug)
	logger := getCustomLogger(ctx)

	// Get time unit and column names
	timeUnit, ok := intervalUnits[arg.Interval]
	if !ok {
		logger.Fatalf("invalid interval: %s", arg.Interval)
	}

	if arg.Limit == 0 {
		arg.Limit = 30000
	}

	columns := getColumnsForTimeUnit(timeUnit)

	// Fetch data from stream
	datafeed := stream(ctx, arg.Instrument, arg.Interval, arg.OfferSide, arg.Start, arg.End, arg.MaxRetries, arg.Limit)
	var data [][]any

	for row := range datafeed {
		data = append(data, row)
	}

	for i, row := range data {
		if timestampMs, ok := row[0].(float64); ok {
			data[i][0] = time.UnixMilli(int64(timestampMs)).UTC()
		}
	}

	df := &dataframe{
		rowIndex: 0,
		columns:  columns,
	}
	df.AddRows(data...)

	return df
}

type LiveFetchArgs struct {
	Instrument string
	OfferSide  string
	Start      time.Time
	End        time.Time
	MaxRetries int
	Limit      int
	Debug      bool
	//
	IntervalValue int
	TimeUnit      string
}

func LiveFetch(ctx context.Context, arg LiveFetchArgs) <-chan Dataframe {
	ctx = setCustomLogger(ctx, arg.Debug)
	logger := getCustomLogger(ctx)

	if arg.IntervalValue <= 0 {
		logger.Fatalf("invalid interval value: %d", arg.IntervalValue)
	}

	// Validate time unit
	_, err := resampleToNearest(time.Now(), arg.TimeUnit, arg.IntervalValue)

	if err != nil {
		logger.Fatalf(err.Error())
	}

	if arg.Limit == 0 {
		arg.Limit = 30000
	}

	var open *float64
	high, low, _close, volume := 0.0, 0.0, 0.0, 0.0
	var lastTimestamp time.Time = time.Time{}
	lastTickCount := -1

	priceIndex, ok := map[string]int{
		OFFER_SIDE_BID: 1,
		OFFER_SIDE_ASK: 2,
	}[arg.OfferSide]

	if !ok {
		logger.Fatalf("invalid offer_side value: %v", arg.OfferSide)
	}

	volumeIndex, ok := map[string]int{
		OFFER_SIDE_BID: -2,
		OFFER_SIDE_ASK: -1,
	}[arg.OfferSide]

	if !ok {
		logger.Fatalf("invalid offer_side value: %v", arg.OfferSide)
	}

	columns := getColumnsForTimeUnit(arg.TimeUnit)
	out := make(chan Dataframe)

	go func() {
		defer close(out)

		df := &dataframe{
			rowIndex: 0,
			columns:  columns,
		}

		out <- df

		rowIndex := 0
		datafeed := stream(ctx, arg.Instrument, INTERVAL_TICK, arg.OfferSide, arg.Start, arg.End, arg.MaxRetries, arg.Limit)

		for row := range datafeed {
			timestamp, _ := resampleToNearest(time.UnixMilli(int64(row[0].(float64))).UTC(), arg.TimeUnit, arg.IntervalValue)

			if lastTimestamp.IsZero() {
				lastTimestamp = timestamp
			}

			if arg.TimeUnit == TIME_UNIT_TICK && arg.IntervalValue == 1 {
				df.AddRows(row)
				out <- df
				continue
			}

			newTickCount := rowIndex / arg.IntervalValue

			if (arg.TimeUnit != TIME_UNIT_TICK && !timestamp.Equal(lastTimestamp)) ||
				(arg.TimeUnit == TIME_UNIT_TICK && lastTickCount != newTickCount) {
				if open != nil {
					df.AddRows([]any{lastTimestamp, open, high, low, _close, volume})
					out <- df
				}
				lastTimestamp = timestamp
				lastTickCount = newTickCount
				open = nil
			}

			price := row[priceIndex].(float64)
			vol := row[len(row)+volumeIndex].(float64)

			if open == nil {
				open = &price
				_close = price
				low = price
				high = price
				volume = 0
			}

			_close = price
			high = math.Max(high, _close)
			low = math.Min(low, _close)
			volume += vol

			df.AddRows([]any{timestamp, open, high, low, _close, volume})
			rowIndex++
		}
	}()

	return out
}

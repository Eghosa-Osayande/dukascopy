use chrono::{TimeZone, Utc};
use dukascopy_rust::dukascopy_base::fetch;
use dukascopy_rust::instrument_generator::fetch_instrument_groups;
use dukascopy_rust::models::Candle;

#[tokio::test]
async fn test_groups_parsing() {
    let groups = fetch_instrument_groups(None)
        .await
        .expect("should fetch groups");
    assert!(groups.contains_key("FX"));
}

#[tokio::test]
async fn test_fetch_ohlc() {
    // Use a fixed date to ensure data is available
    let start = Utc
        .with_ymd_and_hms(2025, 1, 1, 0, 0, 0)
        .unwrap()
        .timestamp_millis();
    let rows = fetch("EUR/USD", "1DAY", "B", start, Some(1), None)
        .await
        .expect("should fetch data");
    assert!(!rows.is_empty());
}

#[tokio::test]
async fn test_candle_conversion() {
    // Fetch one OHLC row and convert to Candle
    let start = Utc
        .with_ymd_and_hms(2025, 1, 1, 0, 0, 0)
        .unwrap()
        .timestamp_millis();
    let raw_rows = fetch("EUR/USD", "1DAY", "B", start, Some(1), None)
        .await
        .expect("should fetch data");
    assert!(!raw_rows.is_empty(), "No raw rows returned");

    let first_row = raw_rows.into_iter().next().unwrap();
    let candle = Candle::try_from(first_row).expect("Failed to convert raw row to Candle");

    // Validate fields
    assert_eq!(candle.timestamp, start);
    assert!(candle.open > 0.0, "Open price should be positive");
    assert!(candle.high >= candle.open, "High should be >= open");
    assert!(candle.low <= candle.open, "Low should be <= open");
    assert!(
        candle.close >= candle.low && candle.close <= candle.high,
        "Close should be within low-high range"
    );
    assert!(candle.volume >= 0.0, "Volume should be non-negative");
}

use dukascopy_rust::dukascopy_base::fetch;
use dukascopy_rust::dukascopy_base::stream;
use dukascopy_rust::models::Candle;

use chrono::{TimeZone, Utc}; // bring the TimeZone trait into scope
use dukascopy_rust::instrument_generator;
use futures::{pin_mut, StreamExt};
#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1) Fetch instrument groups
    let groups = instrument_generator::fetch_instrument_groups(None).await?;
    println!("Groups: {:?}", groups.keys());

    // 2) Fetch 5 daily EUR/USD bars
    let start_dt = Utc.with_ymd_and_hms(2025, 1, 1, 0, 0, 0).unwrap();
    let start_ms = start_dt.timestamp_millis();
    let bars = fetch("EUR/USD", "1DAY", "B", start_ms, Some(5), None).await?;
    println!("First 5 daily bars: {:?}", bars);

    // 3) Stream ticks for 5 seconds
    let now = Utc::now().timestamp_millis();
    let ticks = stream(
        "EUR/USD".into(),
        "TICK".into(),
        "B".into(),
        now,
        Some(now + 5_000),
        None,
    );
    pin_mut!(ticks);

    while let Some(tick) = ticks.next().await {
        println!("Tick: {:?}", tick);
    }

    let raw = fetch("EUR/USD", "1DAY", "B", start_ms, Some(5), None).await?;
    let candles: Vec<Candle> = raw
        .into_iter()
        .map(Candle::try_from)
        .collect::<Result<_, _>>()?;
    println!("Candles: {:#?}", candles);

    Ok(())
}

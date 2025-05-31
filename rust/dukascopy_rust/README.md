# dukascopy_rust

[![Crates.io](https://img.shields.io/crates/v/dukascopy_rust.svg)](https://crates.io/crates/dukascopy_rust)  
[![Docs.rs](https://docs.rs/dukascopy_rust/badge.svg)](https://docs.rs/dukascopy_rust)

Rust wrapper for Dukascopy’s free charting API. Provides:

- **Instrument Discovery**: `fetch_instrument_groups()`
- **Historical Data**: `fetch(...)` → raw rows or typed `Candle`
- **Real-Time Streaming**: `stream(...)` → async `Stream` of ticks
- **Strong Typing**: `Candle` model via `TryFrom<Vec<Value>>`

---

## Installation

```toml
[dependencies]
dukascopy_rust = "0.2"
```

# Fetch dependencies
```bash 
cargo build
```

# Quick start
```rust
use dukascopy_rust::{
    instrument_generator::fetch_instrument_groups,
    dukascopy_base::{fetch, stream},
    models::Candle,
};
use chrono::{Utc, TimeZone};
use futures::{StreamExt, pin_mut};

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // 1) Instrument groups
    let groups = fetch_instrument_groups(None).await?;
    println!("Groups: {:?}", groups.keys());

    // 2) Historical OHLCV
    let start = Utc.with_ymd_and_hms(2025, 1, 1, 0, 0, 0).unwrap()
        .timestamp_millis();
    let raw: Vec<Vec<serde_json::Value>> =
        fetch("EUR/USD", "1DAY", "B", start, Some(5), None).await?;
    let candles: Vec<Candle> = raw
        .into_iter()
        .map(Candle::try_from)
        .collect::<Result<_, _>>()?;
    println!("Candles: {:#?}", candles);

    // 3) Live tick stream (10s)
    let now = Utc::now().timestamp_millis() - 2_000;
    let mut ticks = stream("EUR/USD".into(), "TICK".into(), "B".into(),
                           now, Some(now + 10_000), None);
    pin_mut!(ticks);
    while let Some(t) = ticks.next().await {
        println!("Tick: {:?}", t);
    }

    Ok(())
}
```
## Documentation

- **API docs**: https://docs.rs/dukascopy_rust  
- **Source**: https://github.com/Erhabor-Fona/dukascopy_rust

## License

Dual-licensed under **MIT**. See [LICENSE-MIT](LICENSE-MIT) for details.

use serde::Deserialize;
use serde_json::Value;
use std::collections::HashMap;

#[derive(Debug)]
pub struct Candle {
    pub timestamp: i64,
    pub open: f64,
    pub high: f64,
    pub low: f64,
    pub close: f64,
    pub volume: f64,
}

// Individual instrument group
#[derive(Debug, Deserialize)]
pub struct InstrumentGroup {
    pub id: String,
    pub title: String,
    #[serde(default)]
    pub parent: Option<String>,
    #[serde(default)]
    pub instruments: Vec<String>,
}

// Top-level response wrapper
#[derive(Debug, Deserialize)]
pub struct GroupsResponse {
    pub groups: HashMap<String, InstrumentGroup>,
}
// Response for the instrument group request
// #[derive(Debug, Deserialize)]
// pub struct InstrumentGroupResponse {
//     pub groups: Vec<InstrumentGroup>,
// }

/// Convert a raw JSON row into a `Candle`
impl TryFrom<Vec<Value>> for Candle {
    type Error = Box<dyn std::error::Error>;

    fn try_from(mut row: Vec<Value>) -> Result<Self, Self::Error> {
        Ok(Candle {
            timestamp: row.remove(0).as_i64().ok_or("timestamp parse")?,
            open: row.remove(0).as_f64().ok_or("open parse")?,
            high: row.remove(0).as_f64().ok_or("high parse")?,
            low: row.remove(0).as_f64().ok_or("low parse")?,
            close: row.remove(0).as_f64().ok_or("close parse")?,
            volume: row.remove(0).as_f64().ok_or("volume parse")?,
        })
    }
}

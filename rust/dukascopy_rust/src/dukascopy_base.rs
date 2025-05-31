use futures::stream::{self, Stream};
use rand::{distributions::Alphanumeric, thread_rng, Rng};
use reqwest::header::{HeaderMap, REFERER, USER_AGENT};
use reqwest::Client;
use serde_json::Value;
use std::error::Error;

const CHART_URL: &str = "https://freeserv.dukascopy.com/2.0/index.php";

fn random_callback() -> String {
    let suffix: String = thread_rng()
        .sample_iter(&Alphanumeric)
        .take(9)
        .map(char::from)
        .collect();
    format!("_callbacks____{}", suffix)
}

fn strip_jsonp(s: &str) -> &str {
    if let (Some(start), Some(end)) = (s.find('('), s.rfind(')')) {
        &s[start + 1..end]
    } else {
        s
    }
}

// One-off fetch: returns raw rows (vectors of JSON values)
pub async fn fetch(
    instrument: &str,
    interval: &str,
    offer_side: &str,
    last_update: i64,
    limit: Option<usize>,
    client: Option<&Client>,
) -> Result<Vec<Vec<Value>>, Box<dyn Error>> {
    let http_client = client.cloned().unwrap_or_else(Client::new);
    let callback = random_callback();

    // Build an owned Vec of (String, String)
    let mut params: Vec<(String, String)> = vec![
        ("path".into(), "chart/json3".into()),
        ("splits".into(), "true".into()),
        ("stocks".into(), "true".into()),
        ("time_direction".into(), "N".into()),
        ("jsonp".into(), callback.clone()),
        ("last_update".into(), last_update.to_string()),
        ("offer_side".into(), offer_side.into()),
        ("instrument".into(), instrument.into()),
        ("interval".into(), interval.into()),
    ];

    if let Some(lim) = limit {
        params.push(("limit".into(), lim.to_string()));
    }

    let mut headers = HeaderMap::new();
    headers.insert(USER_AGENT, "rust-reqwest/0.11".parse().unwrap());
    headers.insert( REFERER,
            "https://freeserv.dukascopy.com/2.0/?path=chart/index&showUI=true&showTabs=true&showParameterToolbar=true&showOfferSide=true&allowInstrumentChange=true&allowPeriodChange=true&allowOfferSideChange=true&showAdditionalToolbar=true&showExportImportWorkspace=true&allowSocialSharing=true&showUndoRedoButtons=true&showDetachButton=true&presentationType=candle&axisX=true&axisY=true&legend=true&timeline=true&showDateSeparators=true&showZoom=true&showScrollButtons=true&showAutoShiftButton=true&crosshair=true&borders=false&freeMode=false&theme=Pastelle&uiColor=%23000&availableInstruments=l%3A&instrument=EUR/USD&period=5&offerSide=BID&timezone=0&live=true&allowPan=true&width=100%25&height=700&adv=popup&lang=en"
                .parse().unwrap(),
   );

    let resp = http_client
        .get(CHART_URL)
        .headers(headers)
        .query(&params)
        .send()
        .await?;
    resp.error_for_status_ref()?;

    let body = resp.text().await?;
    if body.is_empty() {
        return Err("Empty chart response".into());
    }
    let payload = strip_jsonp(&body);
    let raw: Vec<Vec<Value>> = serde_json::from_str(payload)?;
    Ok(raw)
}

// Stream rows until `end` timestamp, with simple retry on empty
pub fn stream(
    instrument: String,
    interval: String,
    offer_side: String,
    start: i64,
    end: Option<i64>,
    client: Option<Client>,
) -> impl Stream<Item = Vec<Value>> {
    let client = client.unwrap_or_default();
    stream::unfold((start, true), move |(cursor, first)| {
        let inst = instrument.clone();
        let intl = interval.clone();
        let side = offer_side.clone();
        let cli = client.clone();
        let end_ts = end; // capture it

        async move {
            match fetch(&inst, &intl, &side, cursor, None, Some(&cli)).await {
                Ok(mut rows) if !rows.is_empty() => {
                    if !first && rows[0][0].as_i64() == Some(cursor) {
                        rows.remove(0);
                    }
                    // Take the first row, compute its timestamp, and yield it:
                    let row = rows.remove(0);
                    let ts = row[0].as_i64().unwrap_or(cursor);
                    // If we've passed `end`, bail out:
                    if end_ts.is_some_and(|e| ts > e)  {
                        return None;
                    }
                    Some((row, (ts, false)))
                }
                _ => None,
            }
        }
    })
}

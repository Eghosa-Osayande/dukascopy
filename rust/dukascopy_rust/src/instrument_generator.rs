use crate::models::{GroupsResponse, InstrumentGroup};
use rand::{distributions::Alphanumeric, thread_rng, Rng};
use reqwest::header::{HeaderMap, REFERER, USER_AGENT};
use reqwest::Client;
use std::collections::HashMap;
use std::error::Error;

const BASE_URL: &str = "https://freeserv.dukascopy.com/2.0/index.php";

// random JSONP callback
fn random_callback() -> String {
    let suffix: String = thread_rng()
        .sample_iter(&Alphanumeric)
        .take(9)
        .map(char::from)
        .collect();
    format!("_callbacks____{}", suffix)
}

// Strip JSONP padding: return inner JSON
fn strip_jsonp(s: &str) -> &str {
    if let (Some(start), Some(end)) = (s.find('('), s.rfind(')')) {
        &s[start + 1..end]
    } else {
        s
    }
}

// Fetch the instrument groups from Dukascopy.
pub async fn fetch_instrument_groups(
    client: Option<&Client>,
) -> Result<HashMap<String, InstrumentGroup>, Box<dyn Error>> {
    let client = client.cloned().unwrap_or_else(Client::new);
    let callback = random_callback();
    let url = format!("{}?path=common/instruments&jsonp={}", BASE_URL, callback);
    let mut headers = HeaderMap::new();
    headers.insert(USER_AGENT, "rust-reqwest/0.11".parse().unwrap());
    headers.insert(
        REFERER,
        "https://freeserv.dukascopy.com/2.0/?path=chart/index&showUI=true&showTabs=true&showParameterToolbar=true&showOfferSide=true&allowInstrumentChange=true&allowPeriodChange=true&allowOfferSideChange=true&showAdditionalToolbar=true&showExportImportWorkspace=true&allowSocialSharing=true&showUndoRedoButtons=true&showDetachButton=true&presentationType=candle&axisX=true&axisY=true&legend=true&timeline=true&showDateSeparators=true&showZoom=true&showScrollButtons=true&showAutoShiftButton=true&crosshair=true&borders=false&freeMode=false&theme=Pastelle&uiColor=%23000&availableInstruments=l%3A&instrument=EUR/USD&period=5&offerSide=BID&timezone=0&live=true&allowPan=true&width=100%25&height=700&adv=popup&lang=en"
            .parse()
            .unwrap(),
   );

    // let resp = client.get(&url).send().await?;
    let resp = client.get(&url).headers(headers).send().await?;
    resp.error_for_status_ref()?;
    let body = resp.text().await?;
    if body.is_empty() {
        return Err("Empty response".into());
    }
    let payload = strip_jsonp(&body);
    let gr: GroupsResponse = serde_json::from_str(payload)?;
    Ok(gr.groups)
}

# dukascopy

A Dart wrapper for Dukascopy’s free charting API. It makes it easy to:

- Fetch available instrument groups (e.g., Forex, Commodities, Indices)  
- Retrieve historical OHLC (open, high, low, close) data  
- Stream live tick data (bid/ask prices)  

---

## Installation

Add the package to your `pubspec.yaml`:

```yaml
dependencies:


  dukascopy: ^0.1.3

  ```
Then fetch:
```bash
dart pub get
```
## Usage Example

```Dart
import 'package:dukascopy/dukascopy.dart';

void main() async {
  // Load instrument groups
  final groups = await fetchInstrumentGroups();
  print('Groups: ${groups.keys}');

  // Fetch 5 days of EUR/USD daily data:
  final start = DateTime.utc(2025,1,1);
  final dailyRows = await fetch(
    instrument: 'EUR/USD',
    interval: '1DAY',
    offerSide: 'B',
    lastUpdateMillis: start.millisecondsSinceEpoch,
    limit: 5,
  );
  dailyRows.forEach((row) {
    print('Timestamp=${row[0]}, OHLC=[${row[1]},${row[2]},${row[3]},${row[4]}], vol=${row[5]}');
  });

  // Stream tick data for the next 10 seconds:
  final now = DateTime.now().toUtc();
  await for (final tick in stream(
    instrument: 'EUR/USD',
    interval: 'TICK',
    offerSide: 'B',
    startMillis: now.millisecondsSinceEpoch,
    endMillis: now.add(const Duration(seconds: 10)).millisecondsSinceEpoch,
    limit: 10,
  )) {
    print('Tick @${tick[0]}: bid=${tick[1]}, ask=${tick[2]}');
  }
}
```
See example/dukascopy_example.dart for a complete demo.

## Pub.dev

Once published, you can find the package at:

👉 [https://pub.dev/packages/dukascopy](https://pub.dev/packages/dukascopy)

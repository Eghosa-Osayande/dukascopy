# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- …

### Changed
- …

### Fixed
- …

## [0.2.0] - 2025-05-04

### Added
- `Candle` model and `TryFrom<Vec<Value>>` conversion
- `test_candle_conversion` integration test
- Async integration tests for `fetch()` and `fetch_instrument_groups()`

### Changed
- Updated stream to respect `end` timestamp
- Switched to owned `(String, String)` query parameters to avoid temporary-borrow errors

### Fixed
- Added `Referer` and `User-Agent` headers to avoid 403s
- Pin stream with `pin_mut!` in examples

## [0.1.0] - 2025-04-30

### Added
- Initial release: `fetch_instrument_groups`, `fetch`, `stream`
- Basic example in `examples/dukascopy_example.rs`
- Instrument‐ and chart‐data wrappers


# USDA FAS Open Data SDK (Python)

A powerful, Pythonic SDK for the **USDA Foreign Agricultural Service (FAS) Open Data API**. 
This library provides easy access to vast agricultural data sets including Export Sales, Global Trade, and Production/Supply/Distribution data.

**Source Data**: [USDA FAS Open Data](https://apps.fas.usda.gov/opendatawebV2/#/)

## Data Sets Available

- **ESR (Export Sales Reporting)**: Weekly U.S. export sales of agricultural commodities.
- **GATS (Global Agricultural Trade System)**: U.S. Census and UN ComTrade import/export data.
- **PSD (Production, Supply and Distribution)**: Official USDA forecasts for world agricultural commodities.

## Features

- **Auth Handling**: Seamless integration with USDA FAS API keys.
- **Easy Mode**: `USDAFASEasyClient` automatically normalizes data, replacing numeric codes (e.g., `CountryCode: 2010`) with readable names and descriptions (e.g., `Name: Mexico`, `Genc: MEX`).
- **Weekly ESR Helpers**: Convenience methods for latest market year, latest week ending date, exact week filters, and normalized weekly export-sales pulls.
- **Core Endpoint Coverage**: Wrappers for the main ESR, GATS, and PSD REST endpoints used in the USDA FAS Open Data API.
- **Type Hints**: Fully typed for better IDE support.

## Prerequisites

You need a **USDA FAS API Key** to use this SDK.

1.  Go to the [USDA FAS Open Data Portal](https://apps.fas.usda.gov/opendatawebV2/#/).
2.  Open the "API Keys" section.
3.  Generate or retrieve your API key.

## Installation

```bash
pip install usda-fas-sdk
```

## Quick Start

### 1. Configure Authentication

We recommend using a `.env` file to keep your API key secure.

**Step 1:** Create a file named `.env` in your project root:
```env
USDA_FAS_API_KEY=your_actual_api_key_here
```

**Step 2:** Use the SDK
```python
from usda_fas import USDAFASEasyClient
import json

# Automatically loads USDA_FAS_API_KEY from environment or .env
client = USDAFASEasyClient()

# Example: Pull the latest weekly export-sales records for Corn (Code 401)
data = client.get_esr_latest_week_exports_normalized(commodity_code=401)

if data:
    # Print the first enriched record from the latest week
    print(json.dumps(data[0], indent=2))
```

**Output Example:**
```json
{
  "commodityCode": 401,
  "countryCode": 1220,
  "weeklyExports": 7528,
  "accumulatedExports": 446444,
  "outstandingSales": 179032,
  "grossNewSales": 3493,
  "currentMYNetSales": 3493,
  "currentMYTotalCommitment": 625476,
  "nextMYOutstandingSales": 0,
  "nextMYNetSales": 0,
  "unitId": 1,
  "weekEndingDate": "2026-04-23T00:00:00",
  "countryName": "CANADA  ",
  "countryDescription": "CANADA                         ",
  "gencCode": "CAN",
  "regionName": "WESTERN HEMISPHERE",
  "commodityName": "Corn",
  "unitName": "Metric Tons"
}
```

### 2. Manual Configuration (Alternative)
You can also pass the key directly (not recommended for production code):
```python
client = USDAFASEasyClient(api_key="your_api_key_string")
```

### 3. Pull a Specific Week
Use a week ending date if you want a reproducible weekly snapshot:

```python
from usda_fas import USDAFASEasyClient

client = USDAFASEasyClient()

week_data = client.get_esr_exports_for_week_normalized(
    commodity_code=401,
    week_ending_date="2026-04-23",
)
```

## Advanced Usage

### Accessing Raw Clients
If you prefer raw data or specific client separation, you can access the individual clients:

```python
from usda_fas import ESRClient, GATSClient, PSDClient

esr = ESRClient() # Uses env var
raw_commodities = esr.get_esr_commodities()
```

### Weekly ESR Workflow
The raw ESR client can help you drive weekly export-sales ingestion without hard-coding dates:

```python
from usda_fas import ESRClient

esr = ESRClient()

latest_market_year = esr.get_esr_latest_market_year(401)
latest_week = esr.get_esr_latest_week_ending_date(401, market_year=latest_market_year)
latest_rows = esr.get_esr_latest_week_exports(401, market_year=latest_market_year)
canada_rows = esr.get_esr_exports_for_week(
    commodity_code=401,
    week_ending_date=latest_week,
    market_year=latest_market_year,
    country_code=1220,
)
```

### Client Configuration
You can optionally override the request timeout or API host:

```python
client = USDAFASEasyClient(timeout=60)
```

## Contributing

1.  Fork the repo.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Submit a Pull Request.

## License

MIT

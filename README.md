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
- **Complete Coverage**: Support for all endpoints defined in the official Swagger spec.
- **Type Hints**: Fully typed for better IDE support.

## Prerequisites

You need a **USDA FAS API Key** to use this SDK.

1.  Go to the [USDA FAS Open Data Portal](https://apps.fas.usda.gov/opendatawebV2/#/).
2.  Register or Login.
3.  Navigate to the "API Keys" section to generate your key.

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

# Example: Get Normalized Export Sales Data for Wheat (Code 301) in 2024
data = client.get_esr_exports_normalized(commodity_code=301, market_year=2024)

if data:
    # Print the first enriched record
    print(json.dumps(data[0], indent=2))
```

**Output Example:**
```json
{
  "commodityCode": 301,
  "countryCode": 5800,
  "weeklyExports": 0,
  "accumulatedExports": 0,
  "outstandingSales": 1323,
  "grossNewSales": 1323,
  "currentMYNetSales": 0,
  "currentMYTotalCommitment": 1323,
  "nextMYOutstandingSales": 0,
  "nextMYNetSales": 0,
  "unitId": 1,
  "weekEndingDate": "2023-06-01T00:00:00",
  "countryName": "KOR REP ",
  "countryDescription": "KOREA, REPUBLIC OF             ",
  "gencCode": null,
  "regionName": "OTHER ASIA AND OCEANIA        ",
  "commodityName": "Barley",
  "unitName": "Metric Tons"
}
```

### 2. Manual Configuration (Alternative)
You can also pass the key directly (not recommended for production code):
```python
client = USDAFASEasyClient(api_key="your_api_key_string")
```

## Advanced Usage

### Accessing Raw Clients
If you prefer raw data or specific client separation, you can access the individual clients:

```python
from usda_fas import ESRClient, GATSClient, PSDClient

esr = ESRClient() # Uses env var
raw_commodities = esr.get_esr_commodities()
```

## Contributing

1.  Fork the repo.
2.  Install dependencies: `pip install -r requirements.txt`.
3.  Submit a Pull Request.

## License

MIT

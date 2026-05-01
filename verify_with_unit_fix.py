from usda_fas import USDAFASEasyClient
import json


def main():
    try:
        # api_key loaded from env
        client = USDAFASEasyClient()
    except ValueError as e:
        print(f"Configuration error: {e}")
        print("Set USDA_FAS_API_KEY in your environment or .env before running this script.")
        return

    print("--- Testing ESR Regions ---")
    try:
        regions = client.get_esr_regions()
        print(f"Successfully fetched {len(regions)} regions.")
        if regions:
            print("Sample Region:", regions[0])
    except Exception as e:
        print(f"Error fetching regions: {e}")

    print("\n--- Testing ESR Commodities ---")
    try:
        commodities = client.get_esr_commodities()
        print(f"Successfully fetched {len(commodities)} commodities.")
        if commodities:
            print("Sample Commodity:", commodities[0])
            sample_commodity_code = commodities[0].get('commodityCode')
            print(f"Will use Commodity Code {sample_commodity_code} for next test.")
    except Exception as e:
        print(f"Error fetching commodities: {e}")
        sample_commodity_code = None

    if sample_commodity_code:
        print(f"\n--- Testing ESR Release Metadata (Commodity: {sample_commodity_code}) ---")
        try:
            release_info = client.get_esr_release_info(sample_commodity_code)
            latest_market_year = client.get_esr_latest_market_year(sample_commodity_code)
            latest_week = client.get_esr_latest_week_ending_date(
                sample_commodity_code,
                market_year=latest_market_year,
            )
            print("Release Info:", json.dumps(release_info, indent=2))
            print("Latest Market Year:", latest_market_year)
            print("Latest Week Ending Date:", latest_week)
        except Exception as e:
            print(f"Error fetching release metadata: {e}")
            latest_market_year = None

    if sample_commodity_code and latest_market_year:
        print(
            f"\n--- Testing ESR Latest Weekly Normalized Query "
            f"(Commodity: {sample_commodity_code}, Year: {latest_market_year}) ---"
        )
        try:
            data = client.get_esr_latest_week_exports_normalized(
                sample_commodity_code,
                market_year=latest_market_year,
            )
            print(f"Successfully fetched {len(data)} records.")
            if data:
                print("Sample Normalized Record:")
                print(json.dumps(data[0], indent=2))
            else:
                print("No data found for this commodity.")
        except Exception as e:
            print(f"Error fetching normalized data: {e}")

if __name__ == "__main__":
    main()

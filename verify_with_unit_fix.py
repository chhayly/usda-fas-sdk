from usda_fas import USDAFASEasyClient
import json

def main():
    # api_key loaded from env
    client = USDAFASEasyClient()

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
        print(f"\n--- Testing ESR Normalized Query (Commodity: {sample_commodity_code}, Year: 2024) ---")
        try:
            # Using recent year 2024, might need adjustment if no data
            data = client.get_esr_exports_normalized(sample_commodity_code, 2024)
            print(f"Successfully fetched {len(data)} records.")
            if data:
                print("Sample Normalized Record:")
                print(json.dumps(data[0], indent=2))
            else:
                print("No data found for this year/commodity.")
        except Exception as e:
            print(f"Error fetching normalized data: {e}")

if __name__ == "__main__":
    main()

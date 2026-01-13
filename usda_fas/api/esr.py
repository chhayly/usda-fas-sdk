from typing import List, Dict, Any, Union
from ..client import USDAFASClient

class ESRClient(USDAFASClient):
    """
    Client for the Export Sales Reporting (ESR) API.
    """

    def get_esr_regions(self) -> List[Dict[str, Any]]:
        """
        Returns a set of records with Region Codes and Region Names.
        """
        return self._make_request("GET", "/api/esr/regions")

    def get_esr_countries(self) -> List[Dict[str, Any]]:
        """
        Returns a set of records with Countries and their corresponding Regions.
        """
        return self._make_request("GET", "/api/esr/countries")

    def get_esr_commodities(self) -> List[Dict[str, Any]]:
        """
        Returns a set of records with Commodity Information.
        """
        return self._make_request("GET", "/api/esr/commodities")

    def get_esr_units_of_measure(self) -> List[Dict[str, Any]]:
        """
        Returns a set of records with Units of Measure Information.
        """
        return self._make_request("GET", "/api/esr/unitsOfMeasure")

    def get_esr_data_release_dates(self) -> List[Dict[str, Any]]:
        """
        Returns a set of records with the date of the last release of ESR Commodity Export Data.
        """
        return self._make_request("GET", "/api/esr/datareleasedates")

    def get_esr_exports_all_countries(self, commodity_code: int, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns US Export records of a commodity to all applicable countries for the given Market Year.

        Args:
            commodity_code (int): Commodity Code (e.g., 104 for Wheat - White).
            market_year (int): Market Year (e.g., 2017).
        """
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{market_year}"
        return self._make_request("GET", endpoint)

    def get_esr_exports_by_country(self, commodity_code: int, country_code: int, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns US Export records of a commodity to a specific country for the given Market Year.

        Args:
            commodity_code (int): Commodity Code.
            country_code (int): Country Code (e.g., 1220 for Canada).
            market_year (int): Market Year.
        """
        endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/countryCode/{country_code}/marketYear/{market_year}"
        return self._make_request("GET", endpoint)

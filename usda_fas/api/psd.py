from typing import List, Dict, Any
from ..client import USDAFASClient

class PSDClient(USDAFASClient):
    """
    Client for PSD Data API - Production, Supply and Distribution Forecast Data of World Agricultural Commodities.
    """

    def get_psd_data_release_dates(self, commodity_code: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/psd/commodity/{commodity_code}/dataReleaseDates"
        return self._make_request("GET", endpoint)

    def get_psd_commodity_data_by_year(self, commodity_code: str, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns Forecast number for a given Commodity Code and Market Year for all applicable countries.
        """
        endpoint = f"/api/psd/commodity/{commodity_code}/country/all/year/{market_year}"
        return self._make_request("GET", endpoint)

    def get_psd_country_commodity_data_by_year(self, commodity_code: str, country_code: str, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns Forecast number for a given Commodity Code, Country, and Market Year.
        """
        endpoint = f"/api/psd/commodity/{commodity_code}/country/{country_code}/year/{market_year}"
        return self._make_request("GET", endpoint)

    def get_psd_world_commodity_data_by_year(self, commodity_code: str, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns Forecast number for a given Commodity Code and Market Year for the world.
        """
        endpoint = f"/api/psd/commodity/{commodity_code}/world/year/{market_year}"
        return self._make_request("GET", endpoint)

    def get_psd_regions(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/psd/regions")

    def get_psd_countries(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/psd/countries")

    def get_psd_commodities(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/psd/commodities")

    def get_psd_units_of_measure(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/psd/unitsOfMeasure")

    def get_psd_commodity_attributes(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/psd/commodityAttributes")

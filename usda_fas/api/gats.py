from typing import List, Dict, Any
from ..client import USDAFASClient

class GATSClient(USDAFASClient):
    """
    Client for the GATS Data API - US Census and UN ComTrade Import Export & Re-Export Data.
    """

    def get_gats_census_export_release_dates(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/census/data/exports/dataReleaseDates")

    def get_gats_census_import_release_dates(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/census/data/imports/dataReleaseDates")

    def get_gats_untrade_export_release_dates(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/UNTrade/data/exports/dataReleaseDates")

    def get_gats_untrade_import_release_dates(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/UNTrade/data/imports/dataReleaseDates")

    def get_gats_regions(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/regions")

    def get_gats_countries(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/countries")

    def get_gats_commodities(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/commodities")

    def get_gats_hs6_commodities(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/HS6Commodities")

    def get_gats_units_of_measure(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/unitsOfMeasure")

    def get_gats_customs_districts(self) -> List[Dict[str, Any]]:
        return self._make_request("GET", "/api/gats/customsDistricts")

    def get_gats_census_imports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/censusImports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_census_exports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/censusExports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_census_re_exports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/censusReExports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_customs_district_exports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/customsDistrictExports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_customs_district_imports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/customsDistrictImports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_customs_district_re_exports(self, partner_code: str, year: int, month: int) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/customsDistrictReExports/partnerCode/{partner_code}/year/{year}/month/{month}"
        return self._make_request("GET", endpoint)

    def get_gats_untrade_imports(self, reporter_code: str, year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/UNTradeImports/reporterCode/{reporter_code}/year/{year}"
        return self._make_request("GET", endpoint)

    def get_gats_untrade_exports(self, reporter_code: str, year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/UNTradeExports/reporterCode/{reporter_code}/year/{year}"
        return self._make_request("GET", endpoint)

    def get_gats_untrade_re_exports(self, reporter_code: str, year: str) -> List[Dict[str, Any]]:
        endpoint = f"/api/gats/UNTradeReExports/reporterCode/{reporter_code}/year/{year}"
        return self._make_request("GET", endpoint)

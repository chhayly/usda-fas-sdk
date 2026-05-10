from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from ..client import USDAFASClient

DateInput = Union[str, date, datetime]


class ESRClient(USDAFASClient):
    """
    Client for the Export Sales Reporting (ESR) API.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        timeout: int = 30,
        base_url: Optional[str] = None,
    ):
        super().__init__(api_key=api_key, timeout=timeout, base_url=base_url)
        self._esr_data_release_dates_cache: Optional[List[Dict[str, Any]]] = None
        self._esr_exports_cache: Dict[tuple[int, int, Optional[int]], List[Dict[str, Any]]] = {}

    @staticmethod
    def _normalize_date_value(value: DateInput) -> str:
        """
        Convert USDA API date strings or Python date objects to YYYY-MM-DD.
        """
        if isinstance(value, datetime):
            return value.date().isoformat()

        if isinstance(value, date):
            return value.isoformat()

        if isinstance(value, str):
            return value.split("T", 1)[0].split(" ", 1)[0]

        raise TypeError("week_ending_date must be a str, date, or datetime")

    @classmethod
    def _extract_week_ending_date(cls, record: Dict[str, Any]) -> Optional[str]:
        week_ending_date = record.get("weekEndingDate")
        if not week_ending_date:
            return None

        return cls._normalize_date_value(week_ending_date)

    @classmethod
    def _group_records_by_week_ending_date(cls, records: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        grouped_records: Dict[str, List[Dict[str, Any]]] = {}
        for record in records:
            week_ending_date = cls._extract_week_ending_date(record)
            if week_ending_date:
                grouped_records.setdefault(week_ending_date, []).append(record)

        return grouped_records

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
        if self._esr_data_release_dates_cache is None:
            self._esr_data_release_dates_cache = self._make_request("GET", "/api/esr/datareleasedates")

        return self._esr_data_release_dates_cache

    def get_esr_release_info(self, commodity_code: int) -> Optional[Dict[str, Any]]:
        """
        Return release metadata for a single commodity, if available.
        """
        for record in self.get_esr_data_release_dates():
            if str(record.get("commodityCode")) == str(commodity_code):
                return record

        return None

    def get_esr_latest_market_year(self, commodity_code: int) -> Optional[int]:
        """
        Return the latest market year for a commodity using the ESR release metadata.
        """
        release_info = self.get_esr_release_info(commodity_code)
        if not release_info:
            return None

        market_year = release_info.get("marketYear")
        return int(market_year) if market_year is not None else None

    def get_esr_exports_all_countries(self, commodity_code: int, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns US Export records of a commodity to all applicable countries for the given Market Year.

        Args:
            commodity_code (int): Commodity Code (e.g., 104 for Wheat - White).
            market_year (int): Market Year (e.g., 2017).
        """
        cache_key = (int(commodity_code), int(market_year), None)
        if cache_key not in self._esr_exports_cache:
            endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/allCountries/marketYear/{market_year}"
            self._esr_exports_cache[cache_key] = self._make_request("GET", endpoint)

        return self._esr_exports_cache[cache_key]

    def get_esr_exports_by_country(self, commodity_code: int, country_code: int, market_year: int) -> List[Dict[str, Any]]:
        """
        Returns US Export records of a commodity to a specific country for the given Market Year.

        Args:
            commodity_code (int): Commodity Code.
            country_code (int): Country Code (e.g., 1220 for Canada).
            market_year (int): Market Year.
        """
        cache_key = (int(commodity_code), int(market_year), int(country_code))
        if cache_key not in self._esr_exports_cache:
            endpoint = f"/api/esr/exports/commodityCode/{commodity_code}/countryCode/{country_code}/marketYear/{market_year}"
            self._esr_exports_cache[cache_key] = self._make_request("GET", endpoint)

        return self._esr_exports_cache[cache_key]

    def get_esr_exports(
        self,
        commodity_code: int,
        market_year: int,
        country_code: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Convenience wrapper around the ESR export endpoints.
        """
        if country_code is None:
            return self.get_esr_exports_all_countries(commodity_code, market_year)

        return self.get_esr_exports_by_country(commodity_code, country_code, market_year)

    def get_esr_latest_week_ending_date(
        self,
        commodity_code: int,
        market_year: Optional[int] = None,
        country_code: Optional[int] = None,
    ) -> Optional[str]:
        """
        Return the latest available week ending date for a commodity.

        If market_year is omitted, the latest market year from the release metadata is used.
        If country_code is provided, returns the latest week available for that country.
        """
        if market_year is None:
            market_year = self.get_esr_latest_market_year(commodity_code)

        if market_year is None:
            return None

        records = self.get_esr_exports(commodity_code, market_year, country_code=country_code)
        grouped_records = self._group_records_by_week_ending_date(records)
        if not grouped_records:
            return None

        return max(grouped_records)

    def get_esr_exports_for_week(
        self,
        commodity_code: int,
        week_ending_date: DateInput,
        market_year: Optional[int] = None,
        country_code: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return export records for a specific week ending date.

        If market_year is omitted, the latest market year from the release metadata is used.
        """
        if market_year is None:
            market_year = self.get_esr_latest_market_year(commodity_code)

        if market_year is None:
            return []

        target_week = self._normalize_date_value(week_ending_date)
        records = self.get_esr_exports(commodity_code, market_year, country_code=country_code)
        grouped_records = self._group_records_by_week_ending_date(records)
        return grouped_records.get(target_week, [])

    def get_esr_latest_week_exports(
        self,
        commodity_code: int,
        market_year: Optional[int] = None,
        country_code: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Return export records for the most recent week available for a commodity.

        If market_year is omitted, the latest market year from the release metadata is used.
        """
        if market_year is None:
            market_year = self.get_esr_latest_market_year(commodity_code)

        if market_year is None:
            return []

        records = self.get_esr_exports(commodity_code, market_year, country_code=country_code)
        grouped_records = self._group_records_by_week_ending_date(records)
        if not grouped_records:
            return []

        return grouped_records[max(grouped_records)]

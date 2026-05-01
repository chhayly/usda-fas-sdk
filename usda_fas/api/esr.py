from datetime import date, datetime
from typing import Any, Dict, List, Optional, Union

from ..client import USDAFASClient

DateInput = Union[str, date, datetime]


class ESRClient(USDAFASClient):
    """
    Client for the Export Sales Reporting (ESR) API.
    """

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
            return value.split("T", 1)[0]

        raise TypeError("week_ending_date must be a str, date, or datetime")

    @classmethod
    def _extract_week_ending_date(cls, record: Dict[str, Any]) -> Optional[str]:
        week_ending_date = record.get("weekEndingDate")
        if not week_ending_date:
            return None

        return cls._normalize_date_value(week_ending_date)

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

        return release_info.get("marketYear")

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
        """
        if market_year is None:
            market_year = self.get_esr_latest_market_year(commodity_code)

        if market_year is None:
            return None

        records = self.get_esr_exports(commodity_code, market_year, country_code=country_code)
        week_ending_dates = [
            week_ending_date
            for week_ending_date in (self._extract_week_ending_date(record) for record in records)
            if week_ending_date
        ]
        if not week_ending_dates:
            return None

        return max(week_ending_dates)

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

        return [
            record
            for record in records
            if self._extract_week_ending_date(record) == target_week
        ]

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
        latest_week = None

        for record in records:
            week_ending_date = self._extract_week_ending_date(record)
            if week_ending_date and (latest_week is None or week_ending_date > latest_week):
                latest_week = week_ending_date

        if latest_week is None:
            return []

        return [
            record
            for record in records
            if self._extract_week_ending_date(record) == latest_week
        ]

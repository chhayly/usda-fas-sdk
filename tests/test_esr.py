from datetime import date, datetime

import pytest

from usda_fas.api.esr import ESRClient


def make_client() -> ESRClient:
    return ESRClient(api_key="test-api-key")


def test_normalize_date_value_round_trips_supported_inputs() -> None:
    assert ESRClient._normalize_date_value("2026-04-23") == "2026-04-23"
    assert ESRClient._normalize_date_value("2026-04-23T00:00:00") == "2026-04-23"
    assert ESRClient._normalize_date_value("2026-04-23 00:00:00") == "2026-04-23"
    assert ESRClient._normalize_date_value(date(2026, 4, 23)) == "2026-04-23"
    assert ESRClient._normalize_date_value(datetime(2026, 4, 23, 13, 45, 1)) == "2026-04-23"


def test_normalize_date_value_raises_for_unsupported_type() -> None:
    with pytest.raises(TypeError):
        ESRClient._normalize_date_value(123)  # type: ignore[arg-type]


def test_extract_week_ending_date_handles_missing_or_null_values() -> None:
    assert ESRClient._extract_week_ending_date({}) is None
    assert ESRClient._extract_week_ending_date({"weekEndingDate": None}) is None
    assert ESRClient._extract_week_ending_date({"weekEndingDate": ""}) is None


def test_get_esr_release_info_and_latest_market_year_cast_to_int(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_client()
    monkeypatch.setattr(
        client,
        "get_esr_data_release_dates",
        lambda: [
            {"commodityCode": 301, "marketYear": "2025"},
            {"commodityCode": 401, "marketYear": "2026"},
        ],
    )

    release_info = client.get_esr_release_info(401)

    assert release_info == {"commodityCode": 401, "marketYear": "2026"}
    assert client.get_esr_latest_market_year(401) == 2026


def test_get_esr_latest_week_ending_date_returns_none_for_empty_records(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_client()
    monkeypatch.setattr(client, "get_esr_exports", lambda *args, **kwargs: [])

    assert client.get_esr_latest_week_ending_date(401, market_year=2026) is None


def test_get_esr_exports_all_countries_uses_client_instance_cache(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_client()
    calls: list[str] = []
    expected_records = [{"weekEndingDate": "2026-04-23T00:00:00", "countryCode": 1220}]

    def fake_make_request(method: str, endpoint: str, params=None):
        calls.append(endpoint)
        return expected_records

    monkeypatch.setattr(client, "_make_request", fake_make_request)

    first = client.get_esr_exports_all_countries(401, 2026)
    second = client.get_esr_exports_all_countries(401, 2026)

    assert first == expected_records
    assert second == expected_records
    assert calls == ["/api/esr/exports/commodityCode/401/allCountries/marketYear/2026"]


def test_public_weekly_helpers_work_with_cached_responses(monkeypatch: pytest.MonkeyPatch) -> None:
    client = make_client()
    calls: list[str] = []
    records = [
        {"weekEndingDate": "2026-04-16T00:00:00", "countryCode": 1220, "weeklyExports": 1},
        {"weekEndingDate": "2026-04-23T00:00:00", "countryCode": 1220, "weeklyExports": 2},
        {"weekEndingDate": "2026-04-23T00:00:00", "countryCode": 2010, "weeklyExports": 3},
    ]

    def fake_make_request(method: str, endpoint: str, params=None):
        calls.append(endpoint)
        if endpoint == "/api/esr/datareleasedates":
            return [{"commodityCode": 401, "marketYear": 2026}]
        if endpoint == "/api/esr/exports/commodityCode/401/allCountries/marketYear/2026":
            return records
        raise AssertionError(f"Unexpected endpoint: {endpoint}")

    monkeypatch.setattr(client, "_make_request", fake_make_request)

    latest_week = client.get_esr_latest_week_ending_date(401)
    latest_rows = client.get_esr_latest_week_exports(401)
    exact_week_rows = client.get_esr_exports_for_week(401, "2026-04-23", market_year=2026)

    assert latest_week == "2026-04-23"
    assert latest_rows == exact_week_rows
    assert latest_rows == [
        {"weekEndingDate": "2026-04-23T00:00:00", "countryCode": 1220, "weeklyExports": 2},
        {"weekEndingDate": "2026-04-23T00:00:00", "countryCode": 2010, "weeklyExports": 3},
    ]
    assert calls == [
        "/api/esr/datareleasedates",
        "/api/esr/exports/commodityCode/401/allCountries/marketYear/2026",
    ]

"""
Per-country, per-year calculator data (rates, thresholds, limits, subsidies).

This package is the **single, editable source of truth** for every value that
changes annually or differs by country. Each ``<cc>_<year>.json`` file holds the
raw numbers for one country + tax year; update it once a year (or add a new
``<cc>_<year+1>.json``) without touching any calculator logic.

Money/rate values are stored as JSON **strings** and loaded as ``Decimal`` (the
repo's money-math convention). Plain counts (ages, weeks, days) are stored as
JSON numbers and kept as ``int``. The ``meta`` and ``_notes`` blocks are left as
raw text.

Usage::

    from calculators.services.data import get_rates
    sk = get_rates('SK')          # latest available SK year
    sk = get_rates('SK', 2026)    # a specific year
    sk['salary']['nczd_monthly']  # Decimal('497.23')
    sk['meta']['valid_until']     # '2026-12-31'
"""

from __future__ import annotations

import json
import re
from decimal import Decimal
from pathlib import Path
from typing import Any

_DATA_DIR = Path(__file__).resolve().parent
_DECIMAL_RE = re.compile(r'^-?\d+(\.\d+)?$')

# Keys whose sub-trees are metadata/prose and must NOT be Decimal-converted.
_RAW_SECTIONS = {'meta', '_notes'}

# Cache: (country, year) -> converted dict. Populated on first access.
_CACHE: dict[tuple[str, int], dict[str, Any]] = {}


def _to_decimal_tree(obj: Any) -> Any:
    """Recursively convert decimal-looking strings to ``Decimal``.

    JSON numbers (ints) are preserved as-is; only strings matching a plain
    decimal literal become ``Decimal``. Non-numeric strings are left untouched.
    """
    if isinstance(obj, dict):
        return {k: _to_decimal_tree(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_decimal_tree(v) for v in obj]
    if isinstance(obj, str) and _DECIMAL_RE.match(obj):
        return Decimal(obj)
    return obj


def _convert_document(raw: dict[str, Any]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for section, value in raw.items():
        if section in _RAW_SECTIONS:
            out[section] = value  # keep prose/metadata verbatim
        else:
            out[section] = _to_decimal_tree(value)
    return out


def _path_for(country: str, year: int) -> Path:
    return _DATA_DIR / f'{country.lower()}_{year}.json'


def available_years(country: str) -> list[int]:
    """Sorted list of tax years available for a country (from the data files)."""
    prefix = f'{country.lower()}_'
    years = []
    for p in _DATA_DIR.glob(f'{prefix}*.json'):
        stem = p.stem[len(prefix):]
        if stem.isdigit():
            years.append(int(stem))
    return sorted(years)


def latest_year(country: str) -> int:
    years = available_years(country)
    if not years:
        raise FileNotFoundError(f'No rate data files found for country {country!r}')
    return years[-1]


def get_rates(country: str, year: int | None = None) -> dict[str, Any]:
    """Return the rate set for ``country`` (+ ``year``, default = latest).

    Values are ``Decimal``/``int``. Result is cached and must be treated as
    read-only. Raises ``FileNotFoundError`` if no dataset exists.
    """
    country = country.upper()
    if year is None:
        year = latest_year(country)
    key = (country, year)
    if key not in _CACHE:
        path = _path_for(country, year)
        if not path.exists():
            raise FileNotFoundError(
                f'No rate data for {country} {year} (expected {path.name}). '
                f'Available years: {available_years(country) or "none"}'
            )
        with path.open(encoding='utf-8') as fh:
            _CACHE[key] = _convert_document(json.load(fh))
    return _CACHE[key]


def config_info(country: str, year: int | None = None) -> dict[str, Any]:
    """Metadata block for a country/year (version, validity, sources)."""
    return dict(get_rates(country, year).get('meta', {}))


def clear_cache() -> None:
    """Drop the in-memory cache (tests / hot-reload)."""
    _CACHE.clear()

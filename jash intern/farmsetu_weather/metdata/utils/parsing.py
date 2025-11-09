"""Parsing utilities for MetOffice summary datasets.

Typical MetOffice dataset layout example (UK Tmax):

# Some introductory comment lines
# Another comment line
Year  JAN  FEB  MAR  APR  MAY  JUN  JUL  AUG  SEP  OCT  NOV  DEC  WIN  SPR  SUM  AUT  ANN
1884   5.7  6.1  7.3  8.9  11.5  14.2  15.9  15.5  13.3  10.7   7.8   6.0   6.5   9.2  15.2  10.6  10.4
...

We need to:
- Skip leading comment lines (start with '#') or blank lines.
- Detect header line containing columns (starting with 'Year').
- Parse subsequent data lines until blank line or EOF.

Columns beyond 'Year' are stored individually with their column name.
We treat all numeric cells; missing values represented by '---' or similar become None and are skipped.

The dataset URL conveys parameter and region. Example:
https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt
Parameter: 'Tmax' (segment preceding 'date')
Region: 'UK' (filename without extension)

This module exposes high-level helper functions for:
- inferring parameter & region
- extracting columns
- iterating value rows
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Tuple
import re
from pathlib import PurePosixPath

COMMENT_PREFIXES = ("#",)
MISSING_VALUE_TOKENS = {"---", "", "NA", "N/A"}

HEADER_YEAR_PATTERN = re.compile(r"^Year\b", re.IGNORECASE)
SPACE_SPLIT_PATTERN = re.compile(r"\s+")


@dataclass(frozen=True)
class ParsedHeader:
    columns: List[str]  # includes Year in position 0


@dataclass(frozen=True)
class ParsedRow:
    year: int
    values: List[Tuple[str, float]]  # (column_name, value)


def infer_parameter_and_region(url: str) -> Tuple[str, str]:
    """Infer (parameter, region) from a MetOffice dataset URL.

    Expected pattern: .../datasets/<Parameter>/date/<Region>.txt
    We'll parse path segments to capture this reliably.
    """
    path = PurePosixPath(re.sub(r"https?://[^/]+/", "", url))  # strip scheme/host for simplicity
    parts = path.parts
    # Find 'datasets' then take the next segment as parameter, then look for 'date' and next filename as region
    try:
        datasets_idx = parts.index("datasets")
        parameter = parts[datasets_idx + 1]
    except (ValueError, IndexError):
        raise ValueError(f"Unable to infer parameter from URL: {url}")

    # Region from final filename (without extension)
    region = path.stem
    if not region:
        raise ValueError(f"Unable to infer region from URL: {url}")
    return parameter, region


def iter_non_comment_lines(text: str) -> Iterable[str]:
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line.startswith(COMMENT_PREFIXES):
            continue
        yield line


def parse_header(lines: Iterable[str]) -> ParsedHeader:
    """Find and parse the header line returning column names.

    Consumes lines until a header line is found; returns columns list.
    """
    for line in lines:
        if HEADER_YEAR_PATTERN.search(line):
            columns = SPACE_SPLIT_PATTERN.split(line.strip())
            return ParsedHeader(columns=columns)
    raise ValueError("Header line starting with 'Year' not found in dataset.")


def parse_data_rows(text: str, header: ParsedHeader) -> Iterable[ParsedRow]:
    header_set = set(header.columns)
    for line in iter_non_comment_lines(text):
        if HEADER_YEAR_PATTERN.search(line):  # skip header itself if re-encountered
            continue
        tokens = SPACE_SPLIT_PATTERN.split(line.strip())
        if not tokens:
            continue
        year_token = tokens[0]
        if not year_token.isdigit():  # skip lines not starting with a year
            continue
        year = int(year_token)
        row_values: List[Tuple[str, float]] = []
        for col_name, raw_val in zip(header.columns[1:], tokens[1:]):
            if col_name not in header_set:
                continue
            if raw_val in MISSING_VALUE_TOKENS:
                continue
            try:
                val = float(raw_val)
            except ValueError:
                continue
            row_values.append((col_name, val))
        yield ParsedRow(year=year, values=row_values)


def parse_full(text: str) -> Tuple[ParsedHeader, List[ParsedRow]]:
    """Convenience function returning header and all parsed rows."""
    # We need to iterate lines twice (once for header, again for rows). So store filtered lines.
    non_comment_lines = list(iter_non_comment_lines(text))
    header = parse_header(non_comment_lines)
    # Build rows from original full text (to preserve order) - we could also use filtered.
    rows = list(parse_data_rows(text, header))
    return header, rows

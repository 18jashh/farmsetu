from __future__ import annotations

import logging
from typing import List

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
import requests

from metdata.models import DataRecord
from metdata.utils.parsing import (
    infer_parameter_and_region,
    parse_full,
)

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = (
        "Import summarised weather data from a UK MetOffice dataset URL and store "
        "as normalized DataRecord rows."
    )

    def add_arguments(self, parser) -> None:  # type: ignore[override]
        parser.add_argument(
            "url",
            type=str,
            help=(
                "MetOffice dataset URL, e.g. "
                "https://www.metoffice.gov.uk/pub/data/weather/uk/climate/datasets/Tmax/date/UK.txt"
            ),
        )
        parser.add_argument(
            "--timeout",
            type=float,
            default=30.0,
            help="HTTP request timeout in seconds (default: 30)",
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and report counts without writing to the database.",
        )
        parser.add_argument(
            "--chunk-size",
            type=int,
            default=1000,
            help="Bulk insert chunk size (default: 1000).",
        )

    def handle(self, *args, **options) -> None:  # type: ignore[override]
        url: str = options["url"]
        timeout: float = options["timeout"]
        dry_run: bool = options["dry_run"]
        chunk_size: int = options["chunk_size"]

        try:
            parameter, region = infer_parameter_and_region(url)
        except ValueError as e:
            raise CommandError(str(e))

        self.stdout.write(self.style.NOTICE(f"Fetching: {url}"))
        try:
            resp = requests.get(url, timeout=timeout)
            resp.raise_for_status()
        except Exception as e:  # noqa: BLE001
            raise CommandError(f"Failed to download dataset: {e}")

        text = resp.text
        try:
            header, rows = parse_full(text)
        except Exception as e:  # noqa: BLE001
            raise CommandError(f"Failed to parse dataset text: {e}")

        total_cells = sum(len(r.values) for r in rows)
        self.stdout.write(self.style.NOTICE(
            f"Parsed header with {len(header.columns)-1} columns; years={len(rows)}; cells={total_cells}"
        ))

        if dry_run:
            self.stdout.write(self.style.SUCCESS("Dry run complete; no data written."))
            return

        to_create: List[DataRecord] = []
        for row in rows:
            for col_name, val in row.values:
                to_create.append(
                    DataRecord(
                        year=row.year,
                        parameter=parameter,
                        region=region,
                        column_name=col_name,
                        value=val,
                        source_url=url,
                    )
                )

        created_total = 0
        with transaction.atomic():
            # Insert in chunks; ignore conflicts per unique constraint for idempotency.
            for i in range(0, len(to_create), chunk_size):
                chunk = to_create[i : i + chunk_size]
                DataRecord.objects.bulk_create(chunk, ignore_conflicts=True, batch_size=chunk_size)
                created_total += len(chunk)

        # We cannot know exact number skipped due to conflicts without extra queries.
        self.stdout.write(
            self.style.SUCCESS(
                f"Import attempted {len(to_create)} records (inserts attempted in chunks)."
            )
        )
        self.stdout.write(self.style.SUCCESS(
            f"Done. Parameter={parameter} Region={region} Years={len(rows)} Columns={len(header.columns)-1}"
        ))

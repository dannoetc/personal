from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable

from app.services.reporting import DailyReport, WeeklyReport

CSV_HEADERS = [
    "date",
    "session_count",
    "total_active_seconds",
    "total_raw_seconds",
    "daily_pace_label",
    "daily_pace_emoji",
]


def _total_raw_seconds(session_summaries) -> float:
    return sum(s.total_raw_seconds for s in session_summaries)


def _daily_report_row(report: DailyReport) -> list[str | float]:
    return [
        report.day_summary.date.date().isoformat(),
        report.day_summary.total_sessions,
        float(report.day_summary.total_active_seconds),
        float(_total_raw_seconds(report.session_summaries)),
        report.day_summary.daily_pace_label,
        report.day_summary.daily_pace_emoji,
    ]


def _rows_to_csv(rows: Iterable[Iterable[str | float]]) -> str:
    buffer = StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_HEADERS)
    for row in rows:
        writer.writerow(row)
    return buffer.getvalue()


def daily_report_to_csv(report: DailyReport) -> str:
    """Render a DailyReport into a CSV string."""

    return _rows_to_csv([_daily_report_row(report)])


def weekly_report_to_csv(report: WeeklyReport) -> str:
    """Render a WeeklyReport into a CSV string including a totals row."""

    rows = [_daily_report_row(r) for r in report.daily_reports]

    total_raw_seconds = sum(_total_raw_seconds(r.session_summaries) for r in report.daily_reports)

    rows.append(
        [
            "TOTAL",
            report.totals.get("total_sessions", 0),
            float(report.totals.get("total_active_seconds", 0.0)),
            float(total_raw_seconds),
            "",
            "",
        ]
    )

    return _rows_to_csv(rows)

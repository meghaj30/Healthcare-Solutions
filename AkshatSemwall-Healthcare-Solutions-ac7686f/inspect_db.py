"""Quick utility to dump a preview of data from hospital.db."""
from __future__ import annotations

import json
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).with_name("hospital.db")


def main() -> None:
    if not DB_PATH.exists():
        print(f"Database file not found at {DB_PATH}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [row[0] for row in cur.fetchall() if not row[0].startswith('sqlite_')]

    snapshot = {}
    for table in tables:
        cur.execute(f"SELECT * FROM {table} LIMIT 5")
        rows = [dict(row) for row in cur.fetchall()]
        snapshot[table] = {
            "row_count": cur.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0],
            "sample_rows": rows,
        }

    print(json.dumps(snapshot, indent=2, default=str))


if __name__ == "__main__":
    main()


"""Manage dairy milk collection records and farmer summaries."""

import hashlib
import sqlite3


def record_milk(conn, farmer, litres, fat, day):
    """Record a farmer's milk collection."""
    conn.execute(
        """
        INSERT INTO milk (farmer, litres, fat, day)
        VALUES (?, ?, ?, ?)
        """,
        (farmer, litres, fat, day),
    )
    conn.commit()


def farmer_token(farmer):
    """Generate a SHA-256 hash for a farmer name."""
    return hashlib.sha256(farmer.encode("utf-8")).hexdigest()


def daily_total(conn, day):
    """Calculate the total litres collected on a given day."""
    rows = conn.execute(
        "SELECT litres FROM milk WHERE day = ?", (day,)
    ).fetchall()
    total = sum(row[0] for row in rows)
    return f"Total: {total:.1f} litres"


def top_farmer(conn):
    """Return the farmer with the highest total milk collection."""
    row = conn.execute(
        """
        SELECT farmer, SUM(litres)
        FROM milk
        GROUP BY farmer
        ORDER BY SUM(litres) DESC
        LIMIT 1
        """
    ).fetchone()
    return row[0] if row else None


def print_slip(farmer):
    """Display a milk collection slip message."""
    print(f"Printing slip for {farmer}")


def low_fat(conn):
    """Return farmers whose milk fat is below 3.5 or missing."""
    rows = conn.execute(
        "SELECT farmer, fat FROM milk"
    ).fetchall()
    return [
        farmer for farmer, fat in rows
        if fat is None or fat < 3.5
    ]


def main():
    """Run the dairy collection demonstration."""
    conn = sqlite3.connect(":memory:")
    conn.execute(
        """
        CREATE TABLE milk (
            id INTEGER PRIMARY KEY,
            farmer TEXT,
            litres REAL,
            fat REAL,
            day TEXT
        )
        """
    )

    try:
        record_milk(conn, "Gopal", 12.5, 4.1, "Mon")
        record_milk(conn, "Lata", 20.0, 3.2, "Mon")
        print(daily_total(conn, "Mon"))
        print("Top farmer:", top_farmer(conn))
        print("Low-fat farmers:", low_fat(conn))
        print_slip("Gopal")
        print("Farmer token:", farmer_token("Lata"))
    finally:
        conn.close()


if __name__ == "__main__":
    main()

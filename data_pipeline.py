
import os
import csv

INPUT_FILE = "data/raw_data.csv"
OUTPUT_FILE = "data/processed_data.csv"

REQUIRED_COLUMNS = [
    "ward_id",
    "week",
    "rainfall_mm",
    "avg_temp_C",
    "relative_humidity_pct",
    "water_logging_risk_index",
    "population_density_sqkm",
    "sanitation_score"
]

NUMERIC_COLUMNS = [
    "week",
    "rainfall_mm",
    "avg_temp_C",
    "relative_humidity_pct",
    "water_logging_risk_index",
    "population_density_sqkm",
    "sanitation_score"
]


def create_data_pipeline():

    if not os.path.exists(INPUT_FILE):
        print("Error: Dataset not found!")
        return

    with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            print("Error: CSV file is empty!")
            return

        missing = [
            col for col in REQUIRED_COLUMNS
            if col not in reader.fieldnames
        ]

        if missing:
            print("Missing columns:", missing)
            return

        rows = list(reader)

    if not rows:
        print("Error: Dataset has no records!")
        return

    # Validate and clean data

    for row_number, row in enumerate(rows, start=2):

        if not row["ward_id"].strip():
            print("Error: Missing ward_id at row", row_number)
            return

        for column in NUMERIC_COLUMNS:

            try:
                value = float(row[column])

                if not __import__("math").isfinite(value):
                    raise ValueError

                row[column] = value

            except (ValueError, TypeError):
                print(
                    "Invalid or missing value:",
                    column,
                    "at row",
                    row_number
                )
                return

    # Check duplicate ward and week records

    seen = set()

    for row in rows:
        key = (row["ward_id"], row["week"])

        if key in seen:
            print("Error: Duplicate ward and week record:", key)
            return

        seen.add(key)

    # Sort records

    rows.sort(
        key=lambda row: (
            row["ward_id"],
            row["week"]
        )
    )

    # Save processed data

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=REQUIRED_COLUMNS
        )

        writer.writeheader()
        writer.writerows(rows)

    print("Data Pipeline completed successfully!")
    print("Total records processed:", len(rows))
    print("Output saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    create_data_pipeline()


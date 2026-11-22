

import csv
import os

INPUT_FILE = "data/processed_data.csv"
OUTPUT_FILE = "data/feature_data.csv"


def create_features():

    if not os.path.exists(INPUT_FILE):
        print("Error: Processed dataset not found!")
        print("Please run data_pipeline.py first.")
        return

    with open(INPUT_FILE, "r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if not reader.fieldnames:
            print("Error: Processed dataset is empty!")
            return

        rows = list(reader)
        original_columns = list(reader.fieldnames)

    if not rows:
        print("Error: Dataset has no records!")
        return

    rows.sort(key=lambda row: (
        row["ward_id"],
        float(row["week"])
    ))

    history = {}

    for row in rows:

        ward = row["ward_id"]

        if ward not in history:
            history[ward] = []

        previous = history[ward]

        for lag in [1, 2, 3, 4]:

            if len(previous) >= lag:
                row[f"rainfall_lag_{lag}"] = previous[-lag]
            else:
                row[f"rainfall_lag_{lag}"] = ""

        previous.append(float(row["rainfall_mm"]))

    feature_columns = [
        f"rainfall_lag_{lag}" for lag in [1, 2, 3, 4]
    ]

    fieldnames = original_columns + feature_columns

    os.makedirs("data", exist_ok=True)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as file:

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("Feature Engineering completed successfully!")
    print("Total records:", len(rows))
    print("New features:", feature_columns)
    print("Output saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    create_features()

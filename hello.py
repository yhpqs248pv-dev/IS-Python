import csv
from datetime import date

CSV_FILE = "workouts.csv"

def ensure_csv_exists():
    try:
        with open(CSV_FILE, "r", newline="") as f:
            pass
    except FileNotFoundError:
        with open(CSV_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "exercise", "sets", "reps"])

def append_log(log_date, exercise, sets, reps):
    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([log_date, exercise, sets, reps])

def print_recent(limit=10):
    try:
        with open(CSV_FILE, "r", newline="") as f:
            rows = list(csv.reader(f))
    except FileNotFoundError:
        print("No logs yet.")
        return

    data = rows[1:]  # skip header
    if not data:
        print("No logs yet.")
        return

    print("\nRecent logs:")
    for r in data[-limit:][::-1]:
        d, ex, sets, reps = r
        print(f"- {d} — {ex}: {sets} x {reps}")

def main():
    ensure_csv_exists()
    print("Fitness Tracker v0.3 (CSV)")
    print("Type 'quit' to exit, 'recent' to view recent logs.\n")

    today = str(date.today())

    while True:
        exercise = input("Exercise: ").strip()
        if exercise.lower() == "quit":
            break
        if exercise.lower() == "recent":
            print_recent()
            print()
            continue

        sets = input("Sets: ").strip()
        reps = input("Reps: ").strip()

        append_log(today, exercise, sets, reps)
        print("Saved.\n")

    print("Done.")

if __name__ == "__main__":
    main()

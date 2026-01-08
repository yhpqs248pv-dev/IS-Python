from datetime import date
from db import init_db, get_conn

def add_log():
    log_date = input("Date (YYYY-MM-DD) [enter = today]: ").strip() or str(date.today())
    exercise = input("Exercise: ").strip()
    sets = int(input("Sets: ").strip())
    reps = int(input("Reps: ").strip())

    weight_raw = input("Weight (optional): ").strip()
    weight = float(weight_raw) if weight_raw else None

    notes = input("Notes (optional): ").strip() or None

    with get_conn() as conn:
        conn.execute(
            "INSERT INTO workout_logs (date, exercise, sets, reps, weight, notes) VALUES (?, ?, ?, ?, ?, ?)",
            (log_date, exercise, sets, reps, weight, notes)
        )
    print("✅ Saved.\n")

def recent_logs(limit=10):
    with get_conn() as conn:
        rows = conn.execute(
            """SELECT date, exercise, sets, reps,
                      COALESCE(weight, ''), COALESCE(notes,'')
               FROM workout_logs
               ORDER BY id DESC
               LIMIT ?""",
            (limit,)
        ).fetchall()

    if not rows:
        print("No logs yet.\n")
        return

    for d, ex, sets, reps, wt, notes in rows:
        wt_part = f" @ {wt}" if wt != "" else ""
        notes_part = f" | {notes}" if notes else ""
        print(f"{d} — {ex}: {sets}x{reps}{wt_part}{notes_part}")
    print()

def best_weight():
    ex = input("Exercise name: ").strip()
    with get_conn() as conn:
        row = conn.execute(
            """SELECT MAX(weight)
               FROM workout_logs
               WHERE LOWER(exercise)=LOWER(?) AND weight IS NOT NULL""",
            (ex,)
        ).fetchone()
    best = row[0]
    print("No weighted entries yet.\n" if best is None else f"🏆 Best for {ex}: {best}\n")

def main():
    init_db()
    while True:
        print("Fitness Tracker (SQLite)")
        print("1) Add log")
        print("2) View recent logs")
        print("3) Best weight for an exercise")
        print("4) Quit")
        choice = input("> ").strip()

        if choice == "1":
            add_log()
        elif choice == "2":
            recent_logs()
        elif choice == "3":
            best_weight()
        elif choice == "4":
            break
        else:
            print("Pick 1–4.\n")

if __name__ == "__main__":
    main()

print("Fitness Tracker v0.2")
print("Type 'quit' to exit\n")

logs = []

while True:
    exercise = input("Exercise: ").strip()
    if exercise.lower() == "quit":
        break

    sets = input("Sets: ").strip()
    reps = input("Reps: ").strip()

    logs.append({
        "exercise": exercise,
        "sets": sets,
        "reps": reps
    })

    print("Logged.\n")

print("\nWorkout Summary:")
for log in logs:
    print(f"- {log['exercise']}: {log['sets']} x {log['reps']}")
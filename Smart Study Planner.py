# Smart Study Planner

FILE_NAME = "study_log.txt"


def classify_session(duration):
    """Classify a study session according to its duration."""
    if duration < 30:
        return "short"
    elif duration <= 90:
        return "medium"
    else:
        return "long"


def add_session(sessions):
    """Add a session to the sessions list."""

    subject = input("Enter subject name: ").strip()
    topic = input("Enter topic covered: ").strip()
    date = input("Enter date/day label: ").strip()

    while True:
        try:
            duration = int(input("Enter duration in minutes: "))
            if duration > 0:
                break
            else:
                print("Error: duration must be greater than 0.")
        except ValueError:
            print("Error: please enter a valid number.")

    # Replace the "|" delimiter so it doesn't break the save file format
    subject = subject.replace("|", "/")
    topic = topic.replace("|", "/")
    date = date.replace("|", "/")

    session = {
        "subject": subject,
        "topic": topic,
        "date": date,
        "duration": duration
    }

    sessions.append(session)
    print("Study session added successfully.")


def view_sessions(sessions):
    """Display all recorded study sessions."""

    if not sessions:
        print("\nNo study sessions recorded.")
        return

    print("\n" + "=" * 80)
    print("ALL STUDY SESSIONS")
    print("=" * 80)

    print(
        f"{'Subject':<20}"
        f"{'Topic':<25}"
        f"{'Date/Day':<15}"
        f"{'Duration':<12}"
        f"{'Class':<10}"
    )
    print("-" * 80)

    for session in sessions:
        classification = classify_session(session["duration"])

        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12}"
            f"{classification:<10}"
        )

    print("-" * 80)

    total_minutes = sum(session["duration"] for session in sessions)
    print(
        f"Total time studied: {total_minutes} minutes "
        f"({total_minutes / 60:.2f} hours)"
    )


def search_by_subject(sessions, subject):
    """Search and display sessions matching a given subject."""

    matches = [
        session for session in sessions
        if session["subject"].lower() == subject.lower()
    ]

    if not matches:
        print(f"\nNo sessions found for subject '{subject}'.")
        return

    print("\n" + "=" * 80)
    print(f"SESSIONS FOR SUBJECT: {subject}")
    print("=" * 80)

    for session in matches:
        classification = classify_session(session["duration"])
        print(
            f"{session['subject']:<20}"
            f"{session['topic']:<25}"
            f"{session['date']:<15}"
            f"{session['duration']:<12}"
            f"{classification:<10}"
        )

    print("-" * 80)
    total = sum(session["duration"] for session in matches)
    print(f"Total time studied for {subject}: {total} minutes ({total / 60:.2f} hours)")


def study_statistics(sessions):
    """Calculate and display study statistics."""

    if not sessions:
        print("\nNo study sessions available for statistics.")
        return

    # Total minutes -> hours
    total_minutes = sum(session["duration"] for session in sessions)
    total_hours = total_minutes / 60

    print("\n" + "=" * 60)
    print("STUDY STATISTICS")
    print("=" * 60)

    print(f"Total hours studied overall: {total_hours:.2f} hours")

    # Build subject totals
    subject_totals = {}
    for session in sessions:
        subject_totals[session["subject"]] = (
            subject_totals.get(session["subject"], 0) + session["duration"]
        )

    # Subject with the least study time
    weakest_subject = min(subject_totals, key=subject_totals.get)
    print(
        f"\nSubject with the least study time: {weakest_subject} "
        f"({subject_totals[weakest_subject] / 60:.2f} hours)"
    )

    # Longest individual session
    longest_session = max(sessions, key=lambda session: session["duration"])
    print("\nLongest study session:")
    print(f"Subject: {longest_session['subject']}")
    print(f"Topic: {longest_session['topic']}")
    print(f"Duration: {longest_session['duration']} minutes")

    print("=" * 60)


def save_sessions(sessions):
    """Save all study sessions to the log file."""

    with open(FILE_NAME, "w") as file:
        for session in sessions:
            file.write(
                f"{session['subject']}|"
                f"{session['topic']}|"
                f"{session['date']}|"
                f"{session['duration']}\n"
            )

    print("\nStudy sessions saved successfully.")


def load_sessions():
    """Load previously saved sessions from the log file."""

    sessions = []

    try:
        with open(FILE_NAME, "r") as file:
            for line in file:
                line = line.strip()
                if not line:
                    continue
                parts = line.split("|")
                if len(parts) == 4:
                    session = {
                        "subject": parts[0],
                        "topic": parts[1],
                        "date": parts[2],
                        "duration": float(parts[3])
                    }
                    sessions.append(session)
    except FileNotFoundError:
        print("No previous study log found. Starting with an empty planner.")

    return sessions


def main():
    """Display the menu and control the smart study planner."""

    sessions = load_sessions()

    while True:
        print("=" * 40)
        print("   SMART STUDY PLANNER")
        print("=" * 40)
        print("1. Add a study session")
        print("2. View all sessions")
        print("3. Search sessions by subject")
        print("4. View statistics")
        print("5. Save and exit")
        print("=" * 40)

        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            add_session(sessions)

        elif choice == "2":
            view_sessions(sessions)

        elif choice == "3":
            subject = input("Enter subject to search: ").strip()
            search_by_subject(sessions, subject)

        elif choice == "4":
            study_statistics(sessions)

        elif choice == "5":
            save_sessions(sessions)
            print("Thank you for using Smart Study Planner.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()
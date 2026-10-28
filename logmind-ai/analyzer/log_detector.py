from pathlib import Path
from collections import Counter


def detect_repeated_errors(file_path):
    log_file = Path(file_path)

    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    error_messages = []

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if " ERROR " in line:
                parts = line.split(" ERROR ", 1)
                error_message = parts[1].strip()
                error_messages.append(error_message)

    error_counts = Counter(error_messages)

    repeated_errors = {
        message: count
        for message, count in error_counts.items()
        if count > 1
    }

    return {
        "total_errors": len(error_messages),
        "unique_errors": len(error_counts),
        "error_messages": list(error_counts.keys()),
        "error_counts": dict(error_counts),
        "repeated_errors": repeated_errors,
    }


if __name__ == "__main__":
    log_path = (
        Path(__file__).resolve().parents[1]
        / "sample_logs"
        / "application.log"
    )

    results = detect_repeated_errors(log_path)

    print("\n========== LOGMIND DETECTION ==========")
    print(f"Total Errors: {results['total_errors']}")
    print(f"Unique Errors: {results['unique_errors']}")

    print("\nAll Unique Errors:")
    for message in results["error_messages"]:
        print(f"- {message} ({results['error_counts'][message]} occurrences)")

    print("\nRepeated Errors:")
    if results["repeated_errors"]:
        for message, count in results["repeated_errors"].items():
            print(f"- {message} ({count} occurrences)")
    else:
        print("No repeated errors found.")

    print("=======================================")
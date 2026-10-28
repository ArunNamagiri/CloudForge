from pathlib import Path


def analyze_logs(file_path):
    log_file = Path(file_path)

    if not log_file.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    results = {
        "total": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "UNKNOWN": 0,
    }

    with log_file.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            results["total"] += 1

            if " ERROR " in line:
                results["ERROR"] += 1
            elif " WARNING " in line:
                results["WARNING"] += 1
            elif " INFO " in line:
                results["INFO"] += 1
            else:
                results["UNKNOWN"] += 1

    return results


if __name__ == "__main__":
    log_path = (
        Path(__file__).resolve().parents[1]
        / "sample_logs"
        / "application.log"
    )

    summary = analyze_logs(log_path)

    print("\n========== LOGMIND AI ==========")
    print(f"Total log entries : {summary['total']}")
    print(f"Info messages     : {summary['INFO']}")
    print(f"Warnings          : {summary['WARNING']}")
    print(f"Errors            : {summary['ERROR']}")
    print(f"Unknown entries   : {summary['UNKNOWN']}")
    print("================================")
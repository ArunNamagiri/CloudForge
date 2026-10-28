from pathlib import Path

from analyzer.ai_analyzer import analyze_errors
from analyzer.log_detector import detect_repeated_errors


# Define the location of the sample application log.
PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "sample_logs" / "application.log"


def main():
    print("\n========== LOGMIND AI ==========")
    print("Starting log analysis...")

    try:
        # Step 1: Detect errors in the log file.
        results = detect_repeated_errors(LOG_FILE)

        print("\n--- Log Detection Results ---")
        print(f"Total errors: {results['total_errors']}")
        print(f"Unique errors: {results['unique_errors']}")

        repeated_errors = results["repeated_errors"]

        if repeated_errors:
            print("\nRepeated errors:")
            for message, count in repeated_errors.items():
                print(f"- {message} ({count} occurrences)")

        # Step 2: Collect error messages for AI analysis.
        # Analyze unique errors to avoid sending duplicates.
        error_messages = results["error_messages"]
        if not error_messages:
            print("\nNo repeated errors found.")
            print("Checking whether any errors need AI analysis...")
            # Analyze errors even when none are repeated.
            with LOG_FILE.open("r", encoding="utf-8") as file:
                for line in file:
                    if " ERROR " in line:
                        error_message = line.split(" ERROR ", 1)[1].strip()
                        if error_message not in error_messages:
                            error_messages.append(error_message)

        # Step 3: Send errors to Gemini.
        if error_messages:
            print("\n--- AI Troubleshooting Analysis ---")
            analysis = analyze_errors(error_messages)
            print(analysis)
        else:
            print("\nNo errors detected. AI analysis is not required.")

    except FileNotFoundError as error:
        print(f"\nLog file error: {error}")

    except Exception as error:
        print(f"\nAnalysis failed: {error}")

    print("\n========== ANALYSIS COMPLETE ==========")


if __name__ == "__main__":
    main()

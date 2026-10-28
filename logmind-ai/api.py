from pathlib import Path

from flask import Flask, jsonify
from analyzer.log_detector import detect_repeated_errors
from analyzer.ai_analyzer import analyze_errors


app = Flask(__name__)

PROJECT_DIR = Path(__file__).resolve().parent
LOG_FILE = PROJECT_DIR / "sample_logs" / "application.log"


@app.get("/")
def home():
    return jsonify({
        "application": "LogMind AI",
        "version": "1.0.0",
        "status": "running",
        "endpoints": [
            "/health",
            "/api/v1/analyze",
        ],
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "healthy",
    })


@app.get("/api/v1/analyze")
def analyze_logs():
    try:
        # Detect errors in the application log.
        results = detect_repeated_errors(LOG_FILE)

        # Send all unique error messages to the AI.
        error_messages = results["error_messages"]

        if error_messages:
            ai_analysis = analyze_errors(error_messages)
        else:
            ai_analysis = "No errors detected. AI analysis is not required."

        return jsonify({
            "status": "success",
            "total_errors": results["total_errors"],
            "unique_errors": results["unique_errors"],
            "error_counts": results["error_counts"],
            "repeated_errors": results["repeated_errors"],
            "ai_analysis": ai_analysis,
        })

    except FileNotFoundError as error:
        return jsonify({
            "status": "error",
            "message": str(error),
        }), 404

    except Exception:
        app.logger.exception("Log analysis failed")

        return jsonify({
            "status": "error",
            "message": "Log analysis failed. Check the server logs.",
        }), 502

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002, debug=False)
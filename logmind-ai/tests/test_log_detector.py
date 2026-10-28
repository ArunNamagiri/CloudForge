from analyzer.log_detector import detect_repeated_errors


def test_detects_repeated_errors(tmp_path):
    log_file = tmp_path / "application.log"
    log_file.write_text(
        "2026-10-27 10:15:40 ERROR Database connection failed\n"
        "2026-10-27 10:15:41 ERROR Database connection failed\n"
        "2026-10-27 10:15:50 ERROR Database connection timeout\n",
        encoding="utf-8",
    )

    results = detect_repeated_errors(log_file)

    assert results["total_errors"] == 3
    assert results["unique_errors"] == 2
    assert results["error_counts"]["Database connection failed"] == 2
    assert results["error_counts"]["Database connection timeout"] == 1
    assert results["repeated_errors"]["Database connection failed"] == 2


def test_no_errors(tmp_path):
    log_file = tmp_path / "application.log"
    log_file.write_text(
        "2026-10-27 10:15:30 INFO Application started\n",
        encoding="utf-8",
    )

    results = detect_repeated_errors(log_file)

    assert results["total_errors"] == 0
    assert results["unique_errors"] == 0
    assert results["error_messages"] == []
    assert results["repeated_errors"] == {}


def test_missing_log_file(tmp_path):
    import pytest

    with pytest.raises(FileNotFoundError):
        detect_repeated_errors(tmp_path / "missing.log")


def test_multiple_unique_errors(tmp_path):
    log_file = tmp_path / "application.log"
    log_file.write_text(
        "2026-10-27 10:15:40 ERROR Database connection failed\n"
        "2026-10-27 10:15:50 ERROR Database connection timeout\n"
        "2026-10-27 10:16:00 ERROR Authentication failed\n",
        encoding="utf-8",
    )

    results = detect_repeated_errors(log_file)

    assert results["total_errors"] == 3
    assert results["unique_errors"] == 3
    assert len(results["error_messages"]) == 3
    assert results["repeated_errors"] == {}
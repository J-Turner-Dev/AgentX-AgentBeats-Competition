"""
Compare test results across different runs.
Useful for tracking improvements.
"""

import json
from pathlib import Path
from datetime import datetime


def load_test_results(filename: str) -> dict:
    """Load test results from JSON file"""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        return None


def compare_results(file1: str, file2: str):
    """Compare two test result files"""

    print("\n" + "=" * 60)
    print("COMPARING TEST RESULTS")
    print("=" * 60)

    results1 = load_test_results(file1)
    results2 = load_test_results(file2)

    if not results1 or not results2:
        print("Error loading result files")
        return

    # Extract metrics
    metrics1 = results1["summary"]["metrics"]
    metrics2 = results2["summary"]["metrics"]

    print(
        f"\nRun 1: {results1['summary']['suite_name']} - {results1['summary']['timestamp']}"
    )
    print(
        f"Run 2: {results2['summary']['suite_name']} - {results2['summary']['timestamp']}"
    )

    print(f"\n{'=' * 60}")
    print("METRIC COMPARISON")
    print(f"{'=' * 60}")

    metrics_to_compare = [
        ("exact_match_rate", "Exact Match Rate", "%"),
        ("average_accuracy_score", "Average Accuracy", "%"),
        ("average_confidence", "Average Confidence", "%"),
        ("average_time_seconds", "Average Time", "s"),
    ]

    for key, label, unit in metrics_to_compare:
        val1 = metrics1.get(key, 0)
        val2 = metrics2.get(key, 0)

        if unit == "%":
            val1_display = f"{val1 * 100:.1f}%"
            val2_display = f"{val2 * 100:.1f}%"
            diff = (val2 - val1) * 100
            diff_display = f"{diff:+.1f}%"
        else:
            val1_display = f"{val1:.1f}{unit}"
            val2_display = f"{val2:.1f}{unit}"
            diff = val2 - val1
            diff_display = f"{diff:+.1f}{unit}"

        # Determine if improvement
        if key == "average_time_seconds":
            improved = diff < 0  # Lower is better for time
        else:
            improved = diff > 0  # Higher is better for accuracy

        icon = "↑" if improved else ("↓" if diff != 0 else "→")

        print(f"\n{label}:")
        print(f"  Run 1: {val1_display}")
        print(f"  Run 2: {val2_display}")
        print(f"  Change: {diff_display} {icon}")

    print(f"\n{'=' * 60}")


def list_available_results():
    """List all available result files"""

    data_dir = Path("../data")
    result_files = list(data_dir.glob("test_results_*.json"))

    if not result_files:
        print("No result files found in ../data/")
        return []

    print("\nAvailable result files:")
    for i, f in enumerate(result_files, 1):
        print(f"  {i}. {f.name}")

    return result_files


def main():
    """Interactive comparison tool"""

    files = list_available_results()

    if len(files) < 2:
        print("\nNeed at least 2 result files to compare")
        return

    try:
        idx1 = int(input("\nSelect first file (number): ")) - 1
        idx2 = int(input("Select second file (number): ")) - 1

        if 0 <= idx1 < len(files) and 0 <= idx2 < len(files):
            compare_results(str(files[idx1]), str(files[idx2]))
        else:
            print("Invalid selection")
    except ValueError:
        print("Invalid input")


if __name__ == "__main__":
    main()

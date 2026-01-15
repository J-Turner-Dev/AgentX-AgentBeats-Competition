"""
Comprehensive test runner with detailed metrics.
This will become the foundation of your green agent!
"""

import sys
import json
import time
from datetime import datetime
from pathlib import Path
from collections import Counter

sys.path.append("../PurpleAgent")

from purple_agent import SentimentAgent
from test_topics import TEST_TOPICS, QUICK_TEST, STANDARD_TEST, FULL_TEST
from ground_truth import get_ground_truth, calculate_accuracy


class ComprehensiveTestRunner:
    """
    Advanced test runner that evaluates agent performance.
    This is a preview of your green agent functionality.
    """

    def __init__(self, agent: SentimentAgent):
        self.agent = agent
        self.results = []
        self.start_time = None
        self.end_time = None

    def run_single_test(self, test_case: dict) -> dict:
        """Run agent on a single test case with detailed metrics"""

        topic = test_case["topic"]
        expected = test_case["expected_sentiment"]
        category = test_case["category"]
        difficulty = test_case["difficulty"]

        start_time = time.time()

        try:
            # Run agent
            report = self.agent.analyze_topic(topic)

            elapsed = time.time() - start_time

            # Calculate accuracy using ground truth
            accuracy = calculate_accuracy(report.overall_sentiment, topic)

            # Get ground truth for comparison
            gt = get_ground_truth(topic)

            # Build result
            result = {
                "topic": topic,
                "category": category,
                "difficulty": difficulty,
                "expected_sentiment": expected,
                "actual_sentiment": report.overall_sentiment,
                "confidence": report.confidence,
                "sources_analyzed": report.sources_analyzed,
                "accuracy_score": accuracy,
                "exact_match": (report.overall_sentiment == expected),
                "time_seconds": elapsed,
                "success": True,
                "breakdown": {
                    "positive": report.positive_count,
                    "negative": report.negative_count,
                    "neutral": report.neutral_count,
                    "mixed": report.mixed_count,
                },
                "summary": report.summary,
                "key_findings": report.key_findings,
                "ground_truth_sentiment": gt.get("verified_sentiment", "unknown"),
                "ground_truth_confidence": gt.get("confidence", 0.0),
                "timestamp": str(datetime.now()),
            }

            return result

        except Exception as e:
            # Handle failures gracefully
            return {
                "topic": topic,
                "category": category,
                "difficulty": difficulty,
                "expected_sentiment": expected,
                "success": False,
                "error": str(e),
                "time_seconds": time.time() - start_time,
                "accuracy_score": 0.0,
                "timestamp": str(datetime.now()),
            }

    def run_test_suite(self, test_suite: list, suite_name: str = "Test Suite"):
        """Run complete test suite"""

        self.start_time = time.time()
        self.results = []

        print("\n" + "=" * 60)
        print(f"RUNNING {suite_name.upper()}")
        print(f"Total topics: {len(test_suite)}")
        print("=" * 60)

        for i, test_case in enumerate(test_suite, 1):
            print(f"\n[{i}/{len(test_suite)}] Testing: {test_case['topic']}")
            print(
                f"  Category: {test_case['category']}, Difficulty: {test_case['difficulty']}"
            )
            print(f"  Expected: {test_case['expected_sentiment']}")

            result = self.run_single_test(test_case)
            self.results.append(result)

            if result["success"]:
                match_icon = "✓" if result["exact_match"] else "~"
                print(f"  {match_icon} Got: {result['actual_sentiment']}")
                print(
                    f"  Accuracy: {result['accuracy_score']:.0%}, Confidence: {result['confidence']:.0%}"
                )
                print(
                    f"  Time: {result['time_seconds']:.1f}s, Sources: {result['sources_analyzed']}"
                )
            else:
                print(f"  ✗ FAILED: {result['error'][:100]}")

        self.end_time = time.time()

        # Generate and print report
        self.print_summary()

        # Save results
        self.save_results(suite_name)

        return self.results

    def print_summary(self):
        """Print detailed summary of test results"""

        print("\n" + "=" * 60)
        print("TEST RESULTS SUMMARY")
        print("=" * 60)

        total = len(self.results)
        successful = [r for r in self.results if r["success"]]
        failed = [r for r in self.results if not r["success"]]

        # Basic stats
        print(f"\nTotal tests: {total}")
        print(f"Successful: {len(successful)} ({len(successful) / total * 100:.0f}%)")
        print(f"Failed: {len(failed)} ({len(failed) / total * 100:.0f}%)")

        if not successful:
            print("\n⚠ No successful tests to analyze")
            return

        # Accuracy metrics
        exact_matches = sum(1 for r in successful if r["exact_match"])
        avg_accuracy = sum(r["accuracy_score"] for r in successful) / len(successful)
        avg_confidence = sum(r["confidence"] for r in successful) / len(successful)

        print(f"\n{'=' * 60}")
        print("ACCURACY METRICS")
        print(f"{'=' * 60}")
        print(
            f"Exact matches: {exact_matches}/{len(successful)} ({exact_matches / len(successful) * 100:.0f}%)"
        )
        print(f"Average accuracy score: {avg_accuracy:.0%}")
        print(f"Average confidence: {avg_confidence:.0%}")

        # Performance metrics
        avg_time = sum(r["time_seconds"] for r in successful) / len(successful)
        avg_sources = sum(r["sources_analyzed"] for r in successful) / len(successful)

        print(f"\n{'=' * 60}")
        print("PERFORMANCE METRICS")
        print(f"{'=' * 60}")
        print(f"Average time: {avg_time:.1f} seconds")
        print(f"Average sources analyzed: {avg_sources:.1f}")
        print(f"Total time: {self.end_time - self.start_time:.1f} seconds")

        # Breakdown by difficulty
        print(f"\n{'=' * 60}")
        print("ACCURACY BY DIFFICULTY")
        print(f"{'=' * 60}")

        for difficulty in ["easy", "medium", "hard"]:
            diff_results = [r for r in successful if r["difficulty"] == difficulty]
            if diff_results:
                diff_accuracy = sum(r["accuracy_score"] for r in diff_results) / len(
                    diff_results
                )
                diff_exact = sum(1 for r in diff_results if r["exact_match"])
                print(
                    f"{difficulty.capitalize()}: {diff_exact}/{len(diff_results)} exact ({diff_accuracy:.0%} avg accuracy)"
                )

        # Breakdown by category
        print(f"\n{'=' * 60}")
        print("ACCURACY BY CATEGORY")
        print(f"{'=' * 60}")

        categories = set(r["category"] for r in successful)
        for category in sorted(categories):
            cat_results = [r for r in successful if r["category"] == category]
            cat_accuracy = sum(r["accuracy_score"] for r in cat_results) / len(
                cat_results
            )
            cat_exact = sum(1 for r in cat_results if r["exact_match"])
            print(
                f"{category}: {cat_exact}/{len(cat_results)} exact ({cat_accuracy:.0%} avg accuracy)"
            )

        # Sentiment confusion matrix
        print(f"\n{'=' * 60}")
        print("SENTIMENT CONFUSION")
        print(f"{'=' * 60}")

        confusion = {}
        for r in successful:
            expected = r["expected_sentiment"]
            actual = r["actual_sentiment"]
            key = f"{expected} → {actual}"
            confusion[key] = confusion.get(key, 0) + 1

        for pair, count in sorted(confusion.items(), key=lambda x: x[1], reverse=True):
            print(f"  {pair}: {count}")

        # Common errors
        if failed:
            print(f"\n{'=' * 60}")
            print("FAILED TESTS")
            print(f"{'=' * 60}")
            for r in failed:
                print(f"  ✗ {r['topic']}: {r['error'][:80]}")

        print(f"\n{'=' * 60}")

    def save_results(self, suite_name: str):
        """Save detailed results to JSON file"""

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = (
            f"../data/test_results_{suite_name.replace(' ', '_')}_{timestamp}.json"
        )

        # Calculate summary stats
        successful = [r for r in self.results if r["success"]]

        summary = {
            "suite_name": suite_name,
            "timestamp": str(datetime.now()),
            "total_tests": len(self.results),
            "successful": len(successful),
            "failed": len(self.results) - len(successful),
            "total_time_seconds": self.end_time - self.start_time
            if self.end_time
            else 0,
            "metrics": {},
        }

        if successful:
            summary["metrics"] = {
                "exact_match_rate": sum(1 for r in successful if r["exact_match"])
                / len(successful),
                "average_accuracy_score": sum(r["accuracy_score"] for r in successful)
                / len(successful),
                "average_confidence": sum(r["confidence"] for r in successful)
                / len(successful),
                "average_time_seconds": sum(r["time_seconds"] for r in successful)
                / len(successful),
                "average_sources": sum(r["sources_analyzed"] for r in successful)
                / len(successful),
            }

        output = {"summary": summary, "detailed_results": self.results}

        # Save to file
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        with open(filename, "w") as f:
            json.dump(output, f, indent=2)

        print(f"\n✓ Results saved to: {filename}")

        return filename

    def get_metrics(self) -> dict:
        """Get metrics dictionary for programmatic access"""
        successful = [r for r in self.results if r["success"]]

        if not successful:
            return {}

        return {
            "total_tests": len(self.results),
            "successful_tests": len(successful),
            "failed_tests": len(self.results) - len(successful),
            "exact_match_rate": sum(1 for r in successful if r["exact_match"])
            / len(successful),
            "average_accuracy": sum(r["accuracy_score"] for r in successful)
            / len(successful),
            "average_confidence": sum(r["confidence"] for r in successful)
            / len(successful),
            "average_time": sum(r["time_seconds"] for r in successful)
            / len(successful),
            "total_time": self.end_time - self.start_time if self.end_time else 0,
        }


def main():
    """Main test runner"""

    print("\n" + "=" * 60)
    print("COMPREHENSIVE AGENT TEST")
    print("=" * 60)
    print("\nAvailable test suites:")
    print("  1. Quick Test (5 topics) - ~3 minutes")
    print("  2. Standard Test (10 topics) - ~6 minutes")
    print("  3. Full Test (25 topics) - ~15 minutes")

    choice = input("\nSelect test suite (1-3): ").strip()

    suite_map = {
        "1": (QUICK_TEST, "Quick Test"),
        "2": (STANDARD_TEST, "Standard Test"),
        "3": (FULL_TEST, "Full Test"),
    }

    if choice not in suite_map:
        print("Invalid choice, defaulting to Quick Test")
        choice = "1"

    test_suite, suite_name = suite_map[choice]

    # Initialize agent
    print(f"\nInitializing agent...")
    agent = SentimentAgent()

    # Create test runner
    runner = ComprehensiveTestRunner(agent)

    # Run tests
    results = runner.run_test_suite(test_suite, suite_name)

    # Print final summary
    metrics = runner.get_metrics()

    print(f"\n{'=' * 60}")
    print("FINAL SUMMARY")
    print(f"{'=' * 60}")
    print(f"Overall Accuracy: {metrics.get('average_accuracy', 0):.0%}")
    print(f"Exact Match Rate: {metrics.get('exact_match_rate', 0):.0%}")
    print(
        f"Success Rate: {metrics.get('successful_tests', 0)}/{metrics.get('total_tests', 0)}"
    )
    print(f"Total Time: {metrics.get('total_time', 0):.1f}s")
    print(f"Cost: $0.00 (FREE!)")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()

"""
Verify ground truth dataset quality.
Optionally run purple agent to double-check ground truth.
"""

import sys

sys.path.append("../purple-agent")

from test_topics import TEST_TOPICS, QUICK_TEST
from ground_truth import (
    get_ground_truth,
    get_all_topics_with_ground_truth,
    get_ground_truth_summary,
)


def verify_ground_truth_coverage():
    """Check that all test topics have ground truth"""

    print("\n" + "=" * 60)
    print("GROUND TRUTH COVERAGE CHECK")
    print("=" * 60)

    topics_with_gt = set(get_all_topics_with_ground_truth())
    all_test_topics = set(t["topic"] for t in TEST_TOPICS)

    # Topics with ground truth
    covered = topics_with_gt.intersection(all_test_topics)
    missing = all_test_topics - topics_with_gt

    print(f"\nTest topics: {len(all_test_topics)}")
    print(
        f"With ground truth: {len(covered)} ({len(covered) / len(all_test_topics) * 100:.0f}%)"
    )

    if missing:
        print(f"\n⚠ Missing ground truth for {len(missing)} topics:")
        for topic in sorted(missing):
            print(f"  - {topic}")
        print("\nAction: Add ground truth for these topics to ground_truth.py")
    else:
        print("\n✅ All test topics have ground truth!")

    # Show summary
    summary = get_ground_truth_summary()

    print(f"\n{'=' * 60}")
    print("GROUND TRUTH SUMMARY")
    print(f"{'=' * 60}")
    print(f"Total topics with ground truth: {summary['total_topics']}")
    print(f"Average confidence: {summary['average_confidence']:.2f}")
    print(f"\nSentiment distribution:")
    for sentiment, count in sorted(summary["sentiment_distribution"].items()):
        print(f"  {sentiment}: {count}")

    return len(missing) == 0


def verify_with_agent():
    """
    Run purple agent on topics to verify ground truth is reasonable.
    This is optional but helps validate your ground truth.
    """

    print(f"\n{'=' * 60}")
    print("VERIFY GROUND TRUTH WITH AGENT (Optional)")
    print(f"{'=' * 60}")
    print("This will run the purple agent on a few topics to validate ground truth.")

    response = input("\nRun verification? (y/n): ").strip().lower()

    if response != "y":
        print("Skipping agent verification.")
        return

    from purple_agent import SentimentAgent
    import json

    agent = SentimentAgent()

    # Test on quick test topics
    results = []

    print(f"\nTesting {len(QUICK_TEST)} topics...")

    for i, test_case in enumerate(QUICK_TEST, 1):
        topic = test_case["topic"]
        expected = test_case["expected_sentiment"]

        print(f"\n[{i}/{len(QUICK_TEST)}] {topic}")
        print(f"  Expected: {expected}")

        try:
            report = agent.analyze_topic(topic)
            actual = report.overall_sentiment

            gt = get_ground_truth(topic)
            verified = gt.get("verified_sentiment", "unknown")

            print(f"  Agent got: {actual} ({report.confidence:.0%})")
            print(f"  Ground truth: {verified}")

            match_expected = actual == expected
            match_verified = actual == verified

            if match_expected and match_verified:
                print("  ✓✓ Perfect match!")
            elif match_expected or match_verified:
                print("  ✓ Matches one")
            else:
                print("  ⚠ Discrepancy - review recommended")

            results.append(
                {
                    "topic": topic,
                    "expected": expected,
                    "verified": verified,
                    "agent_result": actual,
                    "confidence": report.confidence,
                    "match_expected": match_expected,
                    "match_verified": match_verified,
                }
            )

        except Exception as e:
            print(f"  ✗ Error: {e}")

    # Save results
    import json

    output_file = "../data/ground_truth_verification.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n✓ Verification results saved to: {output_file}")


if __name__ == "__main__":
    coverage_ok = verify_ground_truth_coverage()

    if coverage_ok:
        verify_with_agent()
    else:
        print("\n⚠ Fix ground truth coverage before running agent verification")

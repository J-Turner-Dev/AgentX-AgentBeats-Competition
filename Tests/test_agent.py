"""
Test the purple agent on sample topics.
Run this to validate your agent works correctly.
"""

import sys
import os

sys.path.append("../PurpleAgent")  # Adjust path to your purple-agent directory

from purple_agent import SentimentAgent
from test_topics import QUICK_TEST_TOPICS
import json
from datetime import datetime


def test_agent():
    """Run agent on test topics"""
    print("\n" + "=" * 60)
    print("TESTING SENTIMENT AGENT")
    print("=" * 60)

    agent = SentimentAgent()

    results = []
    correct = 0
    total = 0

    for i, test_case in enumerate(QUICK_TEST_TOPICS, 1):
        print(f"\n{'=' * 60}")
        print(f"TEST {i}/{len(QUICK_TEST_TOPICS)}: {test_case['topic']}")
        print(f"Expected: {test_case['expected_sentiment']}")
        print(f"Reasoning: {test_case['reasoning']}")
        print(f"{'=' * 60}")

        try:
            # Run analysis
            report = agent.analyze_topic(test_case["topic"])

            # Check if result matches expectation
            match = report.overall_sentiment == test_case["expected_sentiment"]

            if match:
                correct += 1
            total += 1

            result = {
                "topic": test_case["topic"],
                "expected": test_case["expected_sentiment"],
                "actual": report.overall_sentiment,
                "confidence": report.confidence,
                "match": match,
                "sources_analyzed": report.sources_analyzed,
                "summary": report.summary,
            }

            results.append(result)

            # Print result
            print(f"\n✓ Expected: {test_case['expected_sentiment']}")
            print(f"✓ Got: {report.overall_sentiment}")
            print(f"✓ Confidence: {report.confidence:.0%}")
            print(f"✓ Match: {'✅ YES' if match else '❌ NO'}")
            print(f"✓ Sources: {report.sources_analyzed}")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            result = {
                "topic": test_case["topic"],
                "expected": test_case["expected_sentiment"],
                "actual": "ERROR",
                "match": False,
                "error": str(e),
            }
            results.append(result)
            total += 1

    # Print summary
    print(f"\n{'=' * 60}")
    print(f"TEST SUMMARY")
    print(f"{'=' * 60}")
    print(f"Tests run: {total}")
    print(f"Correct: {correct}/{total}")
    print(f"Accuracy: {correct / total * 100:.1f}%" if total > 0 else "N/A")
    print(f"{'=' * 60}\n")

    # Print detailed results
    print("DETAILED RESULTS:")
    print("-" * 60)
    for i, r in enumerate(results, 1):
        status = "✅" if r["match"] else "❌"
        print(f"{i}. {status} {r['topic']}")
        print(f"   Expected: {r['expected']} | Got: {r['actual']}")
        if "confidence" in r:
            print(f"   Confidence: {r['confidence']:.0%}")
        print()

    # Save results to file
    output_file = (
        f"../data/test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    )

    # Create data directory if it doesn't exist
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, "w") as f:
        json.dump(
            {
                "timestamp": datetime.now().isoformat(),
                "total_tests": total,
                "correct": correct,
                "accuracy": correct / total if total > 0 else 0,
                "results": results,
            },
            f,
            indent=2,
        )

    print(f"✓ Results saved to: {output_file}")

    # Print usage stats
    print(f"\n{'=' * 60}")
    print(f"USAGE STATS")
    print(f"{'=' * 60}")
    print(f"API calls made: {agent.api_calls}")
    print(f"Searches made: {agent.searches_made}")
    print(f"Total cost: $0.00 (FREE!)")
    print(f"{'=' * 60}\n")

    return results


def test_single_topic(topic: str, expected_sentiment: str = None):
    """Test agent on a single topic"""
    print(f"\n{'=' * 60}")
    print(f"TESTING SINGLE TOPIC: {topic}")
    print(f"{'=' * 60}\n")

    agent = SentimentAgent()
    report = agent.analyze_topic(topic)

    print(f"\n{'=' * 60}")
    print(f"RESULT")
    print(f"{'=' * 60}")
    print(f"Topic: {report.topic}")
    print(f"Overall Sentiment: {report.overall_sentiment.upper()}")
    print(f"Confidence: {report.confidence:.1%}")
    print(f"\nBreakdown:")
    print(f"  Positive: {report.positive_count}")
    print(f"  Negative: {report.negative_count}")
    print(f"  Neutral: {report.neutral_count}")
    print(f"  Mixed: {report.mixed_count}")
    print(f"\nSummary: {report.summary}")

    if expected_sentiment:
        match = report.overall_sentiment == expected_sentiment
        print(f"\nExpected: {expected_sentiment}")
        print(f"Match: {'✅ YES' if match else '❌ NO'}")

    print(f"{'=' * 60}\n")

    return report


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Test the sentiment agent")
    parser.add_argument("--topic", type=str, help="Test a single topic")
    parser.add_argument(
        "--expected",
        type=str,
        help="Expected sentiment (positive/negative/neutral/mixed)",
    )

    args = parser.parse_args()

    if args.topic:
        # Test single topic
        test_single_topic(args.topic, args.expected)
    else:
        # Run full test suite
        test_agent()

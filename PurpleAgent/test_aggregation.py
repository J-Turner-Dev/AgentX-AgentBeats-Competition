"""
Test advanced aggregation on controversial topics.
"""

from purple_agent import SentimentAgent

# Topics with likely divided opinions
controversial_topics = [
    "electric vehicles",
    "remote work",
    "artificial intelligence",
    "social media impact",
]

agent = SentimentAgent()

print("\n" + "=" * 60)
print("ADVANCED AGGREGATION TEST")
print("=" * 60)

for topic in controversial_topics:
    print(f"\n{'=' * 60}")
    print(f"Topic: {topic}")
    print(f"{'=' * 60}")

    report = agent.analyze_topic(topic)

    print(f"\nOverall: {report.overall_sentiment}")
    print(f"Confidence: {report.confidence:.0%}")
    print(f"Distribution:")
    print(f"  Positive: {report.positive_count}")
    print(f"  Negative: {report.negative_count}")
    print(f"  Neutral: {report.neutral_count}")
    print(f"  Mixed: {report.mixed_count}")

    # Check if properly detected as mixed/controversial
    if report.overall_sentiment == "mixed" or report.mixed_count > 0:
        print("  ✓ Detected nuance/controversy")

    print(f"\nSummary: {report.summary}")

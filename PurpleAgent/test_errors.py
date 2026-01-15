"""
Test error handling with difficult topics.
"""

from purple_agent import SentimentAgent

# Topics that might cause issues
difficult_topics = [
    "asdfghjkl",  # Nonsense - should fail gracefully
    "very obscure topic that doesn't exist",  # No results
    "",  # Empty string
    "a" * 200,  # Very long topic
]

agent = SentimentAgent()

print("\n" + "=" * 60)
print("ERROR HANDLING TEST")
print("=" * 60)

for topic in difficult_topics:
    print(f"\n Testing: {topic[:50]}...")

    try:
        report = agent.analyze_topic(topic)
        print(f"  ✓ Handled successfully: {report.overall_sentiment}")
    except Exception as e:
        print(f"  ✓ Failed gracefully: {type(e).__name__}")

agent.error_stats.print_summary()

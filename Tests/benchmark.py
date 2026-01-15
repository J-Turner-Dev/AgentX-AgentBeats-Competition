import sys
import time

sys.path.append("../PurpleAgent")

from purple_agent import SentimentAgent
from test_topics import TEST_TOPICS


def benchmark_agent():
    """Measure agent performance metrics"""

    agent = SentimentAgent()

    metrics = {
        "total_time": 0,
        "successful": 0,
        "failed": 0,
        "avg_sources": 0,
        "avg_confidence": 0,
        "accuracy": 0,
    }

    start_time = time.time()

    for test_case in TEST_TOPICS:
        topic_start = time.time()

        try:
            report = agent.analyze_topic(test_case["topic"])

            metrics["successful"] += 1
            metrics["avg_sources"] += report.sources_analyzed
            metrics["avg_confidence"] += report.confidence

            # Check accuracy
            if report.overall_sentiment == test_case["expected_sentiment"]:
                metrics["accuracy"] += 1

            topic_time = time.time() - topic_start
            print(f"  ✓ {test_case['topic']}: {topic_time:.1f}s")

        except Exception as e:
            metrics["failed"] += 1
            print(f"  ✗ {test_case['topic']}: {str(e)[:50]}")

    metrics["total_time"] = time.time() - start_time

    # Calculate averages
    total_tests = metrics["successful"] + metrics["failed"]
    if metrics["successful"] > 0:
        metrics["avg_sources"] /= metrics["successful"]
        metrics["avg_confidence"] /= metrics["successful"]
        metrics["accuracy"] = metrics["accuracy"] / metrics["successful"]

    # Print report
    print(f"\n{'=' * 60}")
    print("BENCHMARK RESULTS")
    print(f"{'=' * 60}")
    print(f"Total time: {metrics['total_time']:.1f}s")
    print(f"Avg time per topic: {metrics['total_time'] / total_tests:.1f}s")
    print(f"Successful: {metrics['successful']}/{total_tests}")
    print(f"Accuracy: {metrics['accuracy']:.1%}")
    print(f"Avg sources analyzed: {metrics['avg_sources']:.1f}")
    print(f"Avg confidence: {metrics['avg_confidence']:.1%}")
    print(f"API calls: {agent.api_calls}")
    print(f"Searches: {agent.searches_made}")
    print(f"Cost: $0.00 (FREE!)")
    print(f"{'=' * 60}\n")

    return metrics


if __name__ == "__main__":
    benchmark_agent()

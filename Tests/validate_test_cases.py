"""
Validate test case quality and diversity.
"""

from test_topics import TEST_TOPICS
from collections import Counter


def validate_test_cases():
    """Check that test cases meet quality standards"""

    print("\n" + "=" * 60)
    print("TEST CASE VALIDATION")
    print("=" * 60)

    # Basic stats
    print(f"\nTotal test cases: {len(TEST_TOPICS)}")

    # Check sentiment distribution
    sentiments = [t["expected_sentiment"] for t in TEST_TOPICS]
    sentiment_counts = Counter(sentiments)

    print("\nSentiment Distribution:")
    for sentiment, count in sorted(sentiment_counts.items()):
        pct = count / len(TEST_TOPICS) * 100
        print(f"  {sentiment.capitalize()}: {count} ({pct:.0f}%)")

    # Check category distribution
    categories = [t["category"] for t in TEST_TOPICS]
    category_counts = Counter(categories)

    print(f"\nCategories Covered: {len(category_counts)}")
    for category, count in sorted(category_counts.items()):
        print(f"  {category}: {count}")

    # Check difficulty distribution
    difficulties = [t["difficulty"] for t in TEST_TOPICS]
    difficulty_counts = Counter(difficulties)

    print("\nDifficulty Distribution:")
    for difficulty, count in sorted(difficulty_counts.items()):
        pct = count / len(TEST_TOPICS) * 100
        print(f"  {difficulty.capitalize()}: {count} ({pct:.0f}%)")

    # Validation checks
    print(f"\n{'=' * 60}")
    print("VALIDATION CHECKS")
    print(f"{'=' * 60}")

    issues = []
    warnings = []

    # Check: Minimum 20 topics
    if len(TEST_TOPICS) < 20:
        issues.append(f"Need at least 20 topics (have {len(TEST_TOPICS)})")
    else:
        print(f"✓ Sufficient topics: {len(TEST_TOPICS)}")

    # Check: Balanced sentiments
    min_per_sentiment = 3
    for sentiment, count in sentiment_counts.items():
        if count < min_per_sentiment:
            issues.append(
                f"Need at least {min_per_sentiment} {sentiment} topics (have {count})"
            )

    if len(issues) == 0:
        print(f"✓ Balanced sentiments (min {min_per_sentiment} each)")

    # Check: Category diversity
    min_categories = 5
    if len(category_counts) < min_categories:
        warnings.append(
            f"Only {len(category_counts)} categories (recommend {min_categories}+)"
        )
    else:
        print(f"✓ Good category diversity: {len(category_counts)} categories")

    # Check: Difficulty mix
    if difficulty_counts.get("easy", 0) < 5:
        warnings.append("Need more easy topics for baseline testing")
    if difficulty_counts.get("medium", 0) < 3:
        warnings.append("Need more medium difficulty topics")
    if difficulty_counts.get("hard", 0) < 1:
        warnings.append("Should have at least 1 hard topic")

    if len(warnings) == 0:
        print(f"✓ Good difficulty distribution")

    # Check: No duplicate topics
    topics = [t["topic"].lower() for t in TEST_TOPICS]
    if len(topics) != len(set(topics)):
        issues.append("Duplicate topics detected")
    else:
        print(f"✓ No duplicate topics")

    # Check: All required fields present
    required_fields = [
        "topic",
        "expected_sentiment",
        "reasoning",
        "category",
        "difficulty",
    ]
    for i, test_case in enumerate(TEST_TOPICS):
        missing = [f for f in required_fields if f not in test_case]
        if missing:
            issues.append(f"Topic {i} missing fields: {missing}")

    if len([i for i in issues if "missing fields" in i]) == 0:
        print(f"✓ All topics have required fields")

    # Final report
    print(f"\n{'=' * 60}")

    if issues:
        print("❌ VALIDATION FAILED")
        print(f"{'=' * 60}")
        print("\nIssues to fix:")
        for issue in issues:
            print(f"  ✗ {issue}")

    if warnings:
        print("\nWarnings (optional improvements):")
        for warning in warnings:
            print(f"  ⚠ {warning}")

    if not issues and not warnings:
        print("✅ VALIDATION PASSED")
        print(f"{'=' * 60}")
        print("Test cases are high quality and ready for use!")
    elif not issues:
        print("✅ VALIDATION PASSED (with warnings)")
        print(f"{'=' * 60}")
        print("Test cases are acceptable. Consider addressing warnings.")

    print(f"{'=' * 60}\n")

    return len(issues) == 0


if __name__ == "__main__":
    success = validate_test_cases()
    import sys

    sys.exit(0 if success else 1)

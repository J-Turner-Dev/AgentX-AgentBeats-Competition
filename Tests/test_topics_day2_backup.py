"""
Test topics with expected sentiments for validation.
These are topics where sentiment is relatively clear.
"""

TEST_TOPICS = [
    {
        "topic": "iPhone 16",
        "expected_sentiment": "positive",
        "reasoning": "New Apple products generally get positive reviews",
        "category": "technology",
    },
    {
        "topic": "Twitter rebrand to X",
        "expected_sentiment": "negative",
        "reasoning": "Widely criticized rebrand",
        "category": "social_media",
    },
    {
        "topic": "ChatGPT",
        "expected_sentiment": "mixed",
        "reasoning": "Excitement about capabilities + concerns about AI",
        "category": "ai",
    },
    {
        "topic": "climate change",
        "expected_sentiment": "negative",
        "reasoning": "Predominantly concerning news and impacts",
        "category": "environment",
    },
    {
        "topic": "Taylor Swift Eras Tour",
        "expected_sentiment": "positive",
        "reasoning": "Overwhelmingly positive fan reactions",
        "category": "entertainment",
    },
    {
        "topic": "remote work",
        "expected_sentiment": "mixed",
        "reasoning": "People have strong opinions both ways",
        "category": "workplace",
    },
    {
        "topic": "electric vehicles",
        "expected_sentiment": "mixed",
        "reasoning": "Excitement about tech + concerns about infrastructure",
        "category": "automotive",
    },
    {
        "topic": "inflation 2024",
        "expected_sentiment": "negative",
        "reasoning": "Economic concerns dominate",
        "category": "economy",
    },
]

# For Day 1, we'll just test on 2-3 topics to save API calls
QUICK_TEST_TOPICS = TEST_TOPICS[:3]

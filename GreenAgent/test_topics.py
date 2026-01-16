"""
Comprehensive test topics for sentiment analysis.
Covers diverse domains, difficulty levels, and sentiment types.
"""

TEST_TOPICS = [
    # ============================================
    # TECHNOLOGY - Generally Positive
    # ============================================
    {
        "topic": "iPhone 16",
        "expected_sentiment": "positive",
        "reasoning": "New Apple products generally receive positive reviews",
        "category": "technology",
        "difficulty": "easy",
        "tags": ["consumer_tech", "mobile", "apple"],
    },
    {
        "topic": "M4 MacBook Pro",
        "expected_sentiment": "positive",
        "reasoning": "Performance improvements widely praised",
        "category": "technology",
        "difficulty": "easy",
        "tags": ["consumer_tech", "laptops", "apple"],
    },
    {
        "topic": "Steam Deck",
        "expected_sentiment": "positive",
        "reasoning": "Gaming handheld well-received by enthusiasts",
        "category": "gaming",
        "difficulty": "easy",
        "tags": ["gaming", "hardware"],
    },
    # ============================================
    # TECHNOLOGY - Negative
    # ============================================
    {
        "topic": "Twitter rebrand to X",
        "expected_sentiment": "negative",
        "reasoning": "Widely criticized rebrand, brand confusion",
        "category": "social_media",
        "difficulty": "easy",
        "tags": ["social_media", "branding", "controversial"],
    },
    {
        "topic": "Windows 11 forced updates",
        "expected_sentiment": "negative",
        "reasoning": "User frustration with mandatory updates",
        "category": "technology",
        "difficulty": "easy",
        "tags": ["software", "operating_systems"],
    },
    # ============================================
    # TECHNOLOGY - Mixed
    # ============================================
    {
        "topic": "Windows 11",
        "expected_sentiment": "mixed",
        "reasoning": "UI changes divisive, performance mixed",
        "category": "technology",
        "difficulty": "medium",
        "tags": ["software", "operating_systems", "controversial"],
    },
    {
        "topic": "Threads social media app",
        "expected_sentiment": "mixed",
        "reasoning": "Initial hype vs feature limitations",
        "category": "social_media",
        "difficulty": "medium",
        "tags": ["social_media", "meta"],
    },
    # ============================================
    # AI & AUTOMATION - Mixed Sentiments
    # ============================================
    {
        "topic": "ChatGPT",
        "expected_sentiment": "mixed",
        "reasoning": "Excitement about capabilities + concerns about accuracy/ethics",
        "category": "ai",
        "difficulty": "medium",
        "tags": ["ai", "controversial", "transformative"],
    },
    {
        "topic": "AI replacing jobs",
        "expected_sentiment": "negative",
        "reasoning": "Workforce concerns and anxiety predominate",
        "category": "ai",
        "difficulty": "easy",
        "tags": ["ai", "employment", "workforce"],
    },
    {
        "topic": "GitHub Copilot",
        "expected_sentiment": "positive",
        "reasoning": "Developers find it helpful and productive",
        "category": "ai",
        "difficulty": "easy",
        "tags": ["ai", "developer_tools", "coding"],
    },
    {
        "topic": "AI generated art",
        "expected_sentiment": "mixed",
        "reasoning": "Technology advancement vs artist concerns",
        "category": "ai",
        "difficulty": "medium",
        "tags": ["ai", "art", "controversial"],
    },
    # ============================================
    # ENVIRONMENT - Generally Negative/Concerning
    # ============================================
    {
        "topic": "climate change",
        "expected_sentiment": "negative",
        "reasoning": "Predominantly concerning news and impacts",
        "category": "environment",
        "difficulty": "easy",
        "tags": ["environment", "climate", "global"],
    },
    {
        "topic": "electric vehicles",
        "expected_sentiment": "mixed",
        "reasoning": "Enthusiasm for tech + infrastructure/cost concerns",
        "category": "automotive",
        "difficulty": "medium",
        "tags": ["automotive", "environment", "technology"],
    },
    # ============================================
    # ENTERTAINMENT - Generally Positive
    # ============================================
    {
        "topic": "Taylor Swift Eras Tour",
        "expected_sentiment": "positive",
        "reasoning": "Overwhelming fan enthusiasm and success",
        "category": "entertainment",
        "difficulty": "easy",
        "tags": ["entertainment", "music", "concerts"],
    },
    {
        "topic": "Barbie movie 2023",
        "expected_sentiment": "positive",
        "reasoning": "Critical and commercial success",
        "category": "entertainment",
        "difficulty": "easy",
        "tags": ["entertainment", "movies"],
    },
    {
        "topic": "Baldurs Gate 3",
        "expected_sentiment": "positive",
        "reasoning": "Critical acclaim, GOTY awards",
        "category": "gaming",
        "difficulty": "easy",
        "tags": ["gaming", "rpg"],
    },
    # ============================================
    # WORKPLACE - Mixed
    # ============================================
    {
        "topic": "remote work",
        "expected_sentiment": "mixed",
        "reasoning": "Strong opinions both for and against",
        "category": "workplace",
        "difficulty": "medium",
        "tags": ["workplace", "controversial", "productivity"],
    },
    {
        "topic": "4-day work week",
        "expected_sentiment": "positive",
        "reasoning": "Pilot programs show success, worker approval",
        "category": "workplace",
        "difficulty": "medium",
        "tags": ["workplace", "policy", "work_life_balance"],
    },
    {
        "topic": "return to office mandates",
        "expected_sentiment": "negative",
        "reasoning": "Widespread employee pushback and frustration",
        "category": "workplace",
        "difficulty": "easy",
        "tags": ["workplace", "policy"],
    },
    # ============================================
    # ECONOMY - Generally Negative/Concerning
    # ============================================
    {
        "topic": "inflation 2024",
        "expected_sentiment": "negative",
        "reasoning": "Economic concerns and financial stress",
        "category": "economy",
        "difficulty": "easy",
        "tags": ["economy", "finance"],
    },
    {
        "topic": "cryptocurrency regulation",
        "expected_sentiment": "mixed",
        "reasoning": "Investors vs regulators, divided opinions",
        "category": "finance",
        "difficulty": "medium",
        "tags": ["finance", "cryptocurrency", "policy"],
    },
    # ============================================
    # HEALTH - Mixed
    # ============================================
    {
        "topic": "Ozempic for weight loss",
        "expected_sentiment": "mixed",
        "reasoning": "Effectiveness praised, side effects/access concerns",
        "category": "health",
        "difficulty": "medium",
        "tags": ["health", "medicine", "controversial"],
    },
    {
        "topic": "mental health awareness",
        "expected_sentiment": "positive",
        "reasoning": "Growing acceptance, reduced stigma",
        "category": "health",
        "difficulty": "easy",
        "tags": ["health", "mental_health", "social"],
    },
    # ============================================
    # EDGE CASES - Challenging Topics
    # ============================================
    {
        "topic": "pineapple on pizza",
        "expected_sentiment": "mixed",
        "reasoning": "Classic controversial food debate",
        "category": "food",
        "difficulty": "hard",
        "tags": ["food", "controversial", "meme"],
    },
    {
        "topic": "daylight saving time",
        "expected_sentiment": "negative",
        "reasoning": "Most people want it abolished",
        "category": "policy",
        "difficulty": "medium",
        "tags": ["policy", "time"],
    },
    {
        "topic": "self-checkout machines",
        "expected_sentiment": "mixed",
        "reasoning": "Convenience vs job loss vs technical issues",
        "category": "retail",
        "difficulty": "medium",
        "tags": ["retail", "automation", "consumer"],
    },
]

# ============================================
# CATEGORIZED SUBSETS
# ============================================

# By difficulty
EASY_TOPICS = [t for t in TEST_TOPICS if t["difficulty"] == "easy"]
MEDIUM_TOPICS = [t for t in TEST_TOPICS if t["difficulty"] == "medium"]
HARD_TOPICS = [t for t in TEST_TOPICS if t["difficulty"] == "hard"]

# By expected sentiment
POSITIVE_TOPICS = [t for t in TEST_TOPICS if t["expected_sentiment"] == "positive"]
NEGATIVE_TOPICS = [t for t in TEST_TOPICS if t["expected_sentiment"] == "negative"]
MIXED_TOPICS = [t for t in TEST_TOPICS if t["expected_sentiment"] == "mixed"]
NEUTRAL_TOPICS = [t for t in TEST_TOPICS if t["expected_sentiment"] == "neutral"]

# Quick test (5 diverse topics)
QUICK_TEST = [
    TEST_TOPICS[0],  # iPhone 16 (positive, easy)
    TEST_TOPICS[3],  # Twitter rebrand (negative, easy)
    TEST_TOPICS[7],  # ChatGPT (mixed, medium)
    TEST_TOPICS[13],  # Taylor Swift (positive, easy)
    TEST_TOPICS[16],  # remote work (mixed, medium)
]

# Standard test (10 topics)
STANDARD_TEST = QUICK_TEST + [
    TEST_TOPICS[8],  # AI replacing jobs
    TEST_TOPICS[11],  # climate change
    TEST_TOPICS[18],  # return to office
    TEST_TOPICS[20],  # Ozempic
    TEST_TOPICS[23],  # pineapple pizza
]

# Full test (all 25 topics)
FULL_TEST = TEST_TOPICS

print(f"Total test topics: {len(TEST_TOPICS)}")
print(f"  Easy: {len(EASY_TOPICS)}")
print(f"  Medium: {len(MEDIUM_TOPICS)}")
print(f"  Hard: {len(HARD_TOPICS)}")
print(f"  Positive: {len(POSITIVE_TOPICS)}")
print(f"  Negative: {len(NEGATIVE_TOPICS)}")
print(f"  Mixed: {len(MIXED_TOPICS)}")

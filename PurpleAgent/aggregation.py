"""
Advanced sentiment aggregation logic.
Goes beyond simple majority voting.
"""

from typing import List, Dict, Tuple
from dataclasses import dataclass
from collections import Counter


@dataclass
class SentimentResult:
    """Import the dataclass from purple_agent or redefine"""

    source_url: str
    source_title: str
    sentiment: str
    confidence: float
    key_quote: str
    reasoning: str


class SentimentAggregator:
    """
    Advanced sentiment aggregation strategies.
    """

    @staticmethod
    def simple_majority(results: List[SentimentResult]) -> Tuple[str, float]:
        """Simple majority voting"""
        if not results:
            return "neutral", 0.0

        sentiments = [r.sentiment for r in results]
        counter = Counter(sentiments)
        most_common = counter.most_common(1)[0]

        sentiment = most_common[0]
        confidence = most_common[1] / len(results)

        return sentiment, confidence

    @staticmethod
    def weighted_by_confidence(results: List[SentimentResult]) -> Tuple[str, float]:
        """Weight votes by individual confidence scores"""
        if not results:
            return "neutral", 0.0

        # Calculate weighted votes
        weights = {}
        total_weight = 0

        for result in results:
            sentiment = result.sentiment
            weight = result.confidence

            weights[sentiment] = weights.get(sentiment, 0) + weight
            total_weight += weight

        if total_weight == 0:
            return "neutral", 0.0

        # Find sentiment with highest weight
        max_sentiment = max(weights, key=weights.get)
        confidence = weights[max_sentiment] / total_weight

        return max_sentiment, confidence

    @staticmethod
    def consensus_based(
        results: List[SentimentResult], threshold: float = 0.7
    ) -> Tuple[str, float]:
        """
        Requires strong consensus, otherwise returns "mixed"
        """
        if not results:
            return "neutral", 0.0

        sentiment, confidence = SentimentAggregator.weighted_by_confidence(results)

        # If no strong consensus, call it mixed
        if confidence < threshold:
            return "mixed", confidence

        return sentiment, confidence

    @staticmethod
    def detect_controversy(results: List[SentimentResult]) -> bool:
        """
        Detect if topic is controversial (strong opinions both ways)
        """
        if len(results) < 3:
            return False

        sentiments = [r.sentiment for r in results]
        counter = Counter(sentiments)

        # Check if we have significant positive AND negative
        positive = counter.get("positive", 0)
        negative = counter.get("negative", 0)

        total = len(results)

        # Controversial if both positive and negative are at least 25% each
        return (positive / total >= 0.25) and (negative / total >= 0.25)

    @staticmethod
    def get_sentiment_distribution(results: List[SentimentResult]) -> Dict[str, float]:
        """Get percentage distribution of sentiments"""
        if not results:
            return {}

        sentiments = [r.sentiment for r in results]
        counter = Counter(sentiments)
        total = len(results)

        return {sentiment: count / total for sentiment, count in counter.items()}

    @staticmethod
    def calculate_confidence_stats(results: List[SentimentResult]) -> Dict[str, float]:
        """Calculate confidence statistics"""
        if not results:
            return {"mean": 0.0, "min": 0.0, "max": 0.0}

        confidences = [r.confidence for r in results]

        return {
            "mean": sum(confidences) / len(confidences),
            "min": min(confidences),
            "max": max(confidences),
            "median": sorted(confidences)[len(confidences) // 2],
        }

    @staticmethod
    def aggregate_advanced(results: List[SentimentResult]) -> Dict:
        """
        Comprehensive aggregation with multiple metrics
        """
        if not results:
            return {
                "overall_sentiment": "neutral",
                "confidence": 0.0,
                "is_controversial": False,
                "distribution": {},
                "confidence_stats": {},
            }

        # Use consensus-based aggregation
        sentiment, confidence = SentimentAggregator.consensus_based(results)

        # Detect controversy
        is_controversial = SentimentAggregator.detect_controversy(results)

        # If controversial, override to "mixed"
        if is_controversial and sentiment not in ["mixed", "neutral"]:
            sentiment = "mixed"

        return {
            "overall_sentiment": sentiment,
            "confidence": confidence,
            "is_controversial": is_controversial,
            "distribution": SentimentAggregator.get_sentiment_distribution(results),
            "confidence_stats": SentimentAggregator.calculate_confidence_stats(results),
        }

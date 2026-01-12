"""
Track API usage (even though everything is FREE, it's good practice!)
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class UsageTracker:
    """Tracks API usage"""

    def __init__(self):
        self.groq_calls = 0
        self.tavily_searches = 0
        self.start_time = datetime.now()

    def add_groq_call(self):
        """Track a Groq API call"""
        self.groq_calls += 1

    def add_search(self):
        """Track a Tavily search"""
        self.tavily_searches += 1

    def get_summary(self) -> dict:
        """Get usage summary"""
        elapsed = (datetime.now() - self.start_time).total_seconds()

        return {
            "groq_calls": self.groq_calls,
            "tavily_searches": self.tavily_searches,
            "duration_seconds": elapsed,
            "cost": 0.0,  # Everything is FREE!
            "rate_groq": self.groq_calls / (elapsed / 60) if elapsed > 0 else 0,
            "rate_tavily": self.tavily_searches / (elapsed / 60) if elapsed > 0 else 0,
        }

    def print_summary(self):
        """Print usage summary"""
        summary = self.get_summary()

        print(f"\n{'=' * 60}")
        print(f"USAGE SUMMARY")
        print(f"{'=' * 60}")
        print(f"Groq API calls: {summary['groq_calls']}")
        print(f"Tavily searches: {summary['tavily_searches']}")
        print(f"Duration: {summary['duration_seconds']:.1f} seconds")
        print(f"Rate: {summary['rate_groq']:.1f} Groq calls/min")
        print(f"Total cost: $0.00 (FREE!)")
        print(f"{'=' * 60}\n")

"""
Purple Agent: Sentiment Analysis Agent
FREE VERSION using Groq API
"""

import os
import json
from typing import List, Dict, Optional
from dataclasses import dataclass
from dotenv import load_dotenv
from groq import Groq
from tavily import TavilyClient
from prompts import (
    SEARCH_QUERY_SYSTEM_PROMPT,
    SEARCH_QUERY_USER_TEMPLATE,
    SENTIMENT_ANALYSIS_SYSTEM_PROMPT,
    SENTIMENT_ANALYSIS_USER_TEMPLATE,
    SUMMARY_SYSTEM_PROMPT,
    SUMMARY_USER_TEMPLATE,
)
from error_handler import (
    retry_on_error,
    extract_json_from_text,
    validate_sentiment_result,
    safe_dict_get,
    ErrorStats,
    APIError,
    ParsingError,
    SearchError,
)
from aggregation import SentimentAggregator

# Load environment variables
load_dotenv()


@dataclass
class SentimentResult:
    """Structure for individual source sentiment"""

    source_url: str
    source_title: str
    sentiment: str  # "positive", "negative", "neutral", "mixed"
    confidence: float  # 0.0 to 1.0
    key_quote: str
    reasoning: str


@dataclass
class SentimentReport:
    """Final sentiment analysis report"""

    topic: str
    overall_sentiment: str
    confidence: float
    sources_analyzed: int
    positive_count: int
    negative_count: int
    neutral_count: int
    mixed_count: int
    key_findings: List[str]
    sources: List[SentimentResult]
    summary: str


class SentimentAgent:
    """
    Purple Agent that analyzes sentiment about a topic using FREE Groq API.

    Process:
    1. Generate search queries
    2. Execute web searches (Tavily)
    3. Analyze sentiment of each source (Groq)
    4. Aggregate results
    5. Generate final report
    """

    def __init__(
        self,
        model_name: str = "llama-3.3-70b-versatile",
        max_searches: int = 5,
        cache_enabled: bool = True,
    ):
        """Initialize the agent with FREE APIs"""
        # Initialize Groq client (FREE!)
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key:
            raise ValueError("GROQ_API_KEY not found in .env file!")
        self.llm = Groq(api_key=groq_key)
        self.model_name = model_name

        # Initialize search client (FREE tier: 1000/month)
        tavily_key = os.getenv("TAVILY_API_KEY")
        if not tavily_key:
            raise ValueError("TAVILY_API_KEY not found in .env file!")
        self.search_client = TavilyClient(api_key=tavily_key)

        # Configuration
        self.max_searches = max_searches
        self.cache_enabled = cache_enabled
        self.cache = {}

        # Track API calls (for monitoring)
        self.api_calls = 0
        self.searches_made = 0

        # Track Errors
        self.error_stats = ErrorStats()

    def analyze_topic(self, topic: str) -> SentimentReport:
        """
        Main entry point: analyze sentiment for a topic.

        Args:
            topic: The subject to analyze sentiment for

        Returns:
            SentimentReport with complete analysis
        """
        print(f"\n{'=' * 60}")
        print(f"Analyzing sentiment for: {topic}")
        print(f"Using FREE Groq API (Model: {self.model_name})")
        print(f"{'=' * 60}\n")

        # Step 1: Generate search queries
        queries = self._generate_search_queries(topic)
        print(f"✓ Generated {len(queries)} search queries")

        # Step 2: Search the web
        search_results = self._execute_searches(queries)
        print(f"✓ Found {len(search_results)} sources")

        # Step 3: Analyze each source
        sentiment_results = self._analyze_sources(topic, search_results)
        print(f"✓ Analyzed {len(sentiment_results)} sources")

        # Step 4: Aggregate and generate report
        report = self._generate_report(topic, sentiment_results)
        print(f"\n✓ Overall sentiment: {report.overall_sentiment.upper()}")
        print(f"✓ Confidence: {report.confidence:.0%}")
        print(f"✓ API calls: {self.api_calls} (all FREE!)")
        print(f"✓ Searches: {self.searches_made} (FREE tier)")

        return report

    @retry_on_error(max_retries=3, delay=1)
    def _generate_search_queries(self, topic: str) -> List[str]:
        """Generate queries with error handling"""

        self.error_stats.record_call()

        prompt = SEARCH_QUERY_USER_TEMPLATE.format(topic=topic)

        try:
            self.api_calls += 1

            response = self.llm.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SEARCH_QUERY_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.7,
                max_tokens=150,
            )

            queries_json = response.choices[0].message.content.strip()

            # Use robust JSON extraction
            queries = extract_json_from_text(queries_json)

            if not isinstance(queries, list):
                raise ParsingError("Expected list of queries")

            return queries[:3]

        except Exception as e:
            self.error_stats.record_error("query_generation")
            print(f"  ⚠️ Query generation error: {e}")
            # Fallback queries
            return [
                f"{topic} reviews opinions",
                f"{topic} positive feedback",
                f"{topic} criticism concerns",
            ]

    def _execute_searches(self, queries: List[str]) -> List[Dict]:
        """Execute searches with robust error handling"""
        all_results = []

        for query in queries[: self.max_searches]:
            # Check cache first
            if self.cache_enabled and query in self.cache:
                print(f"  [CACHED] {query}")
                all_results.extend(self.cache[query])
                continue

            try:
                print(f"  [SEARCH] {query}")
                self.searches_made += 1
                self.error_stats.record_call()

                response = self.search_client.search(
                    query=query, max_results=2, search_depth="basic"
                )

                results = []
                for result in response.get("results", []):
                    # Safely extract fields
                    url = safe_dict_get(result, "url", "unknown")
                    title = safe_dict_get(result, "title", "Untitled")
                    content = safe_dict_get(result, "content", "")

                    if url != "unknown" and content:
                        results.append(
                            {
                                "url": url,
                                "title": title,
                                "content": content[:1000],
                                "score": safe_dict_get(result, "score", 0, float),
                            }
                        )

                if self.cache_enabled:
                    self.cache[query] = results

                all_results.extend(results)

            except Exception as e:
                self.error_stats.record_error("search")
                print(f"  ⚠️ Search error for '{query}': {str(e)[:100]}")
                continue

        # Deduplicate
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result["url"] not in seen_urls:
                seen_urls.add(result["url"])
                unique_results.append(result)

        if not unique_results:
            self.error_stats.record_error("no_results")
            raise SearchError(f"No search results found for topic")

        return unique_results

    def _analyze_sources(
        self, topic: str, search_results: List[Dict]
    ) -> List[SentimentResult]:
        """Analyze sources, filtering out failures"""
        sentiment_results = []

        for i, result in enumerate(search_results, 1):
            print(
                f"  Analyzing source {i}/{len(search_results)}: {result['title'][:50]}..."
            )

            try:
                analysis = self._analyze_single_source(topic, result)
                if analysis is not None:  # Only add successful analyses
                    sentiment_results.append(analysis)
            except Exception as e:
                print(f"    ⚠️ Skipping source due to error: {str(e)[:100]}")
                continue

        if not sentiment_results:
            self.error_stats.record_error("all_analyses_failed")
            raise AgentError("Failed to analyze any sources")

        return sentiment_results

    def _analyze_single_source(
        self, topic: str, source: Dict
    ) -> Optional[SentimentResult]:
        """Analyze with comprehensive error handling"""

        prompt = SENTIMENT_ANALYSIS_USER_TEMPLATE.format(
            topic=topic, title=source["title"], content=source["content"]
        )

        max_retries = 3

        for attempt in range(max_retries):
            try:
                self.api_calls += 1
                self.error_stats.record_call()

                response = self.llm.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": SENTIMENT_ANALYSIS_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.2,
                    max_tokens=200,
                )

                analysis_json = response.choices[0].message.content.strip()

                # Robust JSON extraction
                analysis = extract_json_from_text(analysis_json)

                # Validate result
                if not validate_sentiment_result(analysis):
                    raise ParsingError("Invalid sentiment result format")

                # Safely extract fields with validation
                sentiment = analysis["sentiment"]
                confidence = max(0.0, min(1.0, float(analysis["confidence"])))
                key_quote = str(analysis["key_quote"])[:200]
                reasoning = str(analysis["reasoning"])[:200]

                return SentimentResult(
                    source_url=source["url"],
                    source_title=source["title"],
                    sentiment=sentiment,
                    confidence=confidence,
                    key_quote=key_quote,
                    reasoning=reasoning,
                )

            except Exception as e:
                self.error_stats.record_error("sentiment_analysis")

                if attempt < max_retries - 1:
                    self.error_stats.record_retry()
                    print(f"    Retry {attempt + 1}/{max_retries}")
                    time.sleep(1)
                    continue
                else:
                    print(f"    ⚠️ Analysis failed: {str(e)[:100]}")
                    # Return None instead of fallback - we'll filter these out
                    return None

    def _generate_report(
        self, topic: str, sentiment_results: List[SentimentResult]
    ) -> SentimentReport:
        """Generate report with advanced aggregation"""

        # Use advanced aggregation
        aggregation = SentimentAggregator.aggregate_advanced(sentiment_results)

        overall = aggregation["overall_sentiment"]
        confidence = aggregation["confidence"]
        is_controversial = aggregation["is_controversial"]
        distribution = aggregation["distribution"]

        # Count individual sentiments
        counts = {
            "positive": sum(1 for r in sentiment_results if r.sentiment == "positive"),
            "negative": sum(1 for r in sentiment_results if r.sentiment == "negative"),
            "neutral": sum(1 for r in sentiment_results if r.sentiment == "neutral"),
            "mixed": sum(1 for r in sentiment_results if r.sentiment == "mixed"),
        }

        # Extract key findings - prioritize high confidence results
        sorted_results = sorted(
            sentiment_results, key=lambda x: x.confidence, reverse=True
        )
        key_findings = []

        # Get top findings from each sentiment category
        sentiments_covered = set()
        for result in sorted_results:
            if result.sentiment not in sentiments_covered:
                key_findings.append(f"{result.sentiment.title()}: {result.key_quote}")
                sentiments_covered.add(result.sentiment)
            if len(key_findings) >= 3:
                break

        # Generate summary
        summary = self._generate_summary(topic, sentiment_results, overall)

        # Add controversy note if detected
        if is_controversial:
            summary += (
                " Note: This topic appears to be controversial with divided opinions."
            )

        return SentimentReport(
            topic=topic,
            overall_sentiment=overall,
            confidence=confidence,
            sources_analyzed=len(sentiment_results),
            positive_count=counts["positive"],
            negative_count=counts["negative"],
            neutral_count=counts["neutral"],
            mixed_count=counts["mixed"],
            key_findings=key_findings,
            sources=sentiment_results,
            summary=summary,
        )

    def _generate_summary(
        self, topic: str, results: List[SentimentResult], overall: str
    ) -> str:
        """Generate summary with improved prompts"""

        # Prepare context
        context_parts = []
        for r in results[:5]:  # Use top 5 sources
            context_parts.append(f"- {r.sentiment.upper()}: {r.reasoning}")
        context = "\n".join(context_parts)

        prompt = SUMMARY_USER_TEMPLATE.format(topic=topic, context=context)

        try:
            self.api_calls += 1

            response = self.llm.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": SUMMARY_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
                max_tokens=150,
            )

            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"  ⚠️ Summary generation failed: {e}")
            # Fallback summary
            pos = sum(1 for r in results if r.sentiment == "positive")
            neg = sum(1 for r in results if r.sentiment == "negative")

            if pos > neg:
                return f"Public sentiment about {topic} is predominantly positive based on {len(results)} sources analyzed."
            elif neg > pos:
                return f"Public sentiment about {topic} is predominantly negative based on {len(results)} sources analyzed."
            else:
                return f"Public sentiment about {topic} is mixed or neutral based on {len(results)} sources analyzed."


def main():
    """Test the agent with a sample topic"""
    print("\n" + "=" * 60)
    print("SENTIMENT ANALYSIS AGENT - FREE VERSION")
    print("Using Groq API (FREE) + Tavily Search (FREE)")
    print("=" * 60)

    agent = SentimentAgent()

    # Test topic
    topic = "iPhone 16"

    # Run analysis
    try:
        report = agent.analyze_topic(topic)

        # Print report
        print(f"\n{'=' * 60}")
        print(f"SENTIMENT ANALYSIS REPORT")
        print(f"{'=' * 60}")
        print(f"Topic: {report.topic}")
        print(f"Overall Sentiment: {report.overall_sentiment.upper()}")
        print(f"Confidence: {report.confidence:.1%}")
        print(f"\nBreakdown:")
        print(f"  Positive: {report.positive_count}")
        print(f"  Negative: {report.negative_count}")
        print(f"  Neutral: {report.neutral_count}")
        print(f"  Mixed: {report.mixed_count}")
        print(f"\nSummary:")
        print(f"  {report.summary}")
        print(f"\nKey Findings:")
        for finding in report.key_findings:
            print(f"  • {finding}")
        print(f"{'=' * 60}\n")

        # Save report to file
        output_file = f"../data/{topic.replace(' ', '_')}_report.json"
        with open(output_file, "w") as f:
            json.dump(
                {
                    "topic": report.topic,
                    "overall_sentiment": report.overall_sentiment,
                    "confidence": report.confidence,
                    "sources_analyzed": report.sources_analyzed,
                    "breakdown": {
                        "positive": report.positive_count,
                        "negative": report.negative_count,
                        "neutral": report.neutral_count,
                        "mixed": report.mixed_count,
                    },
                    "summary": report.summary,
                    "key_findings": report.key_findings,
                    "sources": [
                        {
                            "url": s.source_url,
                            "title": s.source_title,
                            "sentiment": s.sentiment,
                            "confidence": s.confidence,
                            "quote": s.key_quote,
                        }
                        for s in report.sources
                    ],
                },
                f,
                indent=2,
            )

        print(f"✓ Report saved to: {output_file}")
        print(f"✓ Total cost: $0.00 (Everything is FREE!)")
        print(f"✓ API calls made: {agent.api_calls}")
        print(f"✓ Searches made: {agent.searches_made}")

        # Print error statistics
        agent.error_stats.print_summary()

    except Exception as e:
        print(f"\n✗ FATAL ERROR: {e}")
        agent.error_stats.print_summary()
        raise


if __name__ == "__main__":
    main()

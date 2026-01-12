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
        cache_enabled: bool = True
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
        
    def analyze_topic(self, topic: str) -> SentimentReport:
        """
        Main entry point: analyze sentiment for a topic.
        
        Args:
            topic: The subject to analyze sentiment for
            
        Returns:
            SentimentReport with complete analysis
        """
        print(f"\n{'='*60}")
        print(f"Analyzing sentiment for: {topic}")
        print(f"Using FREE Groq API (Model: {self.model_name})")
        print(f"{'='*60}\n")
        
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
    
    def _generate_search_queries(self, topic: str) -> List[str]:
        """
        Generate diverse search queries for the topic.
        
        Strategy: Create queries that will find different perspectives
        """
        prompt = f"""Generate 3 diverse search queries to find public sentiment about: {topic}

Create queries that will find:
1. General opinions and reviews
2. Specific praise or positive reactions
3. Criticisms, complaints, or concerns

Return ONLY a JSON array of 3 search query strings, nothing else.
Example format: ["query 1", "query 2", "query 3"]"""

        try:
            self.api_calls += 1
            
            response = self.llm.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "You are a search query generator. Return only valid JSON arrays."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=150
            )
            
            # Parse JSON response
            queries_json = response.choices[0].message.content.strip()
            # Remove markdown code blocks if present
            queries_json = queries_json.replace('```json', '').replace('```', '').strip()
            queries = json.loads(queries_json)
            
            # Validate we got a list
            if not isinstance(queries, list):
                raise ValueError("Expected list of queries")
            
            return queries[:3]  # Ensure max 3 queries
            
        except Exception as e:
            print(f"  ⚠️ Error generating queries: {e}")
            print(f"  ⚠️ Using fallback queries")
            # Fallback: basic queries
            return [
                f"{topic} reviews",
                f"{topic} opinions",
                f"what people think about {topic}"
            ]
    
    def _execute_searches(self, queries: List[str]) -> List[Dict]:
        """
        Execute web searches for all queries.
        
        Returns list of search results with: url, title, content
        """
        all_results = []
        
        for query in queries[:self.max_searches]:
            # Check cache first
            if self.cache_enabled and query in self.cache:
                print(f"  [CACHED] {query}")
                all_results.extend(self.cache[query])
                continue
            
            try:
                print(f"  [SEARCH] {query}")
                self.searches_made += 1
                
                # Execute search via Tavily (FREE)
                response = self.search_client.search(
                    query=query,
                    max_results=2,  # Top 2 per query
                    search_depth="basic"
                )
                
                # Extract results
                results = []
                for result in response.get('results', []):
                    results.append({
                        'url': result.get('url'),
                        'title': result.get('title'),
                        'content': result.get('content', '')[:1000],  # Limit content length
                        'score': result.get('score', 0)
                    })
                
                # Cache results
                if self.cache_enabled:
                    self.cache[query] = results
                
                all_results.extend(results)
                
            except Exception as e:
                print(f"  ⚠️ Error searching '{query}': {e}")
                continue
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_results = []
        for result in all_results:
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                unique_results.append(result)
        
        return unique_results
    
    def _analyze_sources(
        self, 
        topic: str, 
        search_results: List[Dict]
    ) -> List[SentimentResult]:
        """
        Analyze sentiment of each source using Groq.
        """
        sentiment_results = []
        
        for i, result in enumerate(search_results, 1):
            print(f"  Analyzing source {i}/{len(search_results)}: {result['title'][:50]}...")
            
            try:
                # Analyze sentiment with Groq (FREE)
                analysis = self._analyze_single_source(topic, result)
                sentiment_results.append(analysis)
                
            except Exception as e:
                print(f"    ⚠️ Error analyzing source: {e}")
                continue
        
        return sentiment_results
    
    def _analyze_single_source(
        self, 
        topic: str, 
        source: Dict
    ) -> SentimentResult:
        """Analyze sentiment of a single source using Groq"""
        
        prompt = f"""Analyze the sentiment about "{topic}" in this text:

Title: {source['title']}
Content: {source['content']}

Determine:
1. Sentiment: positive, negative, neutral, or mixed
2. Confidence: 0.0 to 1.0 (how certain are you?)
3. Key quote: Extract the most relevant quote (max 100 chars)
4. Reasoning: Brief explanation (max 50 words)

Return ONLY valid JSON in this exact format (no markdown, no explanation):
{{
  "sentiment": "positive|negative|neutral|mixed",
  "confidence": 0.85,
  "key_quote": "exact quote from text",
  "reasoning": "brief explanation"
}}"""

        self.api_calls += 1
        
        response = self.llm.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a sentiment analysis expert. Return only valid JSON."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  # Lower temperature for consistency
            max_tokens=200
        )
        
        # Parse response
        analysis_json = response.choices[0].message.content.strip()
        # Remove markdown if present
        analysis_json = analysis_json.replace('```json', '').replace('```', '').strip()
        analysis = json.loads(analysis_json)
        
        # Create SentimentResult
        return SentimentResult(
            source_url=source['url'],
            source_title=source['title'],
            sentiment=analysis['sentiment'],
            confidence=float(analysis['confidence']),
            key_quote=analysis['key_quote'],
            reasoning=analysis['reasoning']
        )
    
    def _generate_report(
        self, 
        topic: str, 
        sentiment_results: List[SentimentResult]
    ) -> SentimentReport:
        """
        Aggregate individual sentiments into final report.
        """
        # Count sentiments
        counts = {
            'positive': 0,
            'negative': 0,
            'neutral': 0,
            'mixed': 0
        }
        
        for result in sentiment_results:
            if result.sentiment in counts:
                counts[result.sentiment] += 1
        
        # Determine overall sentiment
        total = len(sentiment_results)
        if total == 0:
            overall = "neutral"
            confidence = 0.0
        else:
            # Simple majority rule
            max_sentiment = max(counts, key=counts.get)
            overall = max_sentiment
            confidence = counts[max_sentiment] / total
        
        # Extract key findings
        key_findings = []
        for result in sentiment_results[:3]:  # Top 3 sources
            key_findings.append(f"{result.sentiment.title()}: {result.key_quote}")
        
        # Generate summary with Groq (FREE)
        summary = self._generate_summary(topic, sentiment_results, overall)
        
        return SentimentReport(
            topic=topic,
            overall_sentiment=overall,
            confidence=confidence,
            sources_analyzed=total,
            positive_count=counts['positive'],
            negative_count=counts['negative'],
            neutral_count=counts['neutral'],
            mixed_count=counts['mixed'],
            key_findings=key_findings,
            sources=sentiment_results,
            summary=summary
        )
    
    def _generate_summary(
        self, 
        topic: str, 
        results: List[SentimentResult],
        overall: str
    ) -> str:
        """Generate human-readable summary using Groq"""
        
        # Prepare context
        context = f"Topic: {topic}\nOverall Sentiment: {overall}\n\n"
        context += "Source Sentiments:\n"
        for r in results:
            context += f"- {r.sentiment}: {r.reasoning}\n"
        
        prompt = f"""{context}

Write a 2-3 sentence summary of the overall sentiment about {topic} based on these sources.
Be factual and balanced. Mention if there are divided opinions."""

        self.api_calls += 1
        
        response = self.llm.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": "You are a neutral analyst summarizing sentiment."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=150
        )
        
        return response.choices[0].message.content.strip()


def main():
    """Test the agent with a sample topic"""
    print("\n" + "="*60)
    print("SENTIMENT ANALYSIS AGENT - FREE VERSION")
    print("Using Groq API (FREE) + Tavily Search (FREE)")
    print("="*60)
    
    agent = SentimentAgent()
    
    # Test topic
    topic = "iPhone 16"
    
    # Run analysis
    report = agent.analyze_topic(topic)
    
    # Print report
    print(f"\n{'='*60}")
    print(f"SENTIMENT ANALYSIS REPORT")
    print(f"{'='*60}")
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
    print(f"{'='*60}\n")
    
    # Save report to file
    output_file = f"../data/{topic.replace(' ', '_')}_report.json"
    with open(output_file, 'w') as f:
        json.dump({
            'topic': report.topic,
            'overall_sentiment': report.overall_sentiment,
            'confidence': report.confidence,
            'sources_analyzed': report.sources_analyzed,
            'breakdown': {
                'positive': report.positive_count,
                'negative': report.negative_count,
                'neutral': report.neutral_count,
                'mixed': report.mixed_count
            },
            'summary': report.summary,
            'key_findings': report.key_findings,
            'sources': [
                {
                    'url': s.source_url,
                    'title': s.source_title,
                    'sentiment': s.sentiment,
                    'confidence': s.confidence,
                    'quote': s.key_quote
                }
                for s in report.sources
            ]
        }, f, indent=2)
    
    print(f"✓ Report saved to: {output_file}")
    print(f"✓ Total cost: $0.00 (Everything is FREE!)")
    print(f"✓ API calls made: {agent.api_calls}")
    print(f"✓ Searches made: {agent.searches_made}")


if __name__ == "__main__":
    main()
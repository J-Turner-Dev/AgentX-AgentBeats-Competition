"""
Green Agent (Evaluator) for Sentiment Analysis - COMPLETE VERSION
Fully integrated with ground truth and all test topics.
Ready for competition submission.
"""

import os
import json
import time
import requests
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import logging
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import test topics and ground truth
# These must be available in the container
try:
    from test_topics import TEST_TOPICS, FULL_TEST, STANDARD_TEST, QUICK_TEST
except ImportError:
    logger.warning("Could not import test_topics, will load from JSON")
    TEST_TOPICS = None
    FULL_TEST = None
    STANDARD_TEST = None
    QUICK_TEST = None

try:
    from ground_truth import get_ground_truth, calculate_accuracy
except ImportError:
    logger.warning("Could not import ground_truth, using fallback scoring")

    # Fallback implementations if ground_truth not available
    def get_ground_truth(topic: str) -> dict:
        """Fallback ground truth getter"""
        return {
            "verified_sentiment": "unknown",
            "confidence": 0.0,
            "notes": "No ground truth available",
        }

    def calculate_accuracy(predicted: str, topic: str) -> float:
        """Fallback accuracy calculator - returns 0.5 to indicate no ground truth"""
        return 0.5


@dataclass
class AssessmentResult:
    """Result from assessing a purple agent on one topic"""

    topic: str
    expected_sentiment: str
    actual_sentiment: str
    confidence: float
    sources_analyzed: int
    correct: bool
    accuracy_score: float
    time_taken: float
    category: str
    difficulty: str
    ground_truth_confidence: float
    details: Dict[str, Any]
    error: Optional[str] = None


class GreenAgent:
    """
    Green Agent - Complete Evaluator

    Uses ground truth data and full test suite for comprehensive evaluation.
    """

    def __init__(self, test_cases: Optional[List[Dict]] = None):
        """
        Initialize evaluator with test cases.

        Args:
            test_cases: List of test case dicts. If None, loads from file or imports.
        """
        self.test_cases = self._load_test_cases(test_cases)
        self.results = []
        self.start_time = None
        self.end_time = None

        logger.info(f"Green Agent initialized with {len(self.test_cases)} test cases")

    def _load_test_cases(self, test_cases: Optional[List[Dict]]) -> List[Dict]:
        """Load test cases from various sources"""

        # Priority 1: Provided test cases
        if test_cases is not None:
            return test_cases

        # Priority 2: Load from JSON file
        if os.path.exists("test_cases.json"):
            logger.info("Loading test cases from test_cases.json")
            with open("test_cases.json", "r") as f:
                data = json.load(f)
                return data.get("test_cases", data)

        # Priority 3: Import from Python module
        if TEST_TOPICS is not None:
            logger.info("Using imported TEST_TOPICS")
            # Use STANDARD_TEST by default (good balance)
            return STANDARD_TEST if STANDARD_TEST else TEST_TOPICS

        # Fallback: Create minimal test set
        logger.warning("No test cases found, using minimal fallback")
        return [
            {
                "topic": "iPhone 16",
                "expected_sentiment": "positive",
                "category": "technology",
                "difficulty": "easy",
                "reasoning": "New Apple products generally positive",
            }
        ]

    def assess_purple_agent(
        self, agent_url: str, timeout: int = 120, max_retries: int = 3
    ) -> List[AssessmentResult]:
        """
        Assess a purple agent on all test cases.

        Args:
            agent_url: URL of purple agent's A2A endpoint
            timeout: Maximum time per assessment in seconds
            max_retries: Number of retries for failed assessments

        Returns:
            List of assessment results
        """

        self.start_time = time.time()

        logger.info("=" * 60)
        logger.info("STARTING ASSESSMENT")
        logger.info("=" * 60)
        logger.info(f"Purple agent: {agent_url}")
        logger.info(f"Test cases: {len(self.test_cases)}")
        logger.info(f"Timeout per test: {timeout}s")
        logger.info("=" * 60)

        results = []

        for i, test_case in enumerate(self.test_cases, 1):
            logger.info(f"\n[{i}/{len(self.test_cases)}] Testing: {test_case['topic']}")
            logger.info(f"  Expected: {test_case['expected_sentiment']}")
            logger.info(f"  Category: {test_case.get('category', 'unknown')}")
            logger.info(f"  Difficulty: {test_case.get('difficulty', 'medium')}")

            result = None
            for attempt in range(max_retries):
                try:
                    result = self._assess_single_task(agent_url, test_case, timeout)
                    break
                except Exception as e:
                    if attempt < max_retries - 1:
                        logger.warning(
                            f"  Attempt {attempt + 1} failed: {e}, retrying..."
                        )
                        time.sleep(2)
                    else:
                        logger.error(f"  All {max_retries} attempts failed: {e}")
                        result = self._create_error_result(test_case, str(e))

            if result:
                results.append(result)

                status = "✓" if result.correct else "✗"
                logger.info(
                    f"  {status} Got: {result.actual_sentiment} (confidence: {result.confidence:.0%})"
                )
                logger.info(f"  Accuracy score: {result.accuracy_score:.2f}")
                logger.info(f"  Time: {result.time_taken:.1f}s")

                if result.error:
                    logger.error(f"  Error: {result.error}")

        self.end_time = time.time()
        self.results = results

        logger.info("\n" + "=" * 60)
        logger.info("ASSESSMENT COMPLETE")
        logger.info("=" * 60)
        logger.info(f"Total time: {self.end_time - self.start_time:.1f}s")
        logger.info(f"Results: {len(results)}/{len(self.test_cases)}")

        return results

    def _assess_single_task(
        self, agent_url: str, test_case: Dict, timeout: int
    ) -> AssessmentResult:
        """Assess purple agent on a single task with ground truth scoring"""

        # Get ground truth data
        gt = get_ground_truth(test_case["topic"])
        gt_confidence = gt.get("confidence", 0.0)

        # Prepare A2A request
        request_data = {
            "task": f"Analyze sentiment for: {test_case['topic']}",
            "config": {"max_time": timeout, "return_details": True},
        }

        # Send request to purple agent
        start_time = time.time()

        response = requests.post(
            f"{agent_url}/assess",
            json=request_data,
            headers={"Content-Type": "application/json"},
            timeout=timeout + 10,  # Add buffer
        )

        elapsed = time.time() - start_time

        # Parse response
        if response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

        data = response.json()

        if not data.get("success"):
            raise Exception(f"Assessment failed: {data.get('error', 'Unknown error')}")

        result_data = data["result"]

        # Calculate accuracy using ground truth
        accuracy_score = calculate_accuracy(
            result_data["sentiment"], test_case["topic"]
        )

        # If no ground truth available, use simple matching
        if accuracy_score == 0.5:  # Indicates no ground truth
            accuracy_score = self._calculate_score(
                expected=test_case["expected_sentiment"],
                actual=result_data["sentiment"],
                confidence=result_data["confidence"],
            )

        correct = result_data["sentiment"] == test_case["expected_sentiment"]

        return AssessmentResult(
            topic=test_case["topic"],
            expected_sentiment=test_case["expected_sentiment"],
            actual_sentiment=result_data["sentiment"],
            confidence=result_data["confidence"],
            sources_analyzed=result_data.get("sources_analyzed", 0),
            correct=correct,
            accuracy_score=accuracy_score,
            time_taken=elapsed,
            category=test_case.get("category", "unknown"),
            difficulty=test_case.get("difficulty", "medium"),
            ground_truth_confidence=gt_confidence,
            details=result_data,
        )

    def _create_error_result(self, test_case: Dict, error: str) -> AssessmentResult:
        """Create error result for failed assessment"""
        return AssessmentResult(
            topic=test_case["topic"],
            expected_sentiment=test_case["expected_sentiment"],
            actual_sentiment="error",
            confidence=0.0,
            sources_analyzed=0,
            correct=False,
            accuracy_score=0.0,
            time_taken=0.0,
            category=test_case.get("category", "unknown"),
            difficulty=test_case.get("difficulty", "medium"),
            ground_truth_confidence=0.0,
            details={"error": error},
            error=error,
        )

    def _calculate_score(self, expected: str, actual: str, confidence: float) -> float:
        """
        Calculate score when ground truth unavailable.
        Fallback scoring method.
        """
        if expected == actual:
            return 1.0

        close_matches = {
            ("mixed", "neutral"): 0.6,
            ("neutral", "mixed"): 0.6,
        }

        partial_matches = {
            ("positive", "mixed"): 0.4,
            ("negative", "mixed"): 0.4,
            ("mixed", "positive"): 0.3,
            ("mixed", "negative"): 0.3,
        }

        key = (expected, actual)

        if key in close_matches:
            return close_matches[key]
        if key in partial_matches:
            return partial_matches[key]

        return 0.0

    def generate_report(self) -> Dict[str, Any]:
        """Generate comprehensive assessment report"""

        if not self.results:
            return {"error": "No results available", "summary": {}, "results": []}

        total = len(self.results)
        successful = sum(1 for r in self.results if r.error is None)
        correct = sum(1 for r in self.results if r.correct)
        total_score = sum(r.accuracy_score for r in self.results)
        avg_time = sum(r.time_taken for r in self.results) / total
        avg_confidence = sum(
            r.confidence for r in self.results if r.error is None
        ) / max(successful, 1)

        # By category
        by_category = {}
        for result in self.results:
            cat = result.category
            if cat not in by_category:
                by_category[cat] = {"total": 0, "correct": 0, "scores": [], "times": []}
            by_category[cat]["total"] += 1
            if result.correct:
                by_category[cat]["correct"] += 1
            by_category[cat]["scores"].append(result.accuracy_score)
            by_category[cat]["times"].append(result.time_taken)

        # By difficulty
        by_difficulty = {}
        for result in self.results:
            diff = result.difficulty
            if diff not in by_difficulty:
                by_difficulty[diff] = {"total": 0, "correct": 0, "scores": []}
            by_difficulty[diff]["total"] += 1
            if result.correct:
                by_difficulty[diff]["correct"] += 1
            by_difficulty[diff]["scores"].append(result.accuracy_score)

        # Calculate category stats
        category_stats = {}
        for cat, data in by_category.items():
            category_stats[cat] = {
                "accuracy": data["correct"] / data["total"],
                "average_score": sum(data["scores"]) / len(data["scores"]),
                "average_time": sum(data["times"]) / len(data["times"]),
                "total_tests": data["total"],
            }

        # Calculate difficulty stats
        difficulty_stats = {}
        for diff, data in by_difficulty.items():
            difficulty_stats[diff] = {
                "accuracy": data["correct"] / data["total"],
                "average_score": sum(data["scores"]) / len(data["scores"]),
                "total_tests": data["total"],
            }

        return {
            "summary": {
                "total_tests": total,
                "successful_tests": successful,
                "failed_tests": total - successful,
                "correct": correct,
                "accuracy": correct / total,
                "average_score": total_score / total,
                "average_time": avg_time,
                "average_confidence": avg_confidence,
                "total_time": self.end_time - self.start_time if self.end_time else 0,
                "pass_rate": correct / total,  # For AgentBeats compatibility
            },
            "by_category": category_stats,
            "by_difficulty": difficulty_stats,
            "results": [
                {
                    "topic": r.topic,
                    "expected": r.expected_sentiment,
                    "actual": r.actual_sentiment,
                    "correct": r.correct,
                    "score": r.accuracy_score,
                    "confidence": r.confidence,
                    "time": r.time_taken,
                    "category": r.category,
                    "difficulty": r.difficulty,
                    "sources": r.sources_analyzed,
                    "ground_truth_confidence": r.ground_truth_confidence,
                    "error": r.error,
                }
                for r in self.results
            ],
        }

    def save_results(self, output_file: str = "results.json"):
        """Save results in AgentBeats-compatible format"""

        report = self.generate_report()

        # AgentBeats format
        agentbeats_result = {
            "participants": {"agent": os.getenv("PURPLE_AGENT_ID", "unknown-agent")},
            "results": [
                {
                    "pass_rate": report["summary"]["pass_rate"],
                    "time_used": report["summary"]["average_time"],
                    "max_score": 1.0,
                    "details": report,
                }
            ],
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "total_tasks": report["summary"]["total_tests"],
                "evaluator": "sentiment-analysis-green-agent",
                "version": "1.0.0",
            },
        }

        # Ensure output directory exists
        os.makedirs(
            os.path.dirname(output_file) if os.path.dirname(output_file) else ".",
            exist_ok=True,
        )

        with open(output_file, "w") as f:
            json.dump(agentbeats_result, f, indent=2)

        logger.info(f"Results saved to: {output_file}")

        return output_file


def main():
    """Main entry point for green agent"""

    # Get configuration from environment
    purple_agent_url = os.getenv("PURPLE_AGENT_URL", "http://localhost:8000")
    output_file = os.getenv("OUTPUT_FILE", "/app/output/results.json")
    timeout = int(os.getenv("ASSESSMENT_TIMEOUT", "120"))

    logger.info("\n" + "=" * 60)
    logger.info("SENTIMENT ANALYSIS GREEN AGENT")
    logger.info("=" * 60)
    logger.info(f"Purple agent URL: {purple_agent_url}")
    logger.info(f"Output file: {output_file}")
    logger.info(f"Timeout: {timeout}s")
    logger.info("=" * 60 + "\n")

    # Create green agent
    green_agent = GreenAgent()

    # Run assessment
    try:
        results = green_agent.assess_purple_agent(purple_agent_url, timeout=timeout)

        # Generate and print report
        report = green_agent.generate_report()

        logger.info("\n" + "=" * 60)
        logger.info("FINAL REPORT")
        logger.info("=" * 60)
        logger.info(f"Total tests: {report['summary']['total_tests']}")
        logger.info(f"Successful: {report['summary']['successful_tests']}")
        logger.info(f"Correct: {report['summary']['correct']}")
        logger.info(f"Accuracy: {report['summary']['accuracy']:.1%}")
        logger.info(f"Average score: {report['summary']['average_score']:.3f}")
        logger.info(f"Average time: {report['summary']['average_time']:.1f}s")
        logger.info(
            f"Average confidence: {report['summary']['average_confidence']:.1%}"
        )
        logger.info(f"Total time: {report['summary']['total_time']:.1f}s")

        logger.info("\nBy Category:")
        for cat, stats in report["by_category"].items():
            logger.info(
                f"  {cat}: {stats['accuracy']:.1%} ({stats['total_tests']} tests)"
            )

        logger.info("\nBy Difficulty:")
        for diff, stats in report["by_difficulty"].items():
            logger.info(
                f"  {diff}: {stats['accuracy']:.1%} ({stats['total_tests']} tests)"
            )

        logger.info("=" * 60 + "\n")

        # Save results
        green_agent.save_results(output_file)

        logger.info("✅ Assessment complete!")
        sys.exit(0)

    except Exception as e:
        logger.error(f"❌ Assessment failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

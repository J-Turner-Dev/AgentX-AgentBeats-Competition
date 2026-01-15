"""
Robust error handling for API calls and parsing.
"""

import time
import json
import re
from typing import Callable, Any, Optional
from functools import wraps


class AgentError(Exception):
    """Base exception for agent errors"""

    pass


class APIError(AgentError):
    """API call failed"""

    pass


class ParsingError(AgentError):
    """Failed to parse API response"""

    pass


class SearchError(AgentError):
    """Search returned no results"""

    pass


def retry_on_error(max_retries=3, delay=1, backoff=2):
    """Decorator for retrying functions on error"""

    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None

            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e

                    if attempt < max_retries - 1:
                        wait_time = delay * (backoff**attempt)
                        print(
                            f"    Retry {attempt + 1}/{max_retries} after {wait_time}s..."
                        )
                        time.sleep(wait_time)
                    else:
                        print(f"    All retries failed: {str(e)[:100]}")

            raise last_exception

        return wrapper

    return decorator


def extract_json_from_text(text: str) -> dict:
    """
    Extract JSON from text that might have markdown or other formatting.
    Tries multiple strategies.
    """
    # Strategy 1: Clean and parse directly
    text = text.strip()
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Strategy 2: Find JSON object with regex
    json_pattern = r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}"
    matches = re.findall(json_pattern, text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    # Strategy 3: Try to find array
    array_pattern = r"\[[^\[\]]*(?:\[[^\[\]]*\][^\[\]]*)*\]"
    matches = re.findall(array_pattern, text, re.DOTALL)

    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue

    raise ParsingError(f"Could not extract valid JSON from: {text[:200]}")


def validate_sentiment_result(data: dict) -> bool:
    """Validate sentiment analysis result has required fields"""
    required_fields = ["sentiment", "confidence", "key_quote", "reasoning"]

    if not all(field in data for field in required_fields):
        return False

    valid_sentiments = ["positive", "negative", "neutral", "mixed"]
    if data["sentiment"] not in valid_sentiments:
        return False

    try:
        confidence = float(data["confidence"])
        if not 0 <= confidence <= 1:
            return False
    except (ValueError, TypeError):
        return False

    return True


def safe_dict_get(
    data: dict, key: str, default: Any = None, converter: Optional[Callable] = None
) -> Any:
    """Safely get value from dict with optional type conversion"""
    try:
        value = data.get(key, default)
        if converter and value is not None:
            return converter(value)
        return value
    except Exception:
        return default


class ErrorStats:
    """Track error statistics"""

    def __init__(self):
        self.total_calls = 0
        self.errors = {}
        self.retries = 0

    def record_call(self):
        self.total_calls += 1

    def record_error(self, error_type: str):
        self.errors[error_type] = self.errors.get(error_type, 0) + 1

    def record_retry(self):
        self.retries += 1

    def get_error_rate(self) -> float:
        if self.total_calls == 0:
            return 0.0
        total_errors = sum(self.errors.values())
        return total_errors / self.total_calls

    def print_summary(self):
        print(f"\n{'=' * 60}")
        print("ERROR STATISTICS")
        print(f"{'=' * 60}")
        print(f"Total API calls: {self.total_calls}")
        print(f"Total errors: {sum(self.errors.values())}")
        print(f"Total retries: {self.retries}")
        print(f"Error rate: {self.get_error_rate():.1%}")

        if self.errors:
            print("\nErrors by type:")
            for error_type, count in sorted(
                self.errors.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"  {error_type}: {count}")
        print(f"{'=' * 60}\n")

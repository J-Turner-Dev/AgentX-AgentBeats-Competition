"""
A2A Protocol Server for Purple Agent (Sentiment Analysis)
This makes your purple agent compatible with AgentBeats.
"""

import os
import json
import time
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import logging

# Import your existing sentiment agent
from purple_agent import SentimentAgent

# Load environment
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Initialize sentiment agent
sentiment_agent = SentimentAgent()


# Health check endpoint
@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify(
        {
            "status": "healthy",
            "service": "sentiment-analysis-purple-agent",
            "version": "1.0.0",
        }
    ), 200


# A2A Assessment endpoint
@app.route("/assess", methods=["POST"])
def assess():
    """
    A2A Protocol Assessment Endpoint

    Receives assessment request, runs sentiment analysis, returns results.

    Request format:
    {
        "task": "Analyze sentiment for: ",
        "config": {
            "max_time": 60,
            "return_details": true
        }
    }

    Response format:
    {
        "result": {
            "topic": "...",
            "sentiment": "positive|negative|neutral|mixed",
            "confidence": 0.85,
            "sources_analyzed": 6,
            "breakdown": {...},
            "summary": "...",
            "key_findings": [...]
        },
        "success": true,
        "time_taken": 32.5,
        "error": null
    }
    """

    try:
        # Parse request
        data = request.get_json()

        if not data or "task" not in data:
            return jsonify(
                {"success": False, "error": "Missing required field: task"}
            ), 400

        # Extract topic from task
        task = data["task"]
        config = data.get("config", {})

        logger.info(f"Received assessment request: {task}")

        # Parse topic from task string
        # Expected format: "Analyze sentiment for: "
        topic = extract_topic(task)

        if not topic:
            return jsonify(
                {"success": False, "error": "Could not extract topic from task"}
            ), 400

        # Run sentiment analysis
        start_time = time.time()

        try:
            report = sentiment_agent.analyze_topic(topic)
            elapsed_time = time.time() - start_time

            # Format response according to A2A protocol
            response = {
                "result": {
                    "topic": report.topic,
                    "sentiment": report.overall_sentiment,
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
                },
                "success": True,
                "time_taken": elapsed_time,
                "error": None,
            }

            logger.info(f"Assessment completed: {topic} -> {report.overall_sentiment}")

            return jsonify(response), 200

        except Exception as e:
            elapsed_time = time.time() - start_time
            logger.error(f"Assessment failed: {str(e)}")

            return jsonify(
                {
                    "result": None,
                    "success": False,
                    "time_taken": elapsed_time,
                    "error": str(e),
                }
            ), 500

    except Exception as e:
        logger.error(f"Request processing failed: {str(e)}")
        return jsonify(
            {"success": False, "error": f"Internal server error: {str(e)}"}
        ), 500


def extract_topic(task: str) -> str:
    """
    Extract topic from task string.

    Examples:
    - "Analyze sentiment for: iPhone 16" -> "iPhone 16"
    - "iPhone 16" -> "iPhone 16"
    """

    # Try to extract from standard format
    if ":" in task:
        parts = task.split(":", 1)
        return parts[1].strip()

    # Fallback: use entire task as topic
    return task.strip()


# Root endpoint
@app.route("/", methods=["GET"])
def root():
    """Root endpoint with API documentation"""
    return jsonify(
        {
            "service": "Sentiment Analysis Purple Agent",
            "version": "1.0.0",
            "protocol": "A2A",
            "endpoints": {"health": "GET /health", "assess": "POST /assess"},
            "documentation": {
                "assess_request": {
                    "task": "Analyze sentiment for: ",
                    "config": {"max_time": 60, "return_details": True},
                },
                "assess_response": {
                    "result": {
                        "topic": "string",
                        "sentiment": "positive|negative|neutral|mixed",
                        "confidence": "float",
                        "sources_analyzed": "int",
                    },
                    "success": "boolean",
                    "time_taken": "float",
                },
            },
        }
    ), 200


def main():
    """Run the A2A server"""
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting A2A server on {host}:{port}")

    # Use waitress for production-ready server
    from waitress import serve

    serve(app, host=host, port=port, threads=4)


if __name__ == "__main__":
    main()

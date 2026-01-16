FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt* ./

# Install Python dependencies
RUN pip install --no-cache-dir requests python-dotenv

# Copy green agent code
COPY green_agent.py .

# Copy test suite files (these will come from parent directory in build context)
COPY test_topics.py* ./
COPY ground_truth.py* ./
COPY test_cases.json* ./

# Create output directory
RUN mkdir -p /app/output

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PURPLE_AGENT_URL=http://purple-agent:8000
ENV OUTPUT_FILE=/app/output/results.json
ENV ASSESSMENT_TIMEOUT=120

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)"

# Run the green agent
CMD ["python", "green_agent.py"]
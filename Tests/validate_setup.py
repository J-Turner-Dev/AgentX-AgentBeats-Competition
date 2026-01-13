"""
Validate that everything is set up correctly before starting.
Run this first to catch any issues!
"""

import os
import sys
from pathlib import Path


def validate_setup():
    """Check all prerequisites"""
    print("\n" + "=" * 60)
    print("VALIDATING SETUP")
    print("=" * 60 + "\n")

    issues = []
    warnings = []

    # 1. Check Python version
    version = sys.version_info
    if version.major == 3 and version.minor >= 10:
        print(
            "✓ Python version OK:", f"{version.major}.{version.minor}.{version.micro}"
        )
    else:
        issues.append(
            f"✗ Python version too old: {version.major}.{version.minor}, need 3.10+"
        )

    # 2. Load environment variables
    from dotenv import load_dotenv

    env_path = Path("../.env")
    if env_path.exists():
        print("✓ .env file found")
        load_dotenv(dotenv_path=env_path)
    else:
        issues.append("✗ .env file not found in parent directory")

    # 3. Check API keys
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key.startswith("gsk_"):
        print("✓ Groq API key found (starts with gsk_)")
    elif groq_key:
        warnings.append(
            "⚠ Groq API key found but doesn't start with 'gsk_' - might be invalid"
        )
    else:
        issues.append("✗ GROQ_API_KEY missing in .env file")

    tavily_key = os.getenv("TAVILY_API_KEY")
    if tavily_key and tavily_key.startswith("tvly-"):
        print("✓ Tavily API key found (starts with tvly-)")
    elif tavily_key:
        warnings.append(
            "⚠ Tavily API key found but doesn't start with 'tvly-' - might be invalid"
        )
    else:
        issues.append("✗ TAVILY_API_KEY missing in .env file")

    # 4. Check required packages
    packages = {
        "groq": "Groq API client",
        "tavily": "Tavily search client",
        "flask": "Web framework",
        "dotenv": "Environment variables",
        "pydantic": "Data validation",
    }

    for package, description in packages.items():
        try:
            __import__(package if package != "dotenv" else "dotenv")
            print(f"✓ {description} ({package}) installed")
        except ImportError:
            issues.append(f"✗ {description} ({package}) not installed")

    # 5. Check directory structure
    paths_to_check = [
        ("../PurpleAgent", "purple-agent directory"),
        ("../PurpleAgent/purple_agent.py", "purple_agent.py file"),
        ("../GreenAgent", "green-agent directory"),
        ("../Data", "data directory"),
        ("../Tests", "tests directory"),
    ]

    for path, description in paths_to_check:
        if Path(path).exists():
            print(f"✓ {description} exists")
        else:
            warnings.append(f"⚠ {description} not found at {path}")

    # 6. Test API connections (optional but helpful)
    print("\nTesting API connections...")

    try:
        from groq import Groq

        if groq_key:
            client = Groq(api_key=groq_key)
            # Try a minimal API call
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": "Say 'test'"}],
                max_tokens=5,
            )
            print("✓ Groq API connection successful")
    except Exception as e:
        issues.append(f"✗ Groq API connection failed: {str(e)[:100]}")

    try:
        from tavily import TavilyClient

        if tavily_key:
            client = TavilyClient(api_key=tavily_key)
            # Try a minimal search
            response = client.search(query="test", max_results=1)
            print("✓ Tavily API connection successful")
    except Exception as e:
        issues.append(f"✗ Tavily API connection failed: {str(e)[:100]}")

    # Summary
    print(f"\n{'=' * 60}")
    if issues:
        print("❌ SETUP INCOMPLETE")
        print(f"{'=' * 60}")
        for issue in issues:
            print(issue)
        if warnings:
            print("\nWarnings:")
            for warning in warnings:
                print(warning)
        print("\n⚠️ Fix these issues before proceeding.")
        return False
    elif warnings:
        print("⚠️ SETUP COMPLETE WITH WARNINGS")
        print(f"{'=' * 60}")
        for warning in warnings:
            print(warning)
        print("\n✓ You can proceed, but check warnings above.")
        return True
    else:
        print("✅ SETUP COMPLETE")
        print(f"{'=' * 60}")
        print("All prerequisites met! Ready to run agent.")
        print("\nNext steps:")
        print("1. cd ../purple-agent")
        print("2. python purple_agent.py")
        return True


if __name__ == "__main__":
    success = validate_setup()
    sys.exit(0 if success else 1)

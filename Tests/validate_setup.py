"""
Quick validation that everything is set up correctly.
Run this before starting development to catch issues early.
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
        print(f"✓ Python version OK: {version.major}.{version.minor}.{version.micro}")
    else:
        issues.append(
            f"✗ Python version too old: {version.major}.{version.minor}, need 3.10+"
        )

    # 2. Check directory structure
    project_root = Path(__file__).parent.parent

    required_dirs = ["PurpleAgent", "Tests", "Data"]

    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ Directory exists: {dir_name}/")
        else:
            issues.append(f"✗ Missing directory: {dir_name}/")

    # 3. Check required files
    required_files = ["PurpleAgent/purple_agent.py", "tests/test_topics.py", ".env"]

    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"✓ File exists: {file_path}")
        else:
            issues.append(f"✗ Missing file: {file_path}")

    # 4. Check .env file and API keys
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv

            load_dotenv(env_file)

            groq_key = os.getenv("GROQ_API_KEY")
            if groq_key and groq_key.startswith("gsk_"):
                print("✓ Groq API key found (FREE!)")
            elif groq_key:
                warnings.append("⚠️ Groq API key found but doesn't start with 'gsk_'")
            else:
                issues.append("✗ Groq API key missing in .env")

            tavily_key = os.getenv("TAVILY_API_KEY")
            if tavily_key and tavily_key.startswith("tvly"):
                print("✓ Tavily API key found (FREE!)")
            elif tavily_key:
                warnings.append("⚠️ Tavily API key found but doesn't start with 'tvly'")
            else:
                issues.append("✗ Tavily API key missing in .env")

            model_name = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
            print(f"✓ Model configured: {model_name}")
        except ImportError:
            issues.append("✗ python-dotenv not installed (pip install python-dotenv)")
    else:
        issues.append("✗ .env file missing")

    # 5. Check Python packages
    required_packages = [
        ("openai", "openai (for Groq compatibility)"),
        ("tavily", "tavily-python"),
        ("flask", "flask"),
        ("dotenv", "python-dotenv"),
        ("pydantic", "pydantic"),
    ]

    print("\nChecking required packages:")
    for package_name, display_name in required_packages:
        try:
            if package_name == "dotenv":
                import python_dotenv

                print(f"✓ Package installed: {display_name}")
            else:
                __import__(package_name)
                print(f"✓ Package installed: {display_name}")
        except ImportError:
            issues.append(f"✗ Package missing: {display_name}")

    # 6. Test Groq API connectivity (using OpenAI library)
    print("\nTesting API connectivity...")

    try:
        from openai import OpenAI

        groq_key = os.getenv("GROQ_API_KEY")
        if groq_key:
            # Connect to Groq via OpenAI-compatible API
            client = OpenAI(api_key=groq_key, base_url="https://api.groq.com/openai/v1")
            # Try to list models (lightweight test)
            models = client.models.list()
            print(
                f"✓ Groq API accessible (FREE! - {len(models.data)} models available)"
            )

            # Show available models
            print("  Available models:")
            for model in models.data:
                if (
                    "llama" in model.id.lower()
                    or "mixtral" in model.id.lower()
                    or "gemma" in model.id.lower()
                ):
                    print(f"    - {model.id}")
        else:
            warnings.append("⚠️ Skipping Groq API test (no key)")
    except Exception as e:
        warnings.append(f"⚠️ Groq API test failed: {str(e)[:80]}")

    try:
        from tavily import TavilyClient

        tavily_key = os.getenv("TAVILY_API_KEY")
        if tavily_key:
            client = TavilyClient(api_key=tavily_key)
            # Try a simple search
            result = client.search(query="test", max_results=1)
            print("✓ Tavily API accessible (FREE!)")
        else:
            warnings.append("⚠️ Skipping Tavily API test (no key)")
    except Exception as e:
        warnings.append(f"⚠️ Tavily API test failed: {str(e)[:80]}")

    # Summary
    print(f"\n{'=' * 60}")

    if not issues and not warnings:
        print("✅ SETUP COMPLETE - ALL CHECKS PASSED!")
        print(f"{'=' * 60}")
        print("\n🎉 Everything is configured correctly!")
        print("   Using FREE APIs: Groq + Tavily")
        print("   Total cost: $0.00")
        print("\nYou're ready to start building! 🚀")
        print("\nNext steps:")
        print("  1. cd PurpleAgent")
        print("  2. python purple_agent.py")
        print("  3. cd ../tests")
        print("  4. python test_agent.py")
        return True
    elif not issues:
        print("✅ SETUP MOSTLY COMPLETE")
        print(f"{'=' * 60}")
        print("\n⚠️ Warnings (non-critical):")
        for warning in warnings:
            print(f"  {warning}")
        print("\nYou can proceed, but fix warnings when possible.")
        return True
    else:
        print("❌ SETUP INCOMPLETE")
        print(f"{'=' * 60}")
        print("\n❌ Critical issues:")
        for issue in issues:
            print(f"  {issue}")
        if warnings:
            print("\n⚠️ Warnings:")
            for warning in warnings:
                print(f"  {warning}")
        print("\n🔧 Fix these issues before proceeding:")
        print("  1. Make sure you have .env file with API keys")
        print("  2. Run: pip install -r requirements.txt")
        print("  3. Verify directory structure matches project layout")
        return False


if __name__ == "__main__":
    success = validate_setup()
    sys.exit(0 if success else 1)

#!/usr/bin/env python3
"""
Perplexity API Setup Diagnostic Script
=====================================

Diagnoses common issues with Perplexity API setup:
1. Missing API key
2. Invalid API key format
3. Network connectivity
4. chuk_llm configuration
5. MCP tool setup

Run this to troubleshoot your Perplexity integration.
"""

import asyncio
import logging
import os
import sys
import time
from pathlib import Path

# Load .env file at the very beginning
try:
    from dotenv import load_dotenv

    load_dotenv()  # Load .env file
    print("🔄 Loaded .env file")
except ImportError:
    print("⚠️  python-dotenv not available, .env file not loaded")
except Exception as e:
    print(f"⚠️  Error loading .env file: {e}")

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def check_environment_setup():
    """Check environment variables and configuration."""
    print("🔧 Environment Setup Check")
    print("=" * 40)

    issues = []

    # Check for .env file
    env_files = [".env", ".env.local", Path.home() / ".env"]
    env_file_found = None
    for env_file in env_files:
        if Path(env_file).exists():
            print(f"✅ Found .env file: {env_file}")
            env_file_found = env_file
            break

    if not env_file_found:
        print("⚠️  No .env file found in current directory or home")
        issues.append("Consider creating a .env file for API keys")
    else:
        # Show .env file contents (safely)
        try:
            with open(env_file_found, "r") as f:
                content = f.read()
                if "PERPLEXITY_API_KEY" in content:
                    print(f"✅ PERPLEXITY_API_KEY found in {env_file_found}")
                else:
                    print(f"⚠️  PERPLEXITY_API_KEY not found in {env_file_found}")
        except Exception as e:
            print(f"⚠️  Could not read .env file: {e}")

    # Check API key in environment
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("❌ PERPLEXITY_API_KEY environment variable not set")
        issues.append("PERPLEXITY_API_KEY is required")
        print("\n📝 To fix this:")
        print("   1. Get API key from: https://www.perplexity.ai/settings/api")
        print("   2. Add to .env file: PERPLEXITY_API_KEY=your_key_here")
        print("   3. Or export: export PERPLEXITY_API_KEY=your_key_here")

        # Try to reload .env file
        print("\n🔄 Attempting to reload .env file...")
        try:
            from dotenv import load_dotenv

            load_dotenv(override=True)
            api_key_after_reload = os.getenv("PERPLEXITY_API_KEY")
            if api_key_after_reload:
                print("✅ Found API key after reload!")
                api_key = api_key_after_reload
                issues = [i for i in issues if "PERPLEXITY_API_KEY" not in i]
            else:
                print("❌ Still no API key after reload")
        except ImportError:
            print("⚠️  python-dotenv not available for reload")
    else:
        # Check API key format
        if api_key.startswith("pplx-"):
            print("✅ PERPLEXITY_API_KEY found and has correct format (pplx-...)")
            print(f"   Key length: {len(api_key)} characters")
        else:
            print("⚠️  PERPLEXITY_API_KEY found but may have incorrect format")
            print("   Expected: pplx-... format")
            print(f"   Got: {api_key[:10]}...")
            issues.append("API key format may be incorrect")

    return len(issues) == 0, issues


def check_chuk_llm_installation():
    """Check chuk_llm installation and configuration."""
    print("\n📦 chuk_llm Installation Check")
    print("=" * 40)

    issues = []

    try:
        import chuk_llm

        print("✅ chuk_llm module imported successfully")

        # Check version if available
        if hasattr(chuk_llm, "__version__"):
            print(f"   Version: {chuk_llm.__version__}")

    except ImportError as e:
        print(f"❌ Failed to import chuk_llm: {e}")
        issues.append("chuk_llm not installed or not accessible")
        return False, issues

    try:
        from chuk_llm.llm.client import get_client

        print("✅ get_client imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import get_client: {e}")
        issues.append("get_client not available")

    try:
        from chuk_llm.configuration import get_config

        config_manager = get_config()
        providers = config_manager.get_all_providers()

        if "perplexity" in providers:
            print("✅ Perplexity provider found in chuk_llm configuration")
        else:
            print("⚠️  Perplexity provider not found in configuration")
            print(f"   Available providers: {providers}")
            issues.append("Perplexity provider may not be configured")

    except Exception as e:
        print(f"⚠️  Could not check provider configuration: {e}")
        issues.append("Configuration check failed")

    return len(issues) == 0, issues


async def test_perplexity_connection():
    """Test direct connection to Perplexity API."""
    print("\n🌐 Perplexity API Connection Test")
    print("=" * 40)

    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("❌ Cannot test connection - PERPLEXITY_API_KEY not set")
        return False

    try:
        from chuk_llm.llm.client import get_client

        print("Creating Perplexity client...")
        client = get_client(provider="perplexity", model="sonar-pro")
        print("✅ Client created successfully")

        print("Testing API connection with simple query...")
        messages = [{"role": "user", "content": "What is 2+2? Answer briefly."}]

        start_time = time.time()
        result = await asyncio.wait_for(
            client.create_completion(messages), timeout=30.0
        )
        duration = time.time() - start_time

        if isinstance(result, dict) and "response" in result:
            response = result["response"]
            if "error" not in str(response).lower() and "401" not in str(response):
                print(f"✅ API connection successful! ({duration:.2f}s)")
                print(f"   Response: {response[:100]}...")
                return True
            else:
                print(f"❌ API returned error: {response[:200]}...")
                return False
        else:
            print(f"❌ Unexpected response format: {result}")
            return False

    except asyncio.TimeoutError:
        print("❌ API connection timed out after 30 seconds")
        return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        if "401" in str(e) or "Unauthorized" in str(e):
            print("   This suggests an API key issue")
        return False


def check_mcp_setup():
    """Check MCP-specific setup."""
    print("\n🔧 MCP Setup Check")
    print("=" * 40)

    issues = []

    try:
        from chuk_mcp_perplexity.models import (
            PerplexitySearchInput,
            PerplexitySearchResult,
        )

        print("✅ MCP Perplexity models imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MCP models: {e}")
        issues.append("MCP Perplexity models not available")

    try:
        from chuk_mcp_runtime.common.mcp_tool_decorator import mcp_tool

        print("✅ MCP tool decorator imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import MCP tool decorator: {e}")
        issues.append("MCP runtime not available")

    # Check if tools module exists
    try:
        import chuk_mcp_perplexity.tools

        print("✅ MCP Perplexity tools module found")
    except ImportError as e:
        print(f"❌ Failed to import MCP tools: {e}")
        issues.append("MCP Perplexity tools not available")

    return len(issues) == 0, issues


def show_setup_instructions():
    """Show complete setup instructions."""
    print("\n📋 Complete Setup Instructions")
    print("=" * 40)

    print("1. Get Perplexity API Key:")
    print("   • Visit: https://www.perplexity.ai/settings/api")
    print("   • Sign up/login and create an API key")
    print("   • Copy the key (starts with 'pplx-')")
    print()

    print("2. Set Environment Variable:")
    print("   Option A - .env file (recommended):")
    print("   echo 'PERPLEXITY_API_KEY=your_key_here' >> .env")
    print()
    print("   Option B - Export command:")
    print("   export PERPLEXITY_API_KEY=your_key_here")
    print()

    print("3. Install Dependencies:")
    print("   uv add chuk_llm")
    print("   uv add chuk-mcp-runtime")
    print()

    print("4. Test Setup:")
    print("   uv run python debug_perplexity_setup.py")
    print()


async def run_comprehensive_diagnostic():
    """Run all diagnostic checks."""
    print("🔍 Perplexity API Setup Diagnostic")
    print("=" * 50)
    print()

    all_passed = True

    # Environment check
    env_ok, env_issues = check_environment_setup()
    if not env_ok:
        all_passed = False

    # Installation check
    install_ok, install_issues = check_chuk_llm_installation()
    if not install_ok:
        all_passed = False

    # Connection test (only if environment is OK)
    connection_ok = False
    if env_ok:
        connection_ok = await test_perplexity_connection()
        if not connection_ok:
            all_passed = False

    # MCP setup check
    mcp_ok, mcp_issues = check_mcp_setup()
    if not mcp_ok:
        all_passed = False

    # Summary
    print("\n📊 Diagnostic Summary")
    print("=" * 40)

    print(f"Environment Setup: {'✅ PASS' if env_ok else '❌ FAIL'}")
    print(f"chuk_llm Installation: {'✅ PASS' if install_ok else '❌ FAIL'}")
    print(f"API Connection: {'✅ PASS' if connection_ok else '❌ FAIL'}")
    print(f"MCP Setup: {'✅ PASS' if mcp_ok else '❌ FAIL'}")

    print(
        f"\nOverall Status: {'🎉 ALL SYSTEMS GO!' if all_passed else '⚠️  ISSUES FOUND'}"
    )

    # Show issues and solutions
    all_issues = env_issues + install_issues + mcp_issues
    if all_issues:
        print("\n🔧 Issues Found:")
        for i, issue in enumerate(all_issues, 1):
            print(f"   {i}. {issue}")

        show_setup_instructions()

    return all_passed


def main():
    """Main diagnostic runner."""
    try:
        asyncio.run(run_comprehensive_diagnostic())
    except KeyboardInterrupt:
        print("\n⏹️  Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

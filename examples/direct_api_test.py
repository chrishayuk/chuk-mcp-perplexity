#!/usr/bin/env python3
"""
Direct Perplexity API Key Test
=============================

Tests the API key directly with Perplexity's API to verify it's valid.
"""

import asyncio
import os
from typing import Optional

# Load .env file
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    print("⚠️  python-dotenv not available")


def get_api_key() -> Optional[str]:
    """Get and validate API key."""
    api_key = os.getenv("PERPLEXITY_API_KEY")
    if not api_key:
        print("❌ PERPLEXITY_API_KEY not found in environment")
        return None

    print(f"✅ Found API key: {api_key[:15]}... (length: {len(api_key)})")

    if not api_key.startswith("pplx-"):
        print("⚠️  Warning: API key should start with 'pplx-'")

    return api_key


async def test_api_key_direct():
    """Test API key with direct HTTP request."""
    api_key = get_api_key()
    if not api_key:
        return False

    try:
        import httpx
    except ImportError:
        print("❌ httpx not available for direct testing")
        return False

    print("\n🌐 Testing API key with direct HTTP request...")

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    payload = {
        "model": "sonar-pro",
        "messages": [
            {
                "role": "user",
                "content": "Say 'API test successful' if you can read this.",
            }
        ],
        "max_tokens": 50,
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            print("📡 Sending request to Perplexity API...")
            response = await client.post(
                "https://api.perplexity.ai/chat/completions",
                headers=headers,
                json=payload,
            )

            print(f"📊 Response status: {response.status_code}")
            print(f"📊 Response headers: {dict(response.headers)}")

            if response.status_code == 200:
                data = response.json()
                print("✅ API key is valid!")
                print(f"📝 Response: {data}")
                return True
            elif response.status_code == 401:
                print("❌ API key is invalid or expired")
                print(f"📝 Response: {response.text[:500]}...")
                return False
            else:
                print(f"⚠️  Unexpected response: {response.status_code}")
                print(f"📝 Response: {response.text[:500]}...")
                return False

    except Exception as e:
        print(f"❌ Direct API test failed: {e}")
        return False


async def test_with_openai_client():
    """Test with OpenAI client (which Perplexity uses)."""
    api_key = get_api_key()
    if not api_key:
        return False

    print("\n🤖 Testing with OpenAI client...")

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

        print("📡 Making completion request...")
        completion = client.chat.completions.create(
            model="sonar-pro",
            messages=[
                {
                    "role": "user",
                    "content": "Say 'OpenAI client test successful' if you can read this.",
                }
            ],
            max_tokens=50,
        )

        print("✅ OpenAI client test successful!")
        print(f"📝 Response: {completion.choices[0].message.content}")
        return True

    except Exception as e:
        print(f"❌ OpenAI client test failed: {e}")
        if "401" in str(e) or "Unauthorized" in str(e):
            print("   This confirms the API key is invalid")
        return False


def check_api_key_format():
    """Check API key format in detail."""
    api_key = get_api_key()
    if not api_key:
        return False

    print("\n🔍 API Key Format Analysis:")
    print(f"   Full length: {len(api_key)}")
    print(f"   Starts with: {api_key[:10]}")
    print(f"   Ends with: ...{api_key[-5:]}")

    # Check for common issues
    issues = []

    if not api_key.startswith("pplx-"):
        issues.append("Should start with 'pplx-'")

    if len(api_key) < 40:
        issues.append("Seems too short (should be ~50+ characters)")

    if " " in api_key:
        issues.append("Contains spaces")

    if "\n" in api_key or "\r" in api_key:
        issues.append("Contains newline characters")

    if issues:
        print("⚠️  Potential issues found:")
        for issue in issues:
            print(f"     - {issue}")
        return False
    else:
        print("✅ Format looks correct")
        return True


async def main():
    """Run all API key tests."""
    print("🔑 Perplexity API Key Validation")
    print("=" * 35)

    # Check format
    format_ok = check_api_key_format()

    if not format_ok:
        print("\n❌ API key format issues detected")
        print("\n📝 To get a new API key:")
        print("   1. Go to: https://www.perplexity.ai/settings/api")
        print("   2. Delete the old key if it exists")
        print("   3. Create a new API key")
        print("   4. Copy the FULL key including 'pplx-' prefix")
        print("   5. Update your .env file: PERPLEXITY_API_KEY=pplx-your-new-key")
        return

    # Test with direct HTTP
    print("\n" + "=" * 50)
    direct_ok = await test_api_key_direct()

    # Test with OpenAI client
    print("\n" + "=" * 50)
    openai_ok = await test_with_openai_client()

    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary:")
    print(f"   Format check: {'✅ PASS' if format_ok else '❌ FAIL'}")
    print(f"   Direct HTTP:  {'✅ PASS' if direct_ok else '❌ FAIL'}")
    print(f"   OpenAI client: {'✅ PASS' if openai_ok else '❌ FAIL'}")

    if direct_ok and openai_ok:
        print("\n🎉 API key is valid! The issue is elsewhere.")
    else:
        print("\n❌ API key is invalid or expired.")
        print("\n🔧 Next steps:")
        print("   1. Double-check you copied the FULL API key")
        print("   2. Verify the key is still active in Perplexity settings")
        print("   3. Try generating a new API key")
        print("   4. Make sure there are no extra spaces or characters")


if __name__ == "__main__":
    asyncio.run(main())

"""chuk_mcp_perplexity.tools

Async MCP tools backed by Perplexity Sonar models via **chuk-llm**
with per-tool timeout configuration
=================================================================

Exposed tools
-------------
* **perplexity_search** - quick answers with `sonar-pro` (30s timeout).
* **perplexity_deep_research** - long-form research answers with
  `sonar-reasoning-pro` (90s timeout).
* **perplexity_quick_fact** - ultra-fast fact checking (15s timeout).
* **perplexity_search_with_citations** - citation-focused search (45s timeout).

Key points
~~~~~~~~~~
* The tools are **native async** with configurable per-tool timeouts
* Each tool has an appropriate timeout based on expected response time
* Timeout can be overridden in config.yaml or environment variables
* Uses stable chuk_llm client API (discovery-independent)
"""

from __future__ import annotations

import asyncio
from typing import Dict, List

from pydantic import ValidationError

# Import stable chuk_llm client API (discovery-independent)
from chuk_llm.llm.client import get_client
from chuk_mcp_runtime.common.mcp_tool_decorator import mcp_tool

from .models import (
    PerplexitySearchInput,
    PerplexitySearchResult,
    PerplexityResearchInput,
    PerplexityResearchResult,
)

# ---------------------------------------------------------------------------
# Tool: perplexity_search (30 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_search",
    description="Quick conversational answer using Perplexity sonar-pro",
    timeout=30  # 30 seconds for quick search
)
async def perplexity_search(query: str) -> Dict:
    """
    Return a short, conversational answer using Perplexity sonar-pro.
    
    Args:
        query: User query to be answered briefly
    """
    try:
        validated = PerplexitySearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_search: {exc}")

    try:
        # Use stable chuk_llm client API
        client = get_client("perplexity", model="sonar-pro")
        messages = [{"role": "user", "content": validated.query}]
        result = await client.create_completion(messages=messages)
        return PerplexitySearchResult(answer=result["response"]).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity search timed out after 30 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity search failed: {str(e)}")


# ---------------------------------------------------------------------------
# Tool: perplexity_deep_research (90 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_deep_research",
    description="Comprehensive, citation-rich answer using Perplexity sonar-reasoning-pro",
    timeout=90  # 90 seconds for deep research
)
async def perplexity_deep_research(query: str) -> Dict:
    """
    Return an in-depth, well-sourced answer using Perplexity sonar-reasoning-pro.
    
    Args:
        query: User query requiring in-depth research
    """
    try:
        validated = PerplexityResearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_deep_research: {exc}")

    # Enhanced prompt for comprehensive research
    research_prompt = f"""Please provide a comprehensive, well-researched answer to: {validated.query}

Requirements:
- Include multiple reliable sources with citations
- Provide detailed analysis and context
- Include relevant statistics or data when available
- Mention any conflicting viewpoints or limitations
- Use clear, structured formatting"""

    try:
        # Use stable chuk_llm client API with reasoning model
        client = get_client("perplexity", model="sonar-reasoning-pro")
        messages = [{"role": "user", "content": research_prompt}]
        result = await client.create_completion(messages=messages)
        return PerplexityResearchResult(answer=result["response"]).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity deep research timed out after 90 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity deep research failed: {str(e)}")


# ---------------------------------------------------------------------------
# Tool: perplexity_quick_fact (15 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_quick_fact",
    description="Ultra-fast fact checking using Perplexity sonar",
    timeout=15  # 15 seconds for quick facts
)
async def perplexity_quick_fact(query: str) -> Dict:
    """
    Return a quick factual answer for simple queries.
    
    Args:
        query: Simple factual query
    """
    try:
        validated = PerplexitySearchInput(query=f"Quick fact: {query}")
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_quick_fact: {exc}")

    try:
        # Use fast sonar model for quick facts
        client = get_client("perplexity", model="sonar")
        messages = [{"role": "user", "content": validated.query}]
        result = await client.create_completion(messages=messages)
        return PerplexitySearchResult(answer=result["response"]).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity quick fact timed out after 15 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity quick fact failed: {str(e)}")


# ---------------------------------------------------------------------------
# Tool: perplexity_search_with_citations (45 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_search_with_citations",
    description="Search with explicit citation requirements using Perplexity sonar-pro",
    timeout=45  # 45 seconds for citation-heavy search
)
async def perplexity_search_with_citations(query: str) -> Dict:
    """
    Return an answer with explicit citation requirements.
    
    Args:
        query: User query that needs citations
    """
    try:
        validated = PerplexitySearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_search_with_citations: {exc}")

    # Enhanced prompt for better citations
    enhanced_query = f"""Please provide a comprehensive answer to: {validated.query}

Please include:
- Clear, specific citations for all facts
- Source URLs where possible
- Publication dates when available
- Multiple sources for verification"""

    try:
        client = get_client("perplexity", model="sonar-pro")
        messages = [{"role": "user", "content": enhanced_query}]
        result = await client.create_completion(messages=messages)
        return PerplexitySearchResult(answer=result["response"]).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity search with citations timed out after 45 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity search with citations failed: {str(e)}")


# ---------------------------------------------------------------------------
# Tool: perplexity_current_events (45 second timeout)
# ---------------------------------------------------------------------------
@mcp_tool(
    name="perplexity_current_events",
    description="Real-time news and current events using Perplexity sonar-pro",
    timeout=45  # 45 seconds for current events
)
async def perplexity_current_events(query: str) -> Dict:
    """
    Return current news and events related to the query.
    
    Args:
        query: Topic to search for current events
    """
    try:
        validated = PerplexitySearchInput(query=query)
    except ValidationError as exc:
        raise ValueError(f"Invalid input for perplexity_current_events: {exc}")

    # Enhanced prompt for current events
    events_prompt = f"""Please provide current news and recent developments about: {validated.query}

Focus on:
- Latest news from the past week
- Recent developments and trends
- Reliable news sources with publication dates
- Key facts and figures
- Important context for understanding current situation"""

    try:
        client = get_client("perplexity", model="sonar-pro")
        messages = [{"role": "user", "content": events_prompt}]
        result = await client.create_completion(messages=messages)
        return PerplexitySearchResult(answer=result["response"]).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity current events search timed out after 45 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity current events search failed: {str(e)}")
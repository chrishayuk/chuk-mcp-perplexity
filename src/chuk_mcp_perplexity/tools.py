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

Key points
~~~~~~~~~~
* The tools are **native async** with configurable per-tool timeouts
* Each tool has an appropriate timeout based on expected response time
* Timeout can be overridden in config.yaml or environment variables
* Uses latest chuk_llm API with auto-generated provider functions
"""

from __future__ import annotations

import asyncio
from typing import Dict, List

from pydantic import ValidationError

# Import latest chuk_llm API
from chuk_llm import ask_perplexity, ask_perplexity_sync
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

    # Use latest chuk_llm API with auto-generated function
    try:
        result = await ask_perplexity(
            validated.query,
            model="sonar-pro"
        )
        return PerplexitySearchResult(answer=result).model_dump()
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

    # Use latest chuk_llm API with reasoning model
    try:
        result = await ask_perplexity(
            validated.query,
            model="sonar-reasoning-pro"
        )
        return PerplexityResearchResult(answer=result).model_dump()
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

    # Use latest chuk_llm API with fast sonar model
    try:
        result = await ask_perplexity(
            validated.query,
            model="sonar"  # Faster model for quick facts
        )
        return PerplexitySearchResult(answer=result).model_dump()
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
        result = await ask_perplexity(
            enhanced_query,
            model="sonar-pro"
        )
        return PerplexitySearchResult(answer=result).model_dump()
    except asyncio.TimeoutError:
        raise ValueError("Perplexity search with citations timed out after 45 seconds")
    except Exception as e:
        raise ValueError(f"Perplexity search with citations failed: {str(e)}")


# ---------------------------------------------------------------------------
# Utility function for sync usage
# ---------------------------------------------------------------------------
def perplexity_search_sync(query: str, model: str = "sonar-pro") -> str:
    """
    Synchronous wrapper for Perplexity search - useful for testing.
    
    Args:
        query: User query
        model: Perplexity model to use
        
    Returns:
        Response string
    """
    return ask_perplexity_sync(query, model=model)